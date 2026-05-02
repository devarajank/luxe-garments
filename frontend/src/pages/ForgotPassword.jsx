import { useState } from 'react';
import { Link } from 'react-router-dom';

export default function ForgotPassword() {
  const [email, setEmail] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const res = await fetch('/api/users/forgot-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email }),
      });
      if (!res.ok) throw new Error('Something went wrong. Please try again.');
      setSubmitted(true);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      minHeight: 'calc(100vh - 120px)',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'flex-start',
      paddingTop: '48px',
      background: '#f3f3f3',
    }}>
      <div style={{
        background: '#fff',
        border: '1px solid #ddd',
        borderRadius: '8px',
        padding: '24px 32px',
        width: '100%',
        maxWidth: '380px',
      }}>
        <h2 style={{ fontSize: '28px', fontWeight: '400', marginBottom: '6px', color: '#111' }}>
          Forgot password
        </h2>
        <p style={{ fontSize: '13px', color: '#555', marginBottom: '16px' }}>
          Enter the email associated with your account and we'll send a reset link.
        </p>

        {submitted ? (
          <div style={{ fontSize: '14px', color: '#111' }}>
            <div style={{
              background: '#f0fff4',
              border: '1px solid #34a853',
              borderRadius: '4px',
              padding: '10px 14px',
              marginBottom: '16px',
              color: '#1a7a3a',
              fontSize: '13px',
            }}>
              If that email is registered, a reset link has been sent. Check your inbox.
            </div>
            <Link to="/login" style={linkStyle}>Back to sign in</Link>
          </div>
        ) : (
          <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            <div>
              <label style={labelStyle}>Email</label>
              <input
                type="email"
                value={email}
                onChange={e => { setEmail(e.target.value); setError(''); }}
                required
                autoFocus
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
              {loading ? 'Sending…' : 'Send reset link'}
            </button>

            <div style={{ textAlign: 'center', fontSize: '13px', marginTop: '4px' }}>
              <Link to="/login" style={linkStyle}>Back to sign in</Link>
            </div>
          </form>
        )}
      </div>
    </div>
  );
}

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
