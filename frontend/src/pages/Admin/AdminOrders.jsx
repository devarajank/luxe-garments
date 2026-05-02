import { useEffect, useState } from 'react';

const STATUS_COLOR = {
  pending: '#888', confirmed: '#0066c0', shipped: '#e47911',
  delivered: '#007600', cancelled: '#c00',
  return_requested: '#8B5CF6', returned: '#555',
};

const STATUS_LABEL = {
  pending: 'Pending', confirmed: 'Confirmed', shipped: 'Shipped',
  delivered: 'Delivered', cancelled: 'Cancelled',
  return_requested: 'Return Requested', returned: 'Returned',
};

export default function AdminOrders() {
  const [tab, setTab] = useState('all'); // 'all' | 'returns'
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [actionLoading, setActionLoading] = useState(null);
  const [refundInput, setRefundInput] = useState({}); // orderId → amount string

  const adminHeaders = { 'x-user-role': 'admin', 'Content-Type': 'application/json' };

  const fetchOrders = async (statusFilter) => {
    setLoading(true);
    setError(null);
    try {
      const url = statusFilter
        ? `/api/orders/admin/all?status=${statusFilter}&limit=100`
        : '/api/orders/admin/all?limit=100';
      const res = await fetch(url, { headers: adminHeaders });
      if (!res.ok) throw new Error(`Failed to fetch orders: ${res.status}`);
      const data = await res.json();
      setOrders(data.orders || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchOrders(tab === 'returns' ? 'return_requested' : null);
  }, [tab]);

  const approveReturn = async (orderId) => {
    const amount = parseFloat(refundInput[orderId]);
    setActionLoading(orderId);
    try {
      const res = await fetch(`/api/orders/${orderId}/approve-return`, {
        method: 'PUT',
        headers: adminHeaders,
        body: JSON.stringify({ refund_amount: isNaN(amount) ? null : amount }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Approve failed');
      setOrders(prev => prev.filter(o => o.id !== orderId));
    } catch (e) {
      alert(e.message);
    } finally {
      setActionLoading(null);
    }
  };

  const rejectReturn = async (orderId) => {
    setActionLoading(orderId);
    try {
      const res = await fetch(`/api/orders/${orderId}/reject-return`, {
        method: 'PUT',
        headers: adminHeaders,
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Reject failed');
      setOrders(prev => prev.filter(o => o.id !== orderId));
    } catch (e) {
      alert(e.message);
    } finally {
      setActionLoading(null);
    }
  };

  const returnCount = orders.filter(o => o.status === 'return_requested').length;

  return (
    <div style={{ padding: '24px' }}>
      <h1 style={{ fontSize: '28px', fontWeight: 'bold', marginBottom: '20px' }}>Orders</h1>

      {/* Tabs */}
      <div style={{ display: 'flex', gap: '0', marginBottom: '20px', borderBottom: '2px solid #f0f0f0' }}>
        {[
          { key: 'all', label: 'All Orders' },
          { key: 'returns', label: `Returns${tab !== 'returns' && returnCount > 0 ? ` (${returnCount})` : ''}` },
        ].map(t => (
          <button
            key={t.key}
            onClick={() => setTab(t.key)}
            style={{
              padding: '10px 20px', background: 'none', border: 'none',
              borderBottom: tab === t.key ? '2px solid #e47911' : '2px solid transparent',
              fontSize: '14px', fontWeight: tab === t.key ? '600' : '400',
              color: tab === t.key ? '#e47911' : '#555',
              cursor: 'pointer', marginBottom: '-2px',
            }}
          >
            {t.label}
          </button>
        ))}
      </div>

      {loading ? (
        <p style={{ fontSize: '14px', color: '#666' }}>Loading…</p>
      ) : error ? (
        <p style={{ fontSize: '14px', color: '#c00' }}>Error: {error}</p>
      ) : orders.length === 0 ? (
        <p style={{ fontSize: '14px', color: '#666' }}>
          {tab === 'returns' ? 'No pending return requests.' : 'No orders found.'}
        </p>
      ) : tab === 'returns' ? (
        /* Returns view */
        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          {orders.map(order => (
            <div key={order.id} style={{
              background: '#fff', border: '1px solid #e0d0f8', borderRadius: '8px',
              padding: '16px', boxShadow: '0 1px 3px rgba(0,0,0,0.06)',
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', flexWrap: 'wrap', gap: '8px' }}>
                <div>
                  <div style={{ fontSize: '12px', color: '#888', marginBottom: '2px' }}>
                    Order #{order.id.substring(0, 8)} · {new Date(order.created_at).toLocaleDateString('en-IN')}
                  </div>
                  <div style={{ fontSize: '13px', color: '#555', marginBottom: '4px' }}>
                    Customer: <strong>{order.user_id?.substring(0, 16)}</strong>
                  </div>
                  <div style={{ fontSize: '13px', color: '#111', marginBottom: '4px' }}>
                    Total: <strong>₹{Number(order.total).toFixed(2)}</strong>
                  </div>
                  <div style={{
                    fontSize: '13px', background: '#f3eeff', color: '#8B5CF6',
                    padding: '6px 10px', borderRadius: '6px', marginTop: '6px',
                    maxWidth: '360px',
                  }}>
                    <span style={{ fontWeight: '600' }}>Return reason: </span>
                    {order.return_reason || '—'}
                  </div>
                  <div style={{ marginTop: '6px', fontSize: '12px', color: '#555' }}>
                    Items: {order.items?.map(i => i.product_name).join(', ')}
                  </div>
                </div>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', alignItems: 'flex-end' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <span style={{ fontSize: '12px', color: '#555' }}>Refund ₹</span>
                    <input
                      type="number"
                      min="0"
                      step="0.01"
                      placeholder={Number(order.total).toFixed(2)}
                      value={refundInput[order.id] ?? ''}
                      onChange={e => setRefundInput(prev => ({ ...prev, [order.id]: e.target.value }))}
                      style={{
                        width: '100px', padding: '5px 8px', border: '1px solid #ccc',
                        borderRadius: '4px', fontSize: '13px',
                      }}
                    />
                  </div>
                  <button
                    onClick={() => approveReturn(order.id)}
                    disabled={actionLoading === order.id}
                    style={{
                      padding: '7px 16px', background: '#007600', color: '#fff',
                      border: 'none', borderRadius: '6px', cursor: 'pointer',
                      fontSize: '13px', fontWeight: '500', opacity: actionLoading === order.id ? 0.6 : 1,
                    }}
                  >
                    {actionLoading === order.id ? 'Processing…' : 'Approve & Refund'}
                  </button>
                  <button
                    onClick={() => rejectReturn(order.id)}
                    disabled={actionLoading === order.id}
                    style={{
                      padding: '7px 16px', background: '#fff', color: '#c00',
                      border: '1px solid #c00', borderRadius: '6px', cursor: 'pointer',
                      fontSize: '13px', fontWeight: '500', opacity: actionLoading === order.id ? 0.6 : 1,
                    }}
                  >
                    Reject
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        /* All orders table */
        <div style={{ background: '#fff', padding: '20px', borderRadius: '4px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)', overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ borderBottom: '2px solid #f0f0f0' }}>
                {['Order ID', 'Customer', 'Total', 'Status', 'Return Reason', 'Date'].map(h => (
                  <th key={h} style={{ padding: '12px', textAlign: 'left', fontSize: '13px', fontWeight: 'bold' }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {orders.map(order => (
                <tr key={order.id} style={{ borderBottom: '1px solid #f0f0f0' }}>
                  <td style={{ padding: '12px', fontSize: '12px', fontWeight: 'bold' }}>{order.id.substring(0, 8)}</td>
                  <td style={{ padding: '12px', fontSize: '12px' }}>{order.user_id?.substring(0, 14)}…</td>
                  <td style={{ padding: '12px', fontSize: '12px' }}>₹{Number(order.total).toFixed(2)}</td>
                  <td style={{ padding: '12px' }}>
                    <span style={{
                      background: STATUS_COLOR[order.status] || '#888',
                      color: '#fff', padding: '3px 8px', borderRadius: '3px',
                      fontSize: '11px', fontWeight: 'bold',
                    }}>
                      {STATUS_LABEL[order.status] || order.status}
                    </span>
                  </td>
                  <td style={{ padding: '12px', fontSize: '12px', color: '#8B5CF6', maxWidth: '200px' }}>
                    {order.return_reason || '—'}
                  </td>
                  <td style={{ padding: '12px', fontSize: '12px' }}>
                    {new Date(order.created_at).toLocaleDateString('en-IN')}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          <p style={{ marginTop: '16px', fontSize: '12px', color: '#666' }}>{orders.length} orders</p>
        </div>
      )}
    </div>
  );
}
