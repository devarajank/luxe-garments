import { Link, useNavigate } from 'react-router-dom';
import { useCart } from '../context/CartContext';

export default function Cart() {
  const navigate = useNavigate();
  const { cart, removeFromCart, updateQuantity } = useCart();

  const subtotal = cart.reduce((sum, item) => sum + (item.price * item.qty), 0);
  const tax = subtotal * 0.18;
  const total = subtotal + tax;

  return (
    <div style={{ minHeight: '100vh', background: '#EAEDED' }}>
      <div className="main-content">
        <div className="content-max-width">
          <h1 style={{ fontSize: '24px', fontWeight: 'bold', marginBottom: '20px' }}>Shopping Cart</h1>

          {cart.length === 0 ? (
            <div className="section" style={{ textAlign: 'center', padding: '48px' }}>
              <p style={{ fontSize: '16px', color: '#666', marginBottom: '16px' }}>Your cart is empty</p>
              <Link to="/" style={{ textDecoration: 'none' }}>
                <button style={{ background: '#FF9900', color: 'black', padding: '12px 24px', borderRadius: '4px', fontWeight: 'bold', border: 'none', cursor: 'pointer' }}>
                  Continue Shopping
                </button>
              </Link>
            </div>
          ) : (
            <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '20px' }}>
              {/* Cart Items */}
              <div className="section">
                <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                  {cart.map(item => (
                    <div key={item.id} style={{ display: 'grid', gridTemplateColumns: 'auto 1fr auto auto', gap: '16px', alignItems: 'center', paddingBottom: '12px', borderBottom: '1px solid #ddd' }}>
                      <div style={{ width: '80px', height: '80px', background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', borderRadius: '4px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '40px', overflow: 'hidden' }}>
                        {item.image_url ? (
                          <img
                            src={item.image_url}
                            alt={item.name}
                            style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                          />
                        ) : (
                          '👕'
                        )}
                      </div>
                      <div>
                        <h3 style={{ fontWeight: 'bold', marginBottom: '4px' }}>{item.name}</h3>
                        <p style={{ fontSize: '12px', color: '#666' }}>₹{item.price}</p>
                      </div>
                      <div style={{ display: 'flex', alignItems: 'center', border: '1px solid #ddd', borderRadius: '4px' }}>
                        <button onClick={() => updateQuantity(item.id, item.qty - 1)} style={{ padding: '6px 10px', border: 'none', background: 'none', cursor: 'pointer', fontSize: '14px' }}>−</button>
                        <span style={{ padding: '6px 12px', borderLeft: '1px solid #ddd', borderRight: '1px solid #ddd' }}>{item.qty}</span>
                        <button onClick={() => updateQuantity(item.id, item.qty + 1)} style={{ padding: '6px 10px', border: 'none', background: 'none', cursor: 'pointer', fontSize: '14px' }}>+</button>
                      </div>
                      <div style={{ textAlign: 'right' }}>
                        <p style={{ fontWeight: 'bold', marginBottom: '6px' }}>₹{(item.price * item.qty).toFixed(2)}</p>
                        <button onClick={() => removeFromCart(item.id)} style={{ color: '#B12704', fontSize: '12px', background: 'none', border: 'none', cursor: 'pointer', textDecoration: 'underline' }}>
                          Remove
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Order Summary */}
              <div className="section" style={{ height: 'fit-content', position: 'sticky', top: '100px' }}>
                <h3 style={{ fontSize: '16px', fontWeight: 'bold', marginBottom: '16px' }}>Order Summary</h3>
                <div style={{ fontSize: '13px', marginBottom: '16px', paddingBottom: '12px', borderBottom: '1px solid #ddd' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                    <span>Subtotal</span>
                    <span>₹{subtotal.toFixed(2)}</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                    <span>Taxes (18% GST)</span>
                    <span>₹{tax.toFixed(2)}</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span>Delivery</span>
                    <span style={{ color: '#007600', fontWeight: 'bold' }}>FREE</span>
                  </div>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontWeight: 'bold', fontSize: '16px', marginBottom: '16px' }}>
                  <span>Total</span>
                  <span>₹{total.toFixed(2)}</span>
                </div>
                <button onClick={() => navigate('/checkout')} style={{ width: '100%', background: '#FF9900', color: 'black', padding: '12px', borderRadius: '4px', fontWeight: 'bold', border: 'none', cursor: 'pointer', marginBottom: '8px' }}>
                  Proceed to Checkout
                </button>
                <Link to="/" style={{ textDecoration: 'none' }}>
                  <div style={{ textAlign: 'center', color: '#007185', fontSize: '12px', cursor: 'pointer' }}>
                    Continue Shopping
                  </div>
                </Link>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
