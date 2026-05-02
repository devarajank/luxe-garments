import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const STATUS_LABEL = {
  pending: { text: 'Pending', color: '#888' },
  confirmed: { text: 'Confirmed', color: '#0066c0' },
  shipped: { text: 'Shipped', color: '#e47911' },
  delivered: { text: 'Delivered', color: '#007600' },
  cancelled: { text: 'Cancelled', color: '#c00' },
  return_requested: { text: 'Return Requested', color: '#8B5CF6' },
  returned: { text: 'Returned', color: '#555' },
};

function StatusBadge({ status }) {
  const s = STATUS_LABEL[status] || { text: status, color: '#888' };
  return (
    <span style={{
      fontSize: '12px',
      fontWeight: '600',
      color: s.color,
      background: s.color + '18',
      padding: '2px 8px',
      borderRadius: '12px',
      border: `1px solid ${s.color}40`,
    }}>
      {s.text}
    </span>
  );
}

export default function Orders() {
  const { user, token } = useAuth();
  const navigate = useNavigate();
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedOrder, setSelectedOrder] = useState(null);
  const [actionLoading, setActionLoading] = useState(null);
  const [returnModal, setReturnModal] = useState(null); // order id awaiting reason
  const [returnReason, setReturnReason] = useState('');

  useEffect(() => {
    if (!user) {
      navigate('/login', { state: { from: '/orders' } });
      return;
    }
    fetchOrders();
  }, [user]);

  const authHeaders = () => ({
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`,
    'x-user-id': user?.id,
  });

  const fetchOrders = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await fetch('http://localhost:8000/api/orders/', {
        headers: authHeaders(),
      });
      if (!res.ok) throw new Error('Failed to fetch orders');
      const data = await res.json();
      setOrders(data.orders || []);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const cancelOrder = async (orderId) => {
    setActionLoading(orderId);
    try {
      const res = await fetch(`http://localhost:8000/api/orders/${orderId}/cancel`, {
        method: 'PUT',
        headers: authHeaders(),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Cancel failed');
      setOrders(prev => prev.map(o => o.id === orderId ? data : o));
      if (selectedOrder?.id === orderId) setSelectedOrder(data);
    } catch (e) {
      alert(e.message);
    } finally {
      setActionLoading(null);
    }
  };

  const openReturnModal = (orderId) => {
    setReturnReason('');
    setReturnModal(orderId);
  };

  const submitReturn = async () => {
    if (!returnReason.trim()) return;
    const orderId = returnModal;
    setReturnModal(null);
    setActionLoading(orderId);
    try {
      const res = await fetch(`/api/orders/${orderId}/return`, {
        method: 'PUT',
        headers: authHeaders(),
        body: JSON.stringify({ reason: returnReason.trim() }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Return request failed');
      setOrders(prev => prev.map(o => o.id === orderId ? data : o));
      if (selectedOrder?.id === orderId) setSelectedOrder(data);
    } catch (e) {
      alert(e.message);
    } finally {
      setActionLoading(null);
    }
  };

  const formatDate = (iso) =>
    new Date(iso).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' });

  if (loading) return (
    <div style={{ padding: '48px', textAlign: 'center', color: '#888' }}>Loading orders…</div>
  );

  if (error) return (
    <div style={{ padding: '48px', textAlign: 'center', color: '#c00' }}>{error}</div>
  );

  return (
    <div style={{ maxWidth: '960px', margin: '0 auto', padding: '24px 16px' }}>
      <h1 style={{ fontSize: '24px', fontWeight: '400', marginBottom: '24px', color: '#111' }}>
        Your Orders
      </h1>

      {orders.length === 0 ? (
        <div style={{
          background: '#fff',
          border: '1px solid #ddd',
          borderRadius: '8px',
          padding: '48px',
          textAlign: 'center',
          color: '#888',
        }}>
          <div style={{ fontSize: '48px', marginBottom: '12px' }}>📦</div>
          <p style={{ fontSize: '16px' }}>You haven't placed any orders yet.</p>
          <button
            onClick={() => navigate('/')}
            style={{
              marginTop: '16px',
              background: '#FFD814',
              border: '1px solid #FCD200',
              borderRadius: '8px',
              padding: '8px 20px',
              cursor: 'pointer',
              fontWeight: '500',
            }}
          >
            Start Shopping
          </button>
        </div>
      ) : (
        <div style={{ display: 'flex', gap: '20px', alignItems: 'flex-start' }}>
          {/* Order list */}
          <div style={{ flex: 1 }}>
            {orders.map(order => (
              <div
                key={order.id}
                onClick={() => setSelectedOrder(selectedOrder?.id === order.id ? null : order)}
                style={{
                  background: '#fff',
                  border: `1px solid ${selectedOrder?.id === order.id ? '#e47911' : '#ddd'}`,
                  borderRadius: '8px',
                  padding: '16px',
                  marginBottom: '12px',
                  cursor: 'pointer',
                  transition: 'border-color 0.15s',
                }}
              >
                {/* Order header */}
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '12px' }}>
                  <div>
                    <div style={{ fontSize: '12px', color: '#555' }}>ORDER PLACED</div>
                    <div style={{ fontSize: '13px', fontWeight: '500' }}>{formatDate(order.created_at)}</div>
                  </div>
                  <div style={{ textAlign: 'right' }}>
                    <div style={{ fontSize: '12px', color: '#555' }}>TOTAL</div>
                    <div style={{ fontSize: '13px', fontWeight: '600' }}>₹{Number(order.total).toFixed(2)}</div>
                  </div>
                  <div style={{ textAlign: 'right' }}>
                    <div style={{ fontSize: '12px', color: '#555', marginBottom: '4px' }}>STATUS</div>
                    <StatusBadge status={order.status} />
                  </div>
                </div>

                {/* Items preview */}
                <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                  {order.items.map((item, i) => (
                    <div key={i} style={{ fontSize: '13px', color: '#333' }}>
                      {item.product_name || `Product ${item.product_id}`}
                      {item.size ? ` (${item.size})` : ''}
                      {item.quantity > 1 ? ` ×${item.quantity}` : ''}
                      {i < order.items.length - 1 && ','}
                    </div>
                  ))}
                </div>

                {/* Order ID */}
                <div style={{ marginTop: '8px', fontSize: '11px', color: '#999' }}>
                  Order # {order.id}
                </div>
              </div>
            ))}
          </div>

          {/* Order detail panel */}
          {selectedOrder && (
            <div style={{
              width: '320px',
              flexShrink: 0,
              background: '#fff',
              border: '1px solid #ddd',
              borderRadius: '8px',
              padding: '20px',
              position: 'sticky',
              top: '16px',
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
                <h2 style={{ fontSize: '16px', fontWeight: '600', margin: 0 }}>Order Details</h2>
                <button
                  onClick={() => setSelectedOrder(null)}
                  style={{ background: 'none', border: 'none', cursor: 'pointer', fontSize: '18px', color: '#888' }}
                >
                  ×
                </button>
              </div>

              <div style={{ marginBottom: '12px' }}>
                <StatusBadge status={selectedOrder.status} />
              </div>

              <div style={{ fontSize: '12px', color: '#555', marginBottom: '16px' }}>
                Placed: {formatDate(selectedOrder.created_at)}
              </div>

              {/* Items */}
              <div style={{ borderTop: '1px solid #eee', paddingTop: '12px', marginBottom: '12px' }}>
                {selectedOrder.items.map((item, i) => (
                  <div key={i} style={{ marginBottom: '10px', display: 'flex', justifyContent: 'space-between', fontSize: '13px' }}>
                    <div>
                      <div style={{ fontWeight: '500' }}>{item.product_name || `Product ${item.product_id}`}</div>
                      {(item.size || item.color) && (
                        <div style={{ color: '#888', fontSize: '12px' }}>
                          {[item.size, item.color].filter(Boolean).join(' · ')}
                        </div>
                      )}
                      <div style={{ color: '#888', fontSize: '12px' }}>Qty: {item.quantity}</div>
                    </div>
                    <div style={{ fontWeight: '500' }}>₹{(item.price * item.quantity).toFixed(2)}</div>
                  </div>
                ))}
              </div>

              {/* Totals */}
              <div style={{ borderTop: '1px solid #eee', paddingTop: '12px', fontSize: '13px' }}>
                {selectedOrder.discount_amount > 0 && (
                  <div style={{ display: 'flex', justifyContent: 'space-between', color: '#007600', marginBottom: '4px' }}>
                    <span>Discount ({selectedOrder.promotion_code})</span>
                    <span>-₹{Number(selectedOrder.discount_amount).toFixed(2)}</span>
                  </div>
                )}
                <div style={{ display: 'flex', justifyContent: 'space-between', fontWeight: '700', fontSize: '15px' }}>
                  <span>Total</span>
                  <span>₹{Number(selectedOrder.total).toFixed(2)}</span>
                </div>
              </div>

              {/* Shipping address */}
              {selectedOrder.shipping_address && (
                <div style={{ borderTop: '1px solid #eee', paddingTop: '12px', marginTop: '12px', fontSize: '12px', color: '#555' }}>
                  <div style={{ fontWeight: '600', marginBottom: '4px', color: '#111' }}>Ship to</div>
                  <div>{selectedOrder.shipping_address.full_name}</div>
                  <div>{selectedOrder.shipping_address.address_line1}</div>
                  {selectedOrder.shipping_address.address_line2 && <div>{selectedOrder.shipping_address.address_line2}</div>}
                  <div>{selectedOrder.shipping_address.city}, {selectedOrder.shipping_address.state} {selectedOrder.shipping_address.postal_code}</div>
                </div>
              )}

              {/* Return info */}
              {selectedOrder.return_reason && (
                <div style={{ borderTop: '1px solid #eee', paddingTop: '12px', marginTop: '12px', fontSize: '12px' }}>
                  <div style={{ fontWeight: '600', color: '#8B5CF6', marginBottom: '4px' }}>Return Reason</div>
                  <div style={{ color: '#555' }}>{selectedOrder.return_reason}</div>
                  {selectedOrder.refund_amount != null && (
                    <div style={{ marginTop: '6px', color: '#007600', fontWeight: '600' }}>
                      Refund: ₹{Number(selectedOrder.refund_amount).toFixed(2)}
                    </div>
                  )}
                </div>
              )}

              {/* Actions */}
              <div style={{ marginTop: '16px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
                {(selectedOrder.status === 'pending' || selectedOrder.status === 'confirmed') && (
                  <button
                    onClick={() => cancelOrder(selectedOrder.id)}
                    disabled={actionLoading === selectedOrder.id}
                    style={{
                      background: actionLoading === selectedOrder.id ? '#f5f5f5' : '#fff',
                      border: '1px solid #c00',
                      borderRadius: '6px',
                      padding: '8px',
                      cursor: actionLoading === selectedOrder.id ? 'not-allowed' : 'pointer',
                      color: '#c00',
                      fontSize: '13px',
                      fontWeight: '500',
                    }}
                  >
                    {actionLoading === selectedOrder.id ? 'Processing…' : 'Cancel Order'}
                  </button>
                )}
                {selectedOrder.status === 'delivered' && (
                  <button
                    onClick={() => openReturnModal(selectedOrder.id)}
                    disabled={actionLoading === selectedOrder.id}
                    style={{
                      background: actionLoading === selectedOrder.id ? '#f5f5f5' : '#fff',
                      border: '1px solid #8B5CF6',
                      borderRadius: '6px',
                      padding: '8px',
                      cursor: actionLoading === selectedOrder.id ? 'not-allowed' : 'pointer',
                      color: '#8B5CF6',
                      fontSize: '13px',
                      fontWeight: '500',
                    }}
                  >
                    {actionLoading === selectedOrder.id ? 'Processing…' : 'Request Return'}
                  </button>
                )}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Return reason modal */}
      {returnModal && (
        <div style={{
          position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.45)',
          display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000,
        }}>
          <div style={{
            background: '#fff', borderRadius: '8px', padding: '24px',
            width: '100%', maxWidth: '420px', boxShadow: '0 8px 32px rgba(0,0,0,0.18)',
          }}>
            <h3 style={{ fontSize: '18px', fontWeight: '600', marginBottom: '8px', color: '#111' }}>
              Request Return
            </h3>
            <p style={{ fontSize: '13px', color: '#555', marginBottom: '16px' }}>
              Please tell us why you want to return this order.
            </p>
            <textarea
              value={returnReason}
              onChange={e => setReturnReason(e.target.value)}
              placeholder="e.g. Wrong size, damaged item, not as described…"
              rows={4}
              autoFocus
              style={{
                width: '100%', padding: '10px', border: '1px solid #a6a6a6',
                borderRadius: '4px', fontSize: '13px', boxSizing: 'border-box',
                resize: 'vertical', outline: 'none',
              }}
            />
            <div style={{ display: 'flex', gap: '8px', marginTop: '16px', justifyContent: 'flex-end' }}>
              <button
                onClick={() => setReturnModal(null)}
                style={{
                  padding: '8px 16px', border: '1px solid #ddd', borderRadius: '6px',
                  background: '#fff', cursor: 'pointer', fontSize: '13px',
                }}
              >
                Cancel
              </button>
              <button
                onClick={submitReturn}
                disabled={!returnReason.trim()}
                style={{
                  padding: '8px 16px', border: '1px solid #8B5CF6', borderRadius: '6px',
                  background: returnReason.trim() ? '#8B5CF6' : '#e5e0f5',
                  color: '#fff', cursor: returnReason.trim() ? 'pointer' : 'not-allowed',
                  fontSize: '13px', fontWeight: '500',
                }}
              >
                Submit Return
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
