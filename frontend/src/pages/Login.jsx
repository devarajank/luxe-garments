import { useState } from 'react';
import { useNavigate, useLocation, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Login() {
  const [mode, setMode] = useState('login'); // 'login' | 'register'
  const [form, setForm] = useState({ email: '', password: '', first_name: '', last_name: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login, register } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const redirectTo = location.state?.from || '/';

  const handleChange = (e) => {
    setForm(prev => ({ ...prev, [e.target.name]: e.target.value }));
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      if (mode === 'login') {
        await login(form.email, form.password);
      } else {
        if (!form.first_name.trim() || !form.last_name.trim()) {
          setError('First and last name are required.');
          setLoading(false);
          return;
        }
        await register(form.email, form.password, form.first_name, form.last_name);
      }
      navigate(redirectTo, { replace: true });
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
          {mode === 'login' ? 'Sign in' : 'Create account'}
        </h2>

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          {mode === 'register' && (
            <div style={{ display: 'flex', gap: '8px' }}>
              <div style={{ flex: 1 }}>
                <label style={labelStyle}>First name</label>
                <input
                  name="first_name"
                  value={form.first_name}
                  onChange={handleChange}
                  required
                  style={inputStyle}
                />
              </div>
              <div style={{ flex: 1 }}>
                <label style={labelStyle}>Last name</label>
                <input
                  name="last_name"
                  value={form.last_name}
                  onChange={handleChange}
                  required
                  style={inputStyle}
                />
              </div>
            </div>
          )}

          <div>
            <label style={labelStyle}>Email</label>
            <input
              type="email"
              name="email"
              value={form.email}
              onChange={handleChange}
              required
              autoFocus
              style={inputStyle}
            />
          </div>

          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline' }}>
              <label style={labelStyle}>Password</label>
              {mode === 'login' && (
                <Link to="/forgot-password" style={{ ...linkBtnStyle, fontSize: '12px', textDecoration: 'none', color: '#0066c0' }}>
                  Forgot password?
                </Link>
              )}
            </div>
            <input
              type="password"
              name="password"
              value={form.password}
              onChange={handleChange}
              required
              minLength={6}
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
            {loading ? 'Please wait…' : mode === 'login' ? 'Sign in' : 'Create your account'}
          </button>
        </form>

        <div style={{ marginTop: '16px', paddingTop: '16px', borderTop: '1px solid #e7e7e7', textAlign: 'center', fontSize: '13px' }}>
          {mode === 'login' ? (
            <>
              New to Luxe?{' '}
              <button onClick={() => { setMode('register'); setError(''); }} style={linkBtnStyle}>
                Create an account
              </button>
            </>
          ) : (
            <>
              Already have an account?{' '}
              <button onClick={() => { setMode('login'); setError(''); }} style={linkBtnStyle}>
                Sign in
              </button>
            </>
          )}
        </div>
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

const linkBtnStyle = {
  background: 'none',
  border: 'none',
  color: '#0066c0',
  cursor: 'pointer',
  fontSize: '13px',
  padding: 0,
  textDecoration: 'underline',
};
