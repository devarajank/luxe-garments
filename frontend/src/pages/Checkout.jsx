import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useCart } from '../context/CartContext';
import { useAuth } from '../context/AuthContext';

const inp = {
  padding: '10px 12px', border: '1.5px solid var(--border)', borderRadius: 'var(--radius-sm)',
  fontSize: '13px', width: '100%', boxSizing: 'border-box', outline: 'none',
  fontFamily: 'inherit', color: 'var(--text)',
};

function cardType(num) {
  const n = num.replace(/\s/g, '');
  if (/^4/.test(n)) return 'Visa';
  if (/^5[1-5]/.test(n)) return 'Mastercard';
  if (/^6/.test(n)) return 'RuPay';
  if (/^3[47]/.test(n)) return 'Amex';
  return null;
}

function cardIcon(type) {
  const icons = { Visa: '💳', Mastercard: '💳', RuPay: '💳', Amex: '💳' };
  const labels = { Visa: 'VISA', Mastercard: 'MC', RuPay: 'RuPay', Amex: 'AMEX' };
  if (!type) return null;
  return (
    <span style={{ fontSize: '11px', fontWeight: 800, color: 'var(--teal)', background: 'var(--teal-lt)', padding: '2px 6px', borderRadius: '4px' }}>
      {labels[type]}
    </span>
  );
}

function formatCardNumber(val) {
  return val.replace(/\D/g, '').slice(0, 16).replace(/(.{4})/g, '$1 ').trim();
}

function formatExpiry(val) {
  const digits = val.replace(/\D/g, '').slice(0, 4);
  if (digits.length >= 3) return digits.slice(0, 2) + '/' + digits.slice(2);
  return digits;
}

export default function Checkout() {
  const [orderPlaced, setOrderPlaced] = useState(false);
  const [orderId, setOrderId] = useState(null);
  const [placing, setPlacing] = useState(false);

  const [formData, setFormData] = useState({
    fullName: '', email: '', phone: '', address: '', city: '', pincode: '',
    paymentMethod: 'card',
  });

  // Card fields
  const [card, setCard] = useState({ number: '', name: '', expiry: '', cvv: '', showCvv: false });
  // UPI fields
  const [upi, setUpi] = useState({ id: '' });
  // Wallet fields
  const [wallet, setWallet] = useState({ provider: 'paytm', mobile: '' });

  const [couponCode, setCouponCode] = useState('');
  const [couponStatus, setCouponStatus] = useState('idle');
  const [discount, setDiscount] = useState(0);
  const [couponMsg, setCouponMsg] = useState('');
  const [appliedCode, setAppliedCode] = useState(null);

  const [payError, setPayError] = useState('');

  const navigate = useNavigate();
  const { getCartTotal, cart, clearCart } = useCart();
  const { user, token } = useAuth();
  const cartTotal = getCartTotal();
  const finalTotal = Math.max(0, cartTotal - discount);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleApplyCoupon = async () => {
    if (!couponCode.trim()) return;
    setCouponStatus('loading'); setCouponMsg('');
    try {
      const res = await fetch('/api/promotions/validate', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          code: couponCode.trim().toUpperCase(), cart_total: cartTotal,
          user_id: user?.id || null,
          cart_items: cart.map(i => ({ product_id: i.id, category: i.category || null, quantity: i.qty, price: i.price }))
        })
      });
      const data = await res.json();
      if (data.valid) {
        setCouponStatus('valid'); setDiscount(data.discount_amount);
        setAppliedCode(data.code); setCouponMsg(data.message || 'Coupon applied!');
      } else {
        setCouponStatus('invalid'); setDiscount(0); setAppliedCode(null);
        setCouponMsg(data.message || 'Invalid coupon code');
      }
    } catch { setCouponStatus('invalid'); setCouponMsg('Could not validate. Try again.'); }
  };

  const handleRemoveCoupon = () => {
    setCouponCode(''); setCouponStatus('idle'); setDiscount(0); setAppliedCode(null); setCouponMsg('');
  };

  const validatePayment = () => {
    const m = formData.paymentMethod;
    if (m === 'card') {
      const num = card.number.replace(/\s/g, '');
      if (num.length < 16) return 'Enter a valid 16-digit card number';
      if (!card.name.trim()) return 'Enter the cardholder name';
      if (card.expiry.length < 5) return 'Enter a valid expiry date (MM/YY)';
      const [mm, yy] = card.expiry.split('/');
      const now = new Date(); const expMonth = parseInt(mm, 10); const expYear = 2000 + parseInt(yy, 10);
      if (expMonth < 1 || expMonth > 12) return 'Invalid expiry month';
      if (expYear < now.getFullYear() || (expYear === now.getFullYear() && expMonth < now.getMonth() + 1)) return 'Card has expired';
      if (card.cvv.length < 3) return 'Enter a valid CVV';
    }
    if (m === 'upi') {
      if (!upi.id.includes('@') || upi.id.length < 5) return 'Enter a valid UPI ID (e.g. name@upi)';
    }
    if (m === 'wallet') {
      if (!/^\d{10}$/.test(wallet.mobile)) return 'Enter a valid 10-digit mobile number';
    }
    return null;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setPayError('');
    const err = validatePayment();
    if (err) { setPayError(err); return; }

    if (cart.length === 0) { alert('Your cart is empty'); return; }
    setPlacing(true);

    try {
      const res = await fetch('/api/orders/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
          ...(user?.id ? { 'x-user-id': user.id } : {}),
        },
        body: JSON.stringify({
          shipping_address: { line1: formData.address, line2: '', city: formData.city, state: 'Unknown', zip_code: formData.pincode, country: 'IN' },
          promotion_code: appliedCode || null,
          items: cart.map(i => ({ product_id: i.id, product_name: i.name, price: i.price, quantity: i.qty, size: i.size || '', color: i.color || '' }))
        })
      });
      const data = await res.json();
      if (res.ok) { clearCart(); setOrderId(data.id || 'ORD-' + Date.now()); setOrderPlaced(true); }
      else alert('Error: ' + (data.detail || JSON.stringify(data)));
    } catch (err) { alert('Error: ' + (err?.message || String(err))); }
    finally { setPlacing(false); }
  };

  if (orderPlaced) {
    return (
      <div style={{ minHeight: '100vh', background: 'var(--bg)', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '24px' }}>
        <div className="section" style={{ textAlign: 'center', padding: '48px', maxWidth: '500px' }}>
          <div style={{ width: '72px', height: '72px', borderRadius: '50%', background: '#F0FDF4', border: '2px solid #86EFAC', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 20px', fontSize: '32px' }}>✓</div>
          <h1 style={{ fontSize: '26px', fontWeight: 800, marginBottom: '10px', color: 'var(--dark)' }}>Order Confirmed!</h1>
          <p style={{ color: 'var(--text-2)', marginBottom: '8px' }}>Your order has been placed successfully</p>
          <p style={{ fontSize: '18px', fontWeight: 700, color: 'var(--primary)', marginBottom: '12px' }}>Order ID: {orderId}</p>
          {discount > 0 && <p style={{ color: '#16A34A', fontWeight: 600, marginBottom: '8px', fontSize: '13px' }}>You saved ₹{discount.toFixed(2)} with {appliedCode}!</p>}
          <p style={{ color: 'var(--text-2)', marginBottom: '24px', fontSize: '13px' }}>A confirmation will be sent to {formData.email}</p>
          <p style={{ fontSize: '12px', color: 'var(--text-3)', marginBottom: '24px' }}>Estimated delivery: 3–5 business days</p>
          <Link to="/"><button style={{ background: 'var(--primary)', color: '#fff', padding: '12px 28px', borderRadius: 'var(--radius-sm)', fontWeight: 700, border: 'none', cursor: 'pointer', fontSize: '14px' }}>Continue Shopping</button></Link>
        </div>
      </div>
    );
  }

  const method = formData.paymentMethod;
  const ctype = cardType(card.number);

  return (
    <div style={{ minHeight: '100vh', background: 'var(--bg)' }}>
      <div className="main-content">
        <div className="content-max-width">
          <h1 style={{ fontSize: '22px', fontWeight: 800, marginBottom: '24px', color: 'var(--dark)' }}>Checkout</h1>

          <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '20px' }}>
            <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>

              {/* ── Delivery Address ── */}
              <div className="section">
                <h2 style={{ fontSize: '14px', fontWeight: 700, marginBottom: '16px', color: 'var(--dark)', textTransform: 'uppercase', letterSpacing: '0.5px' }}>1 · Delivery Address</h2>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
                  <input style={{ ...inp, gridColumn: '1/-1' }} name="fullName" placeholder="Full Name" value={formData.fullName} onChange={handleChange} required />
                  <input style={inp} type="email" name="email" placeholder="Email" value={formData.email} onChange={handleChange} required />
                  <input style={inp} type="tel" name="phone" placeholder="Phone Number" value={formData.phone} onChange={handleChange} required />
                  <textarea style={{ ...inp, gridColumn: '1/-1', resize: 'none' }} name="address" placeholder="Street Address" value={formData.address} onChange={handleChange} required rows={2} />
                  <input style={inp} name="city" placeholder="City" value={formData.city} onChange={handleChange} required />
                  <input style={inp} name="pincode" placeholder="Pincode" value={formData.pincode} onChange={handleChange} required />
                </div>
              </div>

              {/* ── Payment Method ── */}
              <div className="section">
                <h2 style={{ fontSize: '14px', fontWeight: 700, marginBottom: '16px', color: 'var(--dark)', textTransform: 'uppercase', letterSpacing: '0.5px' }}>2 · Payment Method</h2>

                {/* Method selector */}
                <div style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>
                  {[
                    { val: 'card',   label: '💳 Card' },
                    { val: 'upi',    label: '📱 UPI' },
                    { val: 'wallet', label: '🏦 Wallet' },
                  ].map(({ val, label }) => (
                    <label
                      key={val}
                      style={{
                        flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center',
                        padding: '10px', borderRadius: 'var(--radius-sm)', cursor: 'pointer',
                        border: method === val ? '2px solid var(--primary)' : '2px solid var(--border)',
                        background: method === val ? 'var(--primary-lt)' : 'var(--bg)',
                        fontWeight: method === val ? 700 : 500, fontSize: '13px',
                        color: method === val ? 'var(--primary)' : 'var(--text-2)',
                        transition: 'all 0.15s',
                      }}
                    >
                      <input type="radio" name="paymentMethod" value={val} checked={method === val} onChange={handleChange} style={{ display: 'none' }} />
                      {label}
                    </label>
                  ))}
                </div>

                {/* ── Card fields ── */}
                {method === 'card' && (
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                    {/* Card number */}
                    <div style={{ position: 'relative' }}>
                      <input
                        style={{ ...inp, letterSpacing: '2px', paddingRight: '80px' }}
                        placeholder="Card Number"
                        value={card.number}
                        onChange={e => setCard(c => ({ ...c, number: formatCardNumber(e.target.value) }))}
                        required
                        maxLength={19}
                        inputMode="numeric"
                      />
                      {ctype && <span style={{ position: 'absolute', right: '10px', top: '50%', transform: 'translateY(-50%)' }}>{cardIcon(ctype)}</span>}
                    </div>
                    <input
                      style={inp}
                      placeholder="Cardholder Name"
                      value={card.name}
                      onChange={e => setCard(c => ({ ...c, name: e.target.value }))}
                      required
                    />
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
                      <input
                        style={inp}
                        placeholder="MM/YY"
                        value={card.expiry}
                        onChange={e => setCard(c => ({ ...c, expiry: formatExpiry(e.target.value) }))}
                        required
                        maxLength={5}
                        inputMode="numeric"
                      />
                      <div style={{ position: 'relative' }}>
                        <input
                          style={{ ...inp, letterSpacing: '4px' }}
                          placeholder="CVV"
                          type={card.showCvv ? 'text' : 'password'}
                          value={card.cvv}
                          onChange={e => setCard(c => ({ ...c, cvv: e.target.value.replace(/\D/g, '').slice(0, 4) }))}
                          required
                          maxLength={4}
                          inputMode="numeric"
                        />
                        <button
                          type="button"
                          onClick={() => setCard(c => ({ ...c, showCvv: !c.showCvv }))}
                          style={{ position: 'absolute', right: '10px', top: '50%', transform: 'translateY(-50%)', background: 'none', border: 'none', cursor: 'pointer', fontSize: '14px', color: 'var(--text-3)' }}
                        >
                          {card.showCvv ? '🙈' : '👁'}
                        </button>
                      </div>
                    </div>
                    {/* Sample card hint */}
                    <div style={{ background: 'var(--teal-lt)', border: '1px solid #BAE6FD', borderRadius: 'var(--radius-sm)', padding: '10px 12px', fontSize: '12px', color: 'var(--text-2)' }}>
                      <strong>Demo card:</strong> 4111 1111 1111 1111 · Any future date · Any 3-digit CVV
                    </div>
                  </div>
                )}

                {/* ── UPI fields ── */}
                {method === 'upi' && (
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                    {/* Quick-select UPI apps */}
                    <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                      {[
                        { id: 'phonepe', label: 'PhonePe',   suffix: '@ybl',    bg: '#EDE7F6', color: '#5E35B1' },
                        { id: 'gpay',    label: 'Google Pay', suffix: '@oksbi',  bg: '#E3F2FD', color: '#1565C0' },
                        { id: 'paytm',   label: 'Paytm',     suffix: '@paytm',  bg: '#E3F9F5', color: '#00BAA3' },
                        { id: 'bhim',    label: 'BHIM',      suffix: '@upi',    bg: '#FFF3E0', color: '#E65100' },
                      ].map(app => (
                        <button
                          key={app.id}
                          type="button"
                          onClick={() => setUpi({ id: (formData.phone || 'yourname') + app.suffix })}
                          style={{
                            padding: '7px 14px', borderRadius: 'var(--radius-sm)', border: '1.5px solid transparent',
                            background: app.bg, color: app.color, fontWeight: 700, fontSize: '12px', cursor: 'pointer',
                          }}
                        >
                          {app.label}
                        </button>
                      ))}
                    </div>
                    <div style={{ position: 'relative' }}>
                      <input
                        style={inp}
                        placeholder="Enter UPI ID (e.g. name@ybl)"
                        value={upi.id}
                        onChange={e => setUpi({ id: e.target.value })}
                        required
                      />
                      {upi.id.includes('@') && (
                        <span style={{ position: 'absolute', right: '10px', top: '50%', transform: 'translateY(-50%)', fontSize: '16px' }}>✓</span>
                      )}
                    </div>
                    <div style={{ background: 'var(--teal-lt)', border: '1px solid #BAE6FD', borderRadius: 'var(--radius-sm)', padding: '10px 12px', fontSize: '12px', color: 'var(--text-2)' }}>
                      <strong>Demo:</strong> Click any app above to autofill a sample UPI ID.
                    </div>
                  </div>
                )}

                {/* ── Wallet fields ── */}
                {method === 'wallet' && (
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                    {/* Wallet provider */}
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
                      {[
                        { id: 'paytm',   label: 'Paytm',        emoji: '🟦', bal: '₹2,450' },
                        { id: 'phonepe', label: 'PhonePe',       emoji: '🟣', bal: '₹1,200' },
                        { id: 'gpay',    label: 'Google Pay',    emoji: '🔵', bal: '₹850'   },
                        { id: 'amazon',  label: 'Amazon Pay',    emoji: '🟠', bal: '₹300'   },
                      ].map(w => (
                        <label
                          key={w.id}
                          style={{
                            display: 'flex', alignItems: 'center', gap: '10px', padding: '12px',
                            borderRadius: 'var(--radius-sm)', cursor: 'pointer',
                            border: wallet.provider === w.id ? '2px solid var(--primary)' : '2px solid var(--border)',
                            background: wallet.provider === w.id ? 'var(--primary-lt)' : '#fff',
                            transition: 'all 0.15s',
                          }}
                        >
                          <input type="radio" name="walletProvider" value={w.id} checked={wallet.provider === w.id} onChange={() => setWallet(wl => ({ ...wl, provider: w.id }))} style={{ display: 'none' }} />
                          <span style={{ fontSize: '20px' }}>{w.emoji}</span>
                          <div>
                            <div style={{ fontWeight: 700, fontSize: '13px' }}>{w.label}</div>
                            <div style={{ fontSize: '11px', color: 'var(--text-3)' }}>Balance: {w.bal}</div>
                          </div>
                        </label>
                      ))}
                    </div>
                    <input
                      style={inp}
                      type="tel"
                      placeholder="Registered mobile number"
                      value={wallet.mobile}
                      onChange={e => setWallet(wl => ({ ...wl, mobile: e.target.value.replace(/\D/g, '').slice(0, 10) }))}
                      required
                      maxLength={10}
                      inputMode="numeric"
                    />
                    <div style={{ background: 'var(--teal-lt)', border: '1px solid #BAE6FD', borderRadius: 'var(--radius-sm)', padding: '10px 12px', fontSize: '12px', color: 'var(--text-2)' }}>
                      <strong>Demo:</strong> Enter any 10-digit mobile number to proceed.
                    </div>
                  </div>
                )}

                {payError && (
                  <div style={{ marginTop: '12px', background: 'var(--primary-lt)', border: '1px solid #FECACA', borderRadius: 'var(--radius-sm)', padding: '10px 12px', fontSize: '13px', color: 'var(--primary)', fontWeight: 600 }}>
                    ⚠ {payError}
                  </div>
                )}

                <p style={{ fontSize: '11px', color: 'var(--text-3)', marginTop: '14px' }}>🔒 This is a demo. No real payment is processed.</p>
              </div>

              <button
                type="submit"
                disabled={placing}
                style={{
                  background: placing ? '#9CA3AF' : 'var(--primary)', color: '#fff',
                  padding: '14px', borderRadius: 'var(--radius-sm)', fontWeight: 700,
                  fontSize: '14px', border: 'none', cursor: placing ? 'not-allowed' : 'pointer',
                  transition: 'background 0.2s', letterSpacing: '0.3px',
                }}
              >
                {placing ? 'Placing Order…' : `Place Order${discount > 0 ? ` — Pay ₹${finalTotal.toFixed(2)}` : ''}`}
              </button>
            </form>

            {/* Right column */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              {/* Promo */}
              <div className="section">
                <h3 style={{ fontSize: '13px', fontWeight: 700, marginBottom: '12px', color: 'var(--dark)', textTransform: 'uppercase', letterSpacing: '0.5px' }}>🏷️ Promo Code</h3>
                {couponStatus === 'valid' ? (
                  <div>
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', background: '#F0FDF4', border: '1.5px solid #86EFAC', borderRadius: 'var(--radius-sm)', padding: '10px 12px' }}>
                      <div>
                        <span style={{ fontWeight: 700, fontSize: '13px', color: '#16A34A' }}>{appliedCode}</span>
                        <span style={{ fontSize: '12px', color: 'var(--text-2)', marginLeft: '8px' }}>−₹{discount.toFixed(2)}</span>
                      </div>
                      <button onClick={handleRemoveCoupon} style={{ background: 'none', border: 'none', cursor: 'pointer', color: 'var(--primary)', fontSize: '20px', lineHeight: 1, padding: '0 4px' }}>×</button>
                    </div>
                    <p style={{ fontSize: '11px', color: '#16A34A', marginTop: '6px' }}>{couponMsg}</p>
                  </div>
                ) : (
                  <div>
                    <div style={{ display: 'flex', gap: '8px' }}>
                      <input
                        type="text" value={couponCode}
                        onChange={e => { setCouponCode(e.target.value); if (couponStatus !== 'idle') { setCouponStatus('idle'); setCouponMsg(''); } }}
                        placeholder="Coupon code"
                        onKeyDown={e => e.key === 'Enter' && (e.preventDefault(), handleApplyCoupon())}
                        style={{ ...inp, textTransform: 'uppercase', border: couponStatus === 'invalid' ? '1.5px solid var(--primary)' : '1.5px solid var(--border)' }}
                      />
                      <button type="button" onClick={handleApplyCoupon} disabled={couponStatus === 'loading' || !couponCode.trim()}
                        style={{ background: 'var(--primary)', color: '#fff', padding: '9px 14px', borderRadius: 'var(--radius-sm)', fontWeight: 700, fontSize: '12px', border: 'none', cursor: 'pointer', whiteSpace: 'nowrap', opacity: couponStatus === 'loading' ? 0.6 : 1 }}>
                        {couponStatus === 'loading' ? '…' : 'Apply'}
                      </button>
                    </div>
                    {couponMsg && <p style={{ fontSize: '11px', marginTop: '6px', color: couponStatus === 'invalid' ? 'var(--primary)' : '#16A34A' }}>{couponMsg}</p>}
                    <p style={{ fontSize: '11px', color: 'var(--text-3)', marginTop: '6px' }}>Try: WELCOME10 · SUMMER25 · FLAT20</p>
                  </div>
                )}
              </div>

              {/* Order summary */}
              <div className="section" style={{ position: 'sticky', top: '100px' }}>
                <h3 style={{ fontSize: '13px', fontWeight: 700, marginBottom: '16px', color: 'var(--dark)', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Order Summary</h3>
                <div style={{ fontSize: '13px', marginBottom: '14px', paddingBottom: '14px', borderBottom: '1.5px solid var(--border)', display: 'flex', flexDirection: 'column', gap: '8px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span style={{ color: 'var(--text-2)' }}>Subtotal</span>
                    <span>₹{(cartTotal * 0.847).toFixed(2)}</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span style={{ color: 'var(--text-2)' }}>Taxes (18%)</span>
                    <span>₹{(cartTotal * 0.153).toFixed(2)}</span>
                  </div>
                  {discount > 0 && (
                    <div style={{ display: 'flex', justifyContent: 'space-between', color: '#16A34A', fontWeight: 600 }}>
                      <span>Discount ({appliedCode})</span>
                      <span>−₹{discount.toFixed(2)}</span>
                    </div>
                  )}
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span style={{ color: 'var(--text-2)' }}>Delivery</span>
                    <span style={{ color: '#16A34A', fontWeight: 700 }}>FREE</span>
                  </div>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontWeight: 800, fontSize: '16px', color: 'var(--dark)' }}>
                  <span>Total</span>
                  <span style={{ color: 'var(--primary)' }}>₹{finalTotal.toFixed(2)}</span>
                </div>
                {discount > 0 && <p style={{ fontSize: '11px', color: '#16A34A', marginTop: '8px', textAlign: 'right', fontWeight: 600 }}>You save ₹{discount.toFixed(2)}!</p>}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
