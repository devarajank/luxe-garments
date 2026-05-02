import { Link, useNavigate } from 'react-router-dom';
import { useState, useRef, useEffect } from 'react';
import { useCart } from '../context/CartContext';
import { useAuth } from '../context/AuthContext';

const CATEGORIES = [
  { name: 'Electronics', icon: '📱', subcategories: ['Smartphones', 'Laptops', 'Tablets', 'Accessories', 'Audio'] },
  { name: 'Fashion',     icon: '👕', subcategories: ['Men', 'Women', 'Kids', 'Shoes', 'Accessories'] },
  { name: 'Home & Kitchen', icon: '🏠', subcategories: ['Kitchen', 'Bedding', 'Furniture', 'Decor', 'Appliances'] },
  { name: 'Books',       icon: '📚', subcategories: ['Fiction', 'Non-Fiction', 'Educational', 'Comics', 'Reference'] },
  { name: 'Sports',      icon: '⚽', subcategories: ['Equipment', 'Apparel', 'Outdoor', 'Fitness', 'Games'] },
  { name: 'Beauty',      icon: '💄', subcategories: ['Skincare', 'Makeup', 'Haircare', 'Fragrance', 'Wellness'] },
];

export default function Navbar() {
  const [searchQuery, setSearchQuery] = useState('');
  const [menuOpen, setMenuOpen] = useState(false);
  const [expandedCategory, setExpandedCategory] = useState(null);
  const [accountOpen, setAccountOpen] = useState(false);
  const accountRef = useRef(null);
  const navigate = useNavigate();
  const { getCartCount } = useCart();
  const { user, logout } = useAuth();

  useEffect(() => {
    const handler = (e) => {
      if (accountRef.current && !accountRef.current.contains(e.target)) setAccountOpen(false);
    };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, []);

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/search?q=${encodeURIComponent(searchQuery)}`);
      setSearchQuery('');
    }
  };

  return (
    <nav>
      {/* Main navbar */}
      <div className="nav-main">
        <Link to="/" style={{ textDecoration: 'none', flexShrink: 0 }}>
          <div className="nav-logo">Luxe<span>Retail</span></div>
        </Link>

        <form onSubmit={handleSearch} className="nav-search">
          <select aria-label="Category">
            <option>All</option>
            <option>Electronics</option>
            <option>Fashion</option>
            <option>Home</option>
            <option>Books</option>
            <option>Sports</option>
            <option>Beauty</option>
          </select>
          <input
            type="text"
            placeholder="Search Luxe Retail…"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
          <button type="submit">🔍</button>
        </form>

        <div className="nav-right">
          {/* Account */}
          <div ref={accountRef} style={{ position: 'relative' }}>
            <div onClick={() => user ? setAccountOpen(o => !o) : navigate('/login')}>
              <div className="label">{user ? `Hi, ${user.first_name}` : 'Hello, sign in'}</div>
              <div className="text">Account ▾</div>
            </div>
            {accountOpen && user && (
              <div style={{
                position: 'absolute', top: 'calc(100% + 8px)', right: 0,
                background: '#fff', border: '1px solid #E8E4E0',
                borderRadius: '10px', boxShadow: '0 8px 24px rgba(0,0,0,0.13)',
                zIndex: 200, minWidth: '160px', padding: '8px 0',
              }}>
                <div style={{ padding: '8px 16px', fontSize: '12px', color: '#6B7280', borderBottom: '1px solid #f0f0f0' }}>
                  {user.email}
                </div>
                <button
                  onClick={() => { setAccountOpen(false); navigate('/account'); }}
                  style={{
                    display: 'block', width: '100%', textAlign: 'left',
                    padding: '10px 16px', background: 'none', border: 'none',
                    fontSize: '13px', cursor: 'pointer', color: '#1D2939', fontWeight: 600,
                  }}
                  onMouseEnter={e => e.currentTarget.style.background = '#F9F7F4'}
                  onMouseLeave={e => e.currentTarget.style.background = 'none'}
                >
                  My Account
                </button>
                <button
                  onClick={() => { logout(); setAccountOpen(false); navigate('/'); }}
                  style={{
                    display: 'block', width: '100%', textAlign: 'left',
                    padding: '10px 16px', background: 'none', border: 'none',
                    fontSize: '13px', cursor: 'pointer', color: '#1D2939', fontWeight: 600,
                  }}
                  onMouseEnter={e => e.currentTarget.style.background = '#F9F7F4'}
                  onMouseLeave={e => e.currentTarget.style.background = 'none'}
                >
                  Sign out
                </button>
              </div>
            )}
          </div>

          {/* Orders */}
          <div onClick={() => user ? navigate('/orders') : navigate('/login', { state: { from: '/orders' } })}>
            <div className="label">Returns</div>
            <div className="text">& Orders</div>
          </div>

          {/* Cart */}
          <Link to="/cart" style={{ textDecoration: 'none' }}>
            <div className="nav-cart">
              <div className="nav-cart-icon">🛒</div>
              <span style={{ color: '#fff', fontWeight: 600 }}>Cart</span>
              <div className="nav-cart-badge">{getCartCount()}</div>
            </div>
          </Link>
        </div>
      </div>

      {/* Category strip */}
      <div className="nav-secondary" style={{ position: 'relative' }}>
        <button onClick={() => setMenuOpen(!menuOpen)}>☰ All Categories</button>
        {CATEGORIES.map(cat => (
          <button
            key={cat.name}
            onClick={() => navigate(`/search?category=${cat.name.toLowerCase().replace(/\s+/g, '')}`)}
          >
            {cat.icon} {cat.name}
          </button>
        ))}
        <button onClick={() => navigate('/search?sort=deals')}>🔥 Deals</button>
        <button onClick={() => navigate('/search?sort=newest')}>✨ New Arrivals</button>

        {/* Mega menu */}
        {menuOpen && (
          <>
            <div
              onClick={() => setMenuOpen(false)}
              style={{ position: 'fixed', inset: 0, zIndex: 50 }}
            />
            <div style={{
              position: 'absolute', top: '100%', left: 0,
              background: '#fff', boxShadow: '0 8px 32px rgba(0,0,0,0.15)',
              zIndex: 100, width: '320px', borderRadius: '0 0 12px 12px',
              overflow: 'hidden',
            }}>
              {CATEGORIES.map(category => (
                <div key={category.name}>
                  <div
                    onClick={() => setExpandedCategory(expandedCategory === category.name ? null : category.name)}
                    style={{
                      padding: '12px 18px', cursor: 'pointer', color: '#1D2939',
                      fontSize: '13px', fontWeight: 600,
                      background: expandedCategory === category.name ? '#F9F7F4' : 'transparent',
                      display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                      borderBottom: '1px solid #F0EDE8',
                    }}
                    onMouseEnter={e => e.currentTarget.style.background = '#F9F7F4'}
                    onMouseLeave={e => e.currentTarget.style.background = expandedCategory === category.name ? '#F9F7F4' : 'transparent'}
                  >
                    <span>{category.icon}  {category.name}</span>
                    <span style={{ fontSize: '10px', color: '#9CA3AF' }}>{expandedCategory === category.name ? '▼' : '▶'}</span>
                  </div>
                  {expandedCategory === category.name && (
                    <div style={{ background: '#FAFAF9' }}>
                      {category.subcategories.map(sub => (
                        <div
                          key={sub}
                          onClick={() => {
                            navigate(`/search?category=${category.name.toLowerCase().replace(/\s+/g,'')}&subcategory=${sub.toLowerCase().replace(/\s+/g,'')}`);
                            setMenuOpen(false); setExpandedCategory(null);
                          }}
                          style={{
                            padding: '9px 18px 9px 36px', cursor: 'pointer',
                            color: '#4B5563', fontSize: '13px', borderBottom: '1px solid #F0EDE8',
                          }}
                          onMouseEnter={e => { e.currentTarget.style.background = '#F0EDE8'; e.currentTarget.style.color = '#CC2936'; }}
                          onMouseLeave={e => { e.currentTarget.style.background = 'transparent'; e.currentTarget.style.color = '#4B5563'; }}
                        >
                          {sub}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </>
        )}
      </div>
    </nav>
  );
}
