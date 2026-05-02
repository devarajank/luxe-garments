import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useCart } from '../context/CartContext';

export default function ProductDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { addToCart } = useCart();
  const [product, setProduct] = useState(null);
  const [quantity, setQuantity] = useState(1);
  const [added, setAdded] = useState(false);

  useEffect(() => {
    fetch(`/api/products/${id}`)
      .then(res => res.json())
      .then(data => setProduct(data))
      .catch(err => console.error('Error:', err));
  }, [id]);

  const handleAddToCart = () => {
    if (!product) return;
    addToCart(product, quantity);
    setAdded(true);
    setTimeout(() => setAdded(false), 2000);
  };

  const handleBuyNow = () => {
    if (!product) return;
    addToCart(product, quantity);
    navigate('/checkout');
  };

  if (!product) {
    return (
      <div style={{ minHeight: '100vh', background: 'var(--bg)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <div style={{ textAlign: 'center', color: 'var(--text-2)' }}>
          <div style={{ fontSize: '40px', marginBottom: '12px' }}>⏳</div>
          <p>Loading product…</p>
        </div>
      </div>
    );
  }

  const saved = Math.round(product.price * 0.2);
  const original = product.price + saved;

  return (
    <div style={{ minHeight: '100vh', background: 'var(--bg)' }}>
      <div className="main-content">
        <div className="content-max-width">

          {/* Breadcrumb */}
          <div style={{ fontSize: '12px', color: 'var(--text-3)', marginBottom: '16px', display: 'flex', gap: '6px' }}>
            <span style={{ cursor: 'pointer', color: 'var(--teal)' }} onClick={() => navigate('/')}>Home</span>
            <span>›</span>
            <span style={{ cursor: 'pointer', color: 'var(--teal)' }} onClick={() => navigate('/search')}>Products</span>
            <span>›</span>
            <span style={{ color: 'var(--text-2)' }}>{product.name}</span>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1.1fr 1.4fr 1fr', gap: '24px', marginBottom: '24px' }}>

            {/* Image */}
            <div style={{
              background: 'var(--bg)', borderRadius: 'var(--radius-md)',
              height: '420px', display: 'flex', alignItems: 'center',
              justifyContent: 'center', overflow: 'hidden',
              border: '1.5px solid var(--border)',
            }}>
              {product.image_url
                ? <img src={product.image_url} alt={product.name} style={{ width: '100%', height: '100%', objectFit: 'cover', borderRadius: 'var(--radius-md)' }} />
                : <span style={{ fontSize: '110px' }}>🛍️</span>}
            </div>

            {/* Info */}
            <div style={{ paddingTop: '4px' }}>
              {product.category && (
                <div style={{ fontSize: '11px', fontWeight: 700, color: 'var(--teal)', textTransform: 'uppercase', letterSpacing: '1px', marginBottom: '8px' }}>
                  {product.category}
                </div>
              )}
              <h1 style={{ fontSize: '22px', fontWeight: 800, lineHeight: 1.25, marginBottom: '12px', color: 'var(--dark)' }}>
                {product.name}
              </h1>

              <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '16px' }}>
                <span style={{ color: '#F59E0B', fontSize: '16px' }}>★★★★★</span>
                <span style={{ fontSize: '13px', color: 'var(--teal)', fontWeight: 600 }}>456 reviews</span>
              </div>

              <div style={{ marginBottom: '20px', paddingBottom: '20px', borderBottom: '1.5px solid var(--border)' }}>
                <div style={{ display: 'flex', alignItems: 'baseline', gap: '10px' }}>
                  <span style={{ fontSize: '30px', fontWeight: 800, color: 'var(--primary)' }}>₹{product.price}</span>
                  <span style={{ fontSize: '16px', color: 'var(--text-3)', textDecoration: 'line-through' }}>₹{original}</span>
                  <span style={{ fontSize: '13px', color: '#16A34A', fontWeight: 700, background: '#F0FDF4', padding: '2px 8px', borderRadius: '20px' }}>Save ₹{saved}</span>
                </div>
                <div style={{ fontSize: '12px', color: 'var(--text-3)', marginTop: '6px' }}>Inclusive of all taxes</div>
              </div>

              <div style={{ marginBottom: '20px' }}>
                <h3 style={{ fontWeight: 700, fontSize: '13px', marginBottom: '10px', color: 'var(--dark)', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Key Features</h3>
                <ul style={{ listStyle: 'none', fontSize: '13px', display: 'flex', flexDirection: 'column', gap: '6px' }}>
                  {['Premium quality', 'Comfortable & durable', 'Fast shipping', '30-day easy returns'].map(f => (
                    <li key={f} style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-2)' }}>
                      <span style={{ color: '#16A34A', fontWeight: 700 }}>✓</span> {f}
                    </li>
                  ))}
                </ul>
              </div>

              <div style={{ background: 'var(--teal-lt)', border: '1px solid #BAE6FD', borderRadius: 'var(--radius-sm)', padding: '12px 14px', fontSize: '13px', color: 'var(--dark)' }}>
                <div style={{ marginBottom: '4px' }}><strong>🚚 Free Delivery</strong> on orders above ₹499</div>
                <div><strong style={{ color: '#16A34A' }}>✓ In Stock</strong> — Ships within 1–2 days</div>
              </div>
            </div>

            {/* Buy box */}
            <div className="section" style={{ position: 'sticky', top: '100px', height: 'fit-content' }}>
              <div style={{ fontSize: '26px', fontWeight: 800, color: 'var(--primary)', marginBottom: '4px' }}>₹{product.price}</div>
              <div style={{ fontSize: '12px', color: '#16A34A', fontWeight: 600, marginBottom: '16px' }}>✓ In Stock</div>

              <div style={{ marginBottom: '16px' }}>
                <label style={{ fontSize: '12px', fontWeight: 700, display: 'block', marginBottom: '8px', color: 'var(--text-2)', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Quantity</label>
                <div style={{ display: 'flex', alignItems: 'center', border: '1.5px solid var(--border)', borderRadius: 'var(--radius-sm)', width: 'fit-content', overflow: 'hidden' }}>
                  <button onClick={() => setQuantity(Math.max(1, quantity - 1))}
                    style={{ padding: '8px 14px', border: 'none', background: 'var(--bg)', cursor: 'pointer', fontSize: '18px', fontWeight: 700, color: 'var(--dark)' }}>−</button>
                  <span style={{ padding: '8px 18px', borderLeft: '1px solid var(--border)', borderRight: '1px solid var(--border)', fontWeight: 700 }}>{quantity}</span>
                  <button onClick={() => setQuantity(quantity + 1)}
                    style={{ padding: '8px 14px', border: 'none', background: 'var(--bg)', cursor: 'pointer', fontSize: '18px', fontWeight: 700, color: 'var(--dark)' }}>+</button>
                </div>
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                <button onClick={handleAddToCart} style={{
                  width: '100%', background: added ? '#16A34A' : 'var(--primary)',
                  color: '#fff', padding: '13px', borderRadius: 'var(--radius-sm)',
                  fontWeight: 700, border: 'none', cursor: 'pointer', fontSize: '14px',
                  transition: 'background 0.2s', letterSpacing: '0.2px',
                }}>
                  {added ? '✓ Added to Cart!' : 'Add to Cart'}
                </button>
                <button onClick={handleBuyNow} style={{
                  width: '100%', background: 'var(--dark)',
                  color: '#fff', padding: '13px', borderRadius: 'var(--radius-sm)',
                  fontWeight: 700, border: 'none', cursor: 'pointer', fontSize: '14px',
                }}>
                  Buy Now
                </button>
              </div>

              <div style={{ marginTop: '16px', paddingTop: '14px', borderTop: '1px solid var(--border)', fontSize: '12px', color: 'var(--text-2)' }}>
                <div style={{ marginBottom: '6px' }}>🏪 <strong>Sold by</strong> Luxe Retail Store</div>
                <div style={{ color: '#16A34A', fontWeight: 600 }}>⭐ 98% positive feedback</div>
              </div>
            </div>
          </div>

          {/* Reviews */}
          <div className="section">
            <h2 style={{ fontSize: '17px', fontWeight: 700, marginBottom: '16px', color: 'var(--dark)' }}>Customer Reviews</h2>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '14px' }}>
              {[
                { name: 'Arjun M.', text: 'Excellent quality! Delivered in just 2 days. Very happy with the purchase.' },
                { name: 'Priya S.', text: 'Great value for money. Packaging was secure and product is exactly as described.' },
                { name: 'Rahul K.', text: 'Highly recommended! Will definitely shop again from Luxe Retail.' },
              ].map(r => (
                <div key={r.name} style={{ background: 'var(--bg)', borderRadius: 'var(--radius-sm)', padding: '14px', border: '1px solid var(--border)' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
                    <div style={{ width: '32px', height: '32px', borderRadius: '50%', background: 'var(--primary)', color: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 700, fontSize: '13px' }}>
                      {r.name[0]}
                    </div>
                    <div>
                      <div style={{ fontWeight: 700, fontSize: '13px' }}>{r.name}</div>
                      <span style={{ color: '#F59E0B', fontSize: '12px' }}>★★★★★</span>
                    </div>
                  </div>
                  <p style={{ fontSize: '13px', color: 'var(--text-2)', lineHeight: 1.5 }}>{r.text}</p>
                </div>
              ))}
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}
