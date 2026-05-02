import { useEffect, useState, useRef } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useCart } from '../context/CartContext';

const STATIC_CATEGORIES = [
  { key: 'electronics', icon: '📱', name: 'Electronics',    sub: 'Phones · Laptops · Audio', bg: '#EFF6FF', border: '#BFDBFE' },
  { key: 'fashion',     icon: '👕', name: 'Fashion',        sub: 'Men · Women · Kids',       bg: '#FFF1F2', border: '#FECDD3' },
  { key: 'home',        icon: '🏠', name: 'Home & Kitchen', sub: 'Decor · Appliances',       bg: '#F0FDF4', border: '#BBF7D0' },
  { key: 'beauty',      icon: '💄', name: 'Beauty',         sub: 'Skincare · Makeup',        bg: '#FDF4FF', border: '#E9D5FF' },
  { key: 'sports',      icon: '⚽', name: 'Sports',         sub: 'Fitness · Outdoor',        bg: '#FFFBEB', border: '#FDE68A' },
  { key: 'books',       icon: '📚', name: 'Books',          sub: 'Fiction · Reference',      bg: '#F0F9FF', border: '#BAE6FD' },
];

export default function Home() {
  const [products, setProducts] = useState([]);
  const [deals, setDeals]     = useState([]);
  const [contentSlots, setContentSlots] = useState({});
  const { addToCart } = useCart();
  const navigate = useNavigate();

  const carouselRefs = {
    deals:       useRef(null),
    recommended: useRef(null),
    newReleases: useRef(null),
    bestSellers: useRef(null),
  };

  useEffect(() => {
    fetch('/api/products/?limit=12')
      .then(r => r.json()).then(d => setProducts(d.products || [])).catch(() => {});
    fetch('/api/products/deals?limit=12')
      .then(r => r.json()).then(d => setDeals(Array.isArray(d) ? d : [])).catch(() => {});
    fetch('/api/content/slots')
      .then(r => r.json()).then(d => setContentSlots(d.slots || {})).catch(() => {});
  }, []);

  const scroll = (ref, dir) => {
    if (ref.current) ref.current.scrollBy({ left: dir === 'left' ? -300 : 300, behavior: 'smooth' });
  };

  const ProductCard = ({ product, isDeal = false }) => {
    const handleAdd = (e) => { e.preventDefault(); e.stopPropagation(); addToCart(product, 1); };
    return (
      <Link to={`/product/${product.id}`} style={{ textDecoration: 'none' }}>
        <div className="product-card">
          <div className="product-image">
            {product.image_url
              ? <img src={product.image_url} alt={product.name} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
              : <span>🛍️</span>}
          </div>
          {isDeal && <div className="product-deal-badge">Limited time deal</div>}
          <h3 className="product-name">{product.name}</h3>
          <div className="product-rating">
            <span className="stars">★★★★☆</span>
            <span className="count">(128)</span>
          </div>
          <div className="product-price">
            <span>₹{product.price}</span>
            <span className="original">₹{Math.round(product.price * 1.3)}</span>
          </div>
          <div className="product-prime">✓ Free Delivery</div>
          <button className="product-add-btn" onClick={handleAdd}>Add to Cart</button>
        </div>
      </Link>
    );
  };

  const Carousel = ({ refKey, items, isDeal }) => (
    <div style={{ position: 'relative' }}>
      <div className="carousel" ref={carouselRefs[refKey]}>
        {items.map(p => <ProductCard key={p.id} product={p} isDeal={isDeal} />)}
      </div>
      <button className="carousel-arrow left"  onClick={() => scroll(carouselRefs[refKey], 'left')}>‹</button>
      <button className="carousel-arrow right" onClick={() => scroll(carouselRefs[refKey], 'right')}>›</button>
    </div>
  );

  const cmsCategories = Object.values(contentSlots).filter(s => s.slot_type === 'category_tile');

  return (
    <div style={{ minHeight: '100vh', background: 'var(--bg)' }}>

      {/* Hero */}
      <div className="hero">
        <div className="hero-inner">
          <div className="hero-text">
            <div className="hero-eyebrow">Welcome to Luxe Retail</div>
            <h1>Everything you<br />need, delivered.</h1>
            <p>Electronics, fashion, home essentials, beauty and more — all in one place, with prices you'll love.</p>
            <div>
              <button className="hero-cta" onClick={() => navigate('/search')}>Shop Now</button>
              <span className="hero-badge">🚚 Free delivery above ₹499</span>
            </div>
          </div>
          <div className="hero-icons">
            {[
              { icon: '📱', label: 'Electronics' },
              { icon: '👕', label: 'Fashion' },
              { icon: '🏠', label: 'Home' },
              { icon: '💄', label: 'Beauty' },
            ].map(({ icon, label }) => (
              <div key={label} className="hero-icon-card" onClick={() => navigate(`/search?category=${label.toLowerCase()}`)}>
                <span className="icon">{icon}</span>
                <span>{label}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="main-content">
        <div className="content-max-width">

          {/* Today's Deals */}
          {deals.length > 0 && (
            <div className="section">
              <div className="section-title">
                <span className="title">🔥 Today's Deals</span>
                <span className="badge">LIMITED</span>
                <span className="see-all" onClick={() => navigate('/search?sort=deals')}>See all deals</span>
              </div>
              <Carousel refKey="deals" items={deals} isDeal />
            </div>
          )}

          {/* Shop by Category */}
          <div className="section">
            <div className="section-title">
              <span className="title">Shop by Category</span>
            </div>
            <div className="category-grid">
              {(cmsCategories.length > 0 ? cmsCategories : STATIC_CATEGORIES).map((cat, i) => {
                const fallback = STATIC_CATEGORIES[i] || STATIC_CATEGORIES[0];
                const bg     = cat.bg     || fallback.bg;
                const border = cat.border || fallback.border;
                const key    = cat.slot_key || cat.key;
                const icon   = cat.image_url ? null : (cat.icon || fallback.icon);
                const name   = cat.title || cat.name;
                const sub    = cat.subtitle || cat.sub;
                return (
                  <div
                    key={key}
                    className="category-card"
                    style={{ background: bg, borderColor: border }}
                    onClick={() => navigate(`/search?category=${name.toLowerCase().replace(/\s+/g,'').replace(/&/g,'')}`)}
                  >
                    {cat.image_url
                      ? <img src={cat.image_url} alt={name} style={{ width: '40px', height: '40px', objectFit: 'cover', borderRadius: '50%', marginBottom: '10px' }} />
                      : <span className="icon">{icon}</span>}
                    <div className="name">{name}</div>
                    {sub && <div className="sub">{sub}</div>}
                  </div>
                );
              })}
            </div>
          </div>

          {/* Recommended */}
          {products.length > 0 && (
            <div className="section">
              <div className="section-title">
                <span className="title">Recommended For You</span>
                <span className="see-all" onClick={() => navigate('/search')}>See all</span>
              </div>
              <Carousel refKey="recommended" items={products.slice(0, 8)} />
            </div>
          )}

          {/* New Arrivals */}
          {products.length > 0 && (
            <div className="section">
              <div className="section-title">
                <span className="title">✨ New Arrivals</span>
                <span className="see-all" onClick={() => navigate('/search?sort=newest')}>See all</span>
              </div>
              <Carousel refKey="newReleases" items={products.slice(2, 10)} />
            </div>
          )}

          {/* Best Sellers */}
          {products.length > 0 && (
            <div className="section">
              <div className="section-title">
                <span className="title">⭐ Best Sellers</span>
                <span className="see-all" onClick={() => navigate('/search?sort=bestsellers')}>See all</span>
              </div>
              <Carousel refKey="bestSellers" items={products.slice(4, 12)} />
            </div>
          )}

          {/* Trust strip */}
          <div style={{
            display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(160px,1fr))', gap: '12px', marginBottom: '8px',
          }}>
            {[
              { icon: '🚚', title: 'Free Delivery', sub: 'On orders above ₹499' },
              { icon: '↩️', title: 'Easy Returns',  sub: '30-day return policy' },
              { icon: '🔒', title: 'Secure Payment', sub: 'UPI, Cards & Wallets' },
              { icon: '🎧', title: '24/7 Support',   sub: 'Always here for you' },
            ].map(({ icon, title, sub }) => (
              <div key={title} className="section" style={{ textAlign: 'center', padding: '16px', marginBottom: 0 }}>
                <div style={{ fontSize: '28px', marginBottom: '6px' }}>{icon}</div>
                <div style={{ fontWeight: 700, fontSize: '13px', marginBottom: '2px' }}>{title}</div>
                <div style={{ fontSize: '11px', color: 'var(--text-3)' }}>{sub}</div>
              </div>
            ))}
          </div>

        </div>
      </div>

      {/* Footer */}
      <footer>
        <div className="footer-content">
          <div className="footer-section">
            <h4>Luxe Retail</h4>
            <ul>
              <li><a href="#">About Us</a></li>
              <li><a href="#">Careers</a></li>
              <li><a href="#">Press</a></li>
            </ul>
          </div>
          <div className="footer-section">
            <h4>Shop</h4>
            <ul>
              <li><a href="#">Electronics</a></li>
              <li><a href="#">Fashion</a></li>
              <li><a href="#">Home & Kitchen</a></li>
              <li><a href="#">Beauty</a></li>
            </ul>
          </div>
          <div className="footer-section">
            <h4>Customer Service</h4>
            <ul>
              <li><a href="#">Help Center</a></li>
              <li><a href="#">Returns</a></li>
              <li><a href="#">Track Order</a></li>
              <li><a href="#">Contact Us</a></li>
            </ul>
          </div>
          <div className="footer-section">
            <h4>Connect</h4>
            <ul>
              <li><a href="#">Instagram</a></li>
              <li><a href="#">Twitter / X</a></li>
              <li><a href="#">Facebook</a></li>
              <li><a href="#">YouTube</a></li>
            </ul>
          </div>
        </div>
        <div className="footer-bottom">
          <p>© 2026 Luxe Retail. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
