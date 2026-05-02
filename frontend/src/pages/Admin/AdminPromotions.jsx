import { useEffect, useState } from 'react';

const ADMIN = { 'x-user-role': 'admin', 'x-user-id': 'admin', 'Content-Type': 'application/json' };

const EMPTY_FORM = {
  code: '',
  description: '',
  discount_type: 'percentage',
  discount_value: '',
  min_order_value: '',
  max_discount: '',
  usage_limit: '',
  per_user_limit: '1',
  start_date: '',
  end_date: '',
  is_active: true,
};

function fmt(dt) {
  if (!dt) return '—';
  return new Date(dt).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' });
}

function isExpired(p) {
  if (!p.is_active) return true;
  if (p.end_date && new Date(p.end_date) < new Date()) return true;
  return false;
}

export default function AdminPromotions() {
  const [promotions, setPromotions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState(EMPTY_FORM);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => { fetchPromotions(); }, []);

  const fetchPromotions = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/promotions/', { headers: ADMIN });
      const data = await res.json();
      setPromotions(data.promotions || []);
    } catch {
      setError('Failed to load promotions');
    } finally {
      setLoading(false);
    }
  };

  const handleFormChange = (e) => {
    const { name, value, type, checked } = e.target;
    setForm(prev => ({ ...prev, [name]: type === 'checkbox' ? checked : value }));
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    setSaving(true);
    setError('');
    try {
      const body = {
        code: form.code.trim().toUpperCase(),
        description: form.description,
        discount_type: form.discount_type,
        discount_value: parseFloat(form.discount_value),
        per_user_limit: parseInt(form.per_user_limit) || 1,
        is_active: form.is_active,
      };
      if (form.min_order_value) body.min_order_value = parseFloat(form.min_order_value);
      if (form.max_discount) body.max_discount = parseFloat(form.max_discount);
      if (form.usage_limit) body.usage_limit = parseInt(form.usage_limit);
      if (form.start_date) body.start_date = new Date(form.start_date).toISOString();
      if (form.end_date) body.end_date = new Date(form.end_date).toISOString();

      const res = await fetch('/api/promotions/', {
        method: 'POST',
        headers: ADMIN,
        body: JSON.stringify(body),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Failed to create promotion');
      setPromotions(prev => [data, ...prev]);
      setShowForm(false);
      setForm(EMPTY_FORM);
    } catch (err) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  };

  const handleDeactivate = async (id) => {
    if (!confirm('Deactivate this promotion?')) return;
    try {
      const res = await fetch(`/api/promotions/${id}`, { method: 'DELETE', headers: ADMIN });
      if (!res.ok) throw new Error('Failed');
      setPromotions(prev => prev.map(p => p.id === id ? { ...p, is_active: false } : p));
    } catch {
      alert('Could not deactivate promotion');
    }
  };

  const handleReactivate = async (id) => {
    try {
      const res = await fetch(`/api/promotions/${id}`, {
        method: 'PUT',
        headers: ADMIN,
        body: JSON.stringify({ is_active: true }),
      });
      if (!res.ok) throw new Error('Failed');
      const data = await res.json();
      setPromotions(prev => prev.map(p => p.id === id ? data : p));
    } catch {
      alert('Could not reactivate promotion');
    }
  };

  const filtered = promotions.filter(p => {
    if (filter === 'active') return !isExpired(p);
    if (filter === 'inactive') return isExpired(p);
    return true;
  });

  return (
    <div style={{ padding: '24px' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '24px' }}>
        <h1 style={{ fontSize: '28px', fontWeight: 'bold' }}>Promotions</h1>
        <button
          onClick={() => { setShowForm(true); setError(''); setForm(EMPTY_FORM); }}
          style={{ background: '#FF9900', color: 'black', padding: '10px 20px', borderRadius: '4px', fontWeight: 'bold', fontSize: '13px', border: 'none', cursor: 'pointer' }}
        >
          + New Promotion
        </button>
      </div>

      {/* Filter tabs */}
      <div style={{ display: 'flex', gap: '0', marginBottom: '20px', borderBottom: '2px solid #f0f0f0' }}>
        {['all', 'active', 'inactive'].map(tab => (
          <button
            key={tab}
            onClick={() => setFilter(tab)}
            style={{
              padding: '8px 20px', background: 'none', border: 'none', cursor: 'pointer',
              fontSize: '13px', fontWeight: filter === tab ? 'bold' : 'normal',
              color: filter === tab ? '#FF9900' : '#555',
              borderBottom: filter === tab ? '2px solid #FF9900' : '2px solid transparent',
              marginBottom: '-2px', textTransform: 'capitalize'
            }}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* Create Form */}
      {showForm && (
        <div style={{ background: '#fff', borderRadius: '4px', padding: '24px', marginBottom: '24px', boxShadow: '0 1px 3px rgba(0,0,0,0.12)' }}>
          <h2 style={{ fontSize: '16px', fontWeight: 'bold', marginBottom: '20px' }}>Create Promotion</h2>
          {error && <p style={{ color: '#B12704', fontSize: '13px', marginBottom: '12px' }}>{error}</p>}
          <form onSubmit={handleCreate}>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
              <div>
                <label style={{ fontSize: '12px', fontWeight: 'bold', display: 'block', marginBottom: '4px' }}>Code *</label>
                <input name="code" value={form.code} onChange={handleFormChange} required placeholder="e.g. SAVE20"
                  style={{ width: '100%', padding: '8px 10px', border: '1px solid #ddd', borderRadius: '4px', fontSize: '13px', textTransform: 'uppercase', boxSizing: 'border-box' }} />
              </div>
              <div>
                <label style={{ fontSize: '12px', fontWeight: 'bold', display: 'block', marginBottom: '4px' }}>Description</label>
                <input name="description" value={form.description} onChange={handleFormChange} placeholder="e.g. Save 20% on all orders"
                  style={{ width: '100%', padding: '8px 10px', border: '1px solid #ddd', borderRadius: '4px', fontSize: '13px', boxSizing: 'border-box' }} />
              </div>
              <div>
                <label style={{ fontSize: '12px', fontWeight: 'bold', display: 'block', marginBottom: '4px' }}>Discount Type *</label>
                <select name="discount_type" value={form.discount_type} onChange={handleFormChange}
                  style={{ width: '100%', padding: '8px 10px', border: '1px solid #ddd', borderRadius: '4px', fontSize: '13px', boxSizing: 'border-box' }}>
                  <option value="percentage">Percentage (%)</option>
                  <option value="fixed">Fixed Amount (₹)</option>
                </select>
              </div>
              <div>
                <label style={{ fontSize: '12px', fontWeight: 'bold', display: 'block', marginBottom: '4px' }}>
                  Discount Value * {form.discount_type === 'percentage' ? '(%)' : '(₹)'}
                </label>
                <input name="discount_value" type="number" min="0" step="0.01" value={form.discount_value} onChange={handleFormChange} required placeholder={form.discount_type === 'percentage' ? '10' : '50'}
                  style={{ width: '100%', padding: '8px 10px', border: '1px solid #ddd', borderRadius: '4px', fontSize: '13px', boxSizing: 'border-box' }} />
              </div>
              <div>
                <label style={{ fontSize: '12px', fontWeight: 'bold', display: 'block', marginBottom: '4px' }}>Min Order Value (₹)</label>
                <input name="min_order_value" type="number" min="0" step="0.01" value={form.min_order_value} onChange={handleFormChange} placeholder="Optional"
                  style={{ width: '100%', padding: '8px 10px', border: '1px solid #ddd', borderRadius: '4px', fontSize: '13px', boxSizing: 'border-box' }} />
              </div>
              {form.discount_type === 'percentage' && (
                <div>
                  <label style={{ fontSize: '12px', fontWeight: 'bold', display: 'block', marginBottom: '4px' }}>Max Discount Cap (₹)</label>
                  <input name="max_discount" type="number" min="0" step="0.01" value={form.max_discount} onChange={handleFormChange} placeholder="Optional"
                    style={{ width: '100%', padding: '8px 10px', border: '1px solid #ddd', borderRadius: '4px', fontSize: '13px', boxSizing: 'border-box' }} />
                </div>
              )}
              <div>
                <label style={{ fontSize: '12px', fontWeight: 'bold', display: 'block', marginBottom: '4px' }}>Total Usage Limit</label>
                <input name="usage_limit" type="number" min="1" value={form.usage_limit} onChange={handleFormChange} placeholder="Unlimited"
                  style={{ width: '100%', padding: '8px 10px', border: '1px solid #ddd', borderRadius: '4px', fontSize: '13px', boxSizing: 'border-box' }} />
              </div>
              <div>
                <label style={{ fontSize: '12px', fontWeight: 'bold', display: 'block', marginBottom: '4px' }}>Per-User Limit</label>
                <input name="per_user_limit" type="number" min="1" value={form.per_user_limit} onChange={handleFormChange}
                  style={{ width: '100%', padding: '8px 10px', border: '1px solid #ddd', borderRadius: '4px', fontSize: '13px', boxSizing: 'border-box' }} />
              </div>
              <div>
                <label style={{ fontSize: '12px', fontWeight: 'bold', display: 'block', marginBottom: '4px' }}>Start Date</label>
                <input name="start_date" type="datetime-local" value={form.start_date} onChange={handleFormChange}
                  style={{ width: '100%', padding: '8px 10px', border: '1px solid #ddd', borderRadius: '4px', fontSize: '13px', boxSizing: 'border-box' }} />
              </div>
              <div>
                <label style={{ fontSize: '12px', fontWeight: 'bold', display: 'block', marginBottom: '4px' }}>End Date</label>
                <input name="end_date" type="datetime-local" value={form.end_date} onChange={handleFormChange}
                  style={{ width: '100%', padding: '8px 10px', border: '1px solid #ddd', borderRadius: '4px', fontSize: '13px', boxSizing: 'border-box' }} />
              </div>
              <div style={{ gridColumn: '1 / -1', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <input type="checkbox" name="is_active" id="is_active" checked={form.is_active} onChange={handleFormChange} />
                <label htmlFor="is_active" style={{ fontSize: '13px', cursor: 'pointer' }}>Active immediately</label>
              </div>
            </div>
            <div style={{ display: 'flex', gap: '12px', marginTop: '20px' }}>
              <button type="submit" disabled={saving}
                style={{ background: '#007600', color: 'white', padding: '10px 24px', borderRadius: '4px', fontWeight: 'bold', fontSize: '13px', border: 'none', cursor: 'pointer', opacity: saving ? 0.7 : 1 }}>
                {saving ? 'Creating...' : 'Create Promotion'}
              </button>
              <button type="button" onClick={() => setShowForm(false)}
                style={{ background: '#f0f0f0', color: '#333', padding: '10px 24px', borderRadius: '4px', fontWeight: 'bold', fontSize: '13px', border: 'none', cursor: 'pointer' }}>
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Table */}
      <div style={{ background: '#fff', borderRadius: '4px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)', overflowX: 'auto' }}>
        {loading ? (
          <p style={{ padding: '32px', textAlign: 'center', color: '#888' }}>Loading...</p>
        ) : filtered.length === 0 ? (
          <p style={{ padding: '32px', textAlign: 'center', color: '#888' }}>No promotions found.</p>
        ) : (
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ borderBottom: '2px solid #f0f0f0', background: '#fafafa' }}>
                {['Code', 'Description', 'Discount', 'Min Order', 'Usage', 'Valid Until', 'Status', 'Actions'].map(h => (
                  <th key={h} style={{ padding: '12px 16px', textAlign: 'left', fontSize: '12px', fontWeight: 'bold', color: '#555', whiteSpace: 'nowrap' }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {filtered.map(p => {
                const expired = isExpired(p);
                return (
                  <tr key={p.id} style={{ borderBottom: '1px solid #f0f0f0' }}>
                    <td style={{ padding: '12px 16px', fontSize: '13px', fontWeight: 'bold', fontFamily: 'monospace' }}>{p.code}</td>
                    <td style={{ padding: '12px 16px', fontSize: '12px', color: '#555', maxWidth: '180px' }}>{p.description || '—'}</td>
                    <td style={{ padding: '12px 16px', fontSize: '13px', whiteSpace: 'nowrap' }}>
                      {p.discount_type === 'percentage'
                        ? `${p.discount_value}%${p.max_discount ? ` (max ₹${p.max_discount})` : ''}`
                        : `₹${p.discount_value}`}
                    </td>
                    <td style={{ padding: '12px 16px', fontSize: '12px' }}>{p.min_order_value ? `₹${p.min_order_value}` : '—'}</td>
                    <td style={{ padding: '12px 16px', fontSize: '12px', whiteSpace: 'nowrap' }}>
                      {p.used_count}{p.usage_limit ? `/${p.usage_limit}` : ''} uses
                    </td>
                    <td style={{ padding: '12px 16px', fontSize: '12px', whiteSpace: 'nowrap' }}>{fmt(p.end_date)}</td>
                    <td style={{ padding: '12px 16px' }}>
                      <span style={{
                        fontSize: '11px', padding: '3px 8px', borderRadius: '12px', fontWeight: 'bold',
                        background: expired ? '#f5f5f5' : '#e6f4ea',
                        color: expired ? '#888' : '#007600'
                      }}>
                        {expired ? 'Inactive' : 'Active'}
                      </span>
                    </td>
                    <td style={{ padding: '12px 16px' }}>
                      {expired ? (
                        <button
                          onClick={() => handleReactivate(p.id)}
                          style={{ fontSize: '12px', padding: '4px 10px', border: '1px solid #007600', borderRadius: '4px', background: 'none', color: '#007600', cursor: 'pointer' }}
                        >
                          Reactivate
                        </button>
                      ) : (
                        <button
                          onClick={() => handleDeactivate(p.id)}
                          style={{ fontSize: '12px', padding: '4px 10px', border: '1px solid #B12704', borderRadius: '4px', background: 'none', color: '#B12704', cursor: 'pointer' }}
                        >
                          Deactivate
                        </button>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
