import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Account() {
  const { user, token, updateUser } = useAuth();
  const navigate = useNavigate();

  const [profile, setProfile] = useState(null);
  const [loadError, setLoadError] = useState('');
  const [editing, setEditing] = useState(false);
  const [form, setForm] = useState({ first_name: '', last_name: '', phone: '' });
  const [saving, setSaving] = useState(false);
  const [saveMsg, setSaveMsg] = useState('');
  const fetchedRef = useRef(false);

  const authHeaders = () => ({
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`,
    'x-user-id': user?.id,
  });

  useEffect(() => {
    if (!user) { navigate('/login', { state: { from: '/account' } }); return; }
    if (fetchedRef.current) return;
    fetchedRef.current = true;
    fetch('/api/users/profile', { headers: authHeaders() })
      .then(r => { if (!r.ok) throw new Error('Failed to load profile'); return r.json(); })
      .then(data => {
        setProfile(data);
        setForm({ first_name: data.first_name || '', last_name: data.last_name || '', phone: data.phone || '' });
      })
      .catch(e => setLoadError(e.message));
  }, [user]);

  const handleSave = async () => {
    setSaving(true); setSaveMsg('');
    try {
      const res = await fetch('/api/users/profile', {
        method: 'PUT',
        headers: authHeaders(),
        body: JSON.stringify(form),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Update failed');
      setProfile(data);
      updateUser({ ...user, first_name: data.first_name, last_name: data.last_name, phone: data.phone });
      setEditing(false);
      setSaveMsg('Profile updated successfully.');
    } catch (e) {
      setSaveMsg(e.message);
    } finally {
      setSaving(false);
    }
  };

  if (loadError) return <div style={{ padding: '48px', textAlign: 'center', color: '#c00' }}>{loadError}</div>;
  if (!profile) return <div style={{ padding: '48px', textAlign: 'center', color: '#888' }}>Loading…</div>;

  return (
    <div style={{ maxWidth: '640px', margin: '0 auto', padding: '32px 16px' }}>
      <h1 style={{ fontSize: '22px', fontWeight: '400', marginBottom: '24px', color: '#111' }}>My Account</h1>

      {/* Profile card */}
      <div style={{ background: '#fff', border: '1px solid #ddd', borderRadius: '8px', padding: '24px', marginBottom: '20px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <h2 style={{ fontSize: '16px', fontWeight: '600', margin: 0 }}>Personal Information</h2>
          {!editing && (
            <button
              onClick={() => { setEditing(true); setSaveMsg(''); }}
              style={{ background: 'none', border: '1px solid #a6a6a6', borderRadius: '6px', padding: '6px 14px', cursor: 'pointer', fontSize: '13px' }}
            >
              Edit
            </button>
          )}
        </div>

        {editing ? (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
            <div style={{ display: 'flex', gap: '12px' }}>
              <div style={{ flex: 1 }}>
                <label style={labelStyle}>First Name</label>
                <input style={inputStyle} value={form.first_name} onChange={e => setForm(f => ({ ...f, first_name: e.target.value }))} />
              </div>
              <div style={{ flex: 1 }}>
                <label style={labelStyle}>Last Name</label>
                <input style={inputStyle} value={form.last_name} onChange={e => setForm(f => ({ ...f, last_name: e.target.value }))} />
              </div>
            </div>
            <div>
              <label style={labelStyle}>Phone</label>
              <input style={inputStyle} value={form.phone} onChange={e => setForm(f => ({ ...f, phone: e.target.value }))} placeholder="+91 XXXXX XXXXX" />
            </div>
            <div style={{ display: 'flex', gap: '8px', marginTop: '4px' }}>
              <button
                onClick={handleSave}
                disabled={saving}
                style={{ background: '#FFD814', border: '1px solid #FCD200', borderRadius: '6px', padding: '8px 20px', cursor: saving ? 'not-allowed' : 'pointer', fontWeight: '600', fontSize: '13px' }}
              >
                {saving ? 'Saving…' : 'Save Changes'}
              </button>
              <button
                onClick={() => { setEditing(false); setSaveMsg(''); setForm({ first_name: profile.first_name || '', last_name: profile.last_name || '', phone: profile.phone || '' }); }}
                style={{ background: '#fff', border: '1px solid #ddd', borderRadius: '6px', padding: '8px 20px', cursor: 'pointer', fontSize: '13px' }}
              >
                Cancel
              </button>
            </div>
          </div>
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', fontSize: '14px' }}>
            <Field label="First Name" value={profile.first_name || '—'} />
            <Field label="Last Name" value={profile.last_name || '—'} />
            <Field label="Email" value={profile.email} />
            <Field label="Phone" value={profile.phone || '—'} />
          </div>
        )}

        {saveMsg && (
          <div style={{ marginTop: '12px', fontSize: '13px', color: saveMsg.includes('success') ? '#007600' : '#c00' }}>
            {saveMsg}
          </div>
        )}
      </div>

      {/* Quick links */}
      <div style={{ background: '#fff', border: '1px solid #ddd', borderRadius: '8px', overflow: 'hidden' }}>
        {[
          { label: 'Your Orders', sub: 'Track, return, or buy again', path: '/orders', icon: '📦' },
          { label: 'Change Password', sub: 'Update your password', path: '/forgot-password', icon: '🔒' },
        ].map(({ label, sub, path, icon }) => (
          <div
            key={label}
            onClick={() => navigate(path)}
            style={{
              display: 'flex', alignItems: 'center', gap: '16px',
              padding: '16px 20px', cursor: 'pointer', borderBottom: '1px solid #f0f0f0',
            }}
            onMouseEnter={e => e.currentTarget.style.background = '#fafafa'}
            onMouseLeave={e => e.currentTarget.style.background = '#fff'}
          >
            <span style={{ fontSize: '24px' }}>{icon}</span>
            <div>
              <div style={{ fontSize: '14px', fontWeight: '600', color: '#111' }}>{label}</div>
              <div style={{ fontSize: '12px', color: '#888', marginTop: '2px' }}>{sub}</div>
            </div>
            <span style={{ marginLeft: 'auto', color: '#aaa', fontSize: '18px' }}>›</span>
          </div>
        ))}
      </div>
    </div>
  );
}

function Field({ label, value }) {
  return (
    <div>
      <div style={{ fontSize: '11px', color: '#888', marginBottom: '3px', textTransform: 'uppercase', letterSpacing: '0.5px' }}>{label}</div>
      <div style={{ color: '#111', fontWeight: '500' }}>{value}</div>
    </div>
  );
}

const labelStyle = { display: 'block', fontSize: '12px', color: '#555', marginBottom: '5px' };
const inputStyle = {
  width: '100%', padding: '9px 11px', border: '1px solid #a6a6a6',
  borderRadius: '4px', fontSize: '13px', boxSizing: 'border-box', outline: 'none',
};
