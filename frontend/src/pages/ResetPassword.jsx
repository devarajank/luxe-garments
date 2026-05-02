import { useState } from 'react';
import { useSearchParams, useNavigate, Link } from 'react-router-dom';

export default function ResetPassword() {
  const [searchParams] = useSearchParams();
  const token = searchParams.get('token') || '';
  const [form, setForm] = useState({ password: '', confirm: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setForm(prev => ({ ...prev, [e.target.name]: e.target.value }));
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (form.password !== form.confirm) {
      setError('Passwords do not match.');
      return;
    }
    if (form.password.length < 6) {
      setError('Password must be at least 6 characters.');
      return;
    }
    setLoading(true);
    try {
      const res = await fetch('/api/users/reset-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token, new_password: form.password }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Reset failed.');
      setSuccess(true);
      setTimeout(() => navigate('/login'), 2500);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (!token) {
    return (
      <div style={outerStyle}>
        <div style={cardStyle}>
          <p style={{ color: '#c00', fontSize: '14px' }}>Invalid or missing reset token.</p>
          <Link to="/login" style={linkStyle}>Back to sign in</Link>
        </div>
      </div>
    );
  }

  return (
    <div style={outerStyle}>
      <div style={cardStyle}>
        <h2 style={{ fontSize: '28px', fontWeight: '400', marginBottom: '6px', color: '#111' }}>
          Set new password
        </h2>

        {success ? (
          <div style={{
            background: '#f0fff4',
            border: '1px solid #34a853',
            borderRadius: '4px',
            padding: '10px 14px',
            color: '#1a7a3a',
            fontSize: '13px',
          }}>
            Password updated! Redirecting to sign in…
          </div>
        ) : (
          <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginTop: '12px' }}>
            <div>
              <label style={labelStyle}>New password</label>
              <input
                type="password"
                name="password"
                value={form.password}
                onChange={handleChange}
                required
                minLength={6}
                autoFocus
                style={inputStyle}
              />
            </div>

            <div>
              <label style={labelStyle}>Confirm password</label>
              <input
                type="password"
                name="confirm"
                value={form.confirm}
                onChange={handleChange}
                required
                style={inputStyle}
              />
            </div>

            {error && (
              <div style={{
                background: '#fff8f8',
                border: '1px solid #c00',
                borderRadius: '4px',
                padding: '8px 12px',
                color: '#c00',
                fontSize: '13px',
              }}>
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              style={{
                background: loading ? '#f0c040' : '#FFD814',
                border: '1px solid #FCD200',
                borderRadius: '8px',
                padding: '9px 10px',
                fontSize: '14px',
                fontWeight: '500',
                cursor: loading ? 'not-allowed' : 'pointer',
                width: '100%',
                marginTop: '4px',
              }}
            >
              {loading ? 'Saving…' : 'Save new password'}
            </button>
          </form>
        )}
      </div>
    </div>
  );
}

const outerStyle = {
  minHeight: 'calc(100vh - 120px)',
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'flex-start',
  paddingTop: '48px',
  background: '#f3f3f3',
};

const cardStyle = {
  background: '#fff',
  border: '1px solid #ddd',
  borderRadius: '8px',
  padding: '24px 32px',
  width: '100%',
  maxWidth: '380px',
};

const labelStyle = {
  display: 'block',
  fontSize: '13px',
  fontWeight: '700',
  marginBottom: '4px',
  color: '#111',
};

const inputStyle = {
  width: '100%',
  padding: '7px 10px',
  border: '1px solid #a6a6a6',
  borderRadius: '4px',
  fontSize: '13px',
  boxSizing: 'border-box',
  outline: 'none',
};

const linkStyle = {
  color: '#0066c0',
  fontSize: '13px',
  textDecoration: 'underline',
};
