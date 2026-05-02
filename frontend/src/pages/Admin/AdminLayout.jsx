import { Link, useLocation } from 'react-router-dom';

export default function AdminLayout({ children }) {
  const location = useLocation();

  const isActive = (path) => location.pathname === path ? '#FF9900' : 'transparent';

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '240px 1fr', minHeight: '100vh', background: '#EAEDED' }}>
      {/* Sidebar */}
      <div style={{ background: '#131921', color: 'white', padding: '0', position: 'sticky', top: '80px', height: 'calc(100vh - 80px)', overflowY: 'auto' }}>
        <div style={{ padding: '20px' }}>
          <h2 style={{ fontSize: '16px', fontWeight: 'bold', marginBottom: '24px', color: '#FF9900' }}>Admin Panel</h2>

          <nav style={{ display: 'flex', flexDirection: 'column', gap: '0' }}>
            <Link
              to="/admin"
              style={{
                padding: '12px 16px',
                color: 'white',
                textDecoration: 'none',
                fontSize: '13px',
                cursor: 'pointer',
                background: isActive('/admin'),
                borderLeft: isActive('/admin') !== 'transparent' ? '4px solid #FF9900' : '4px solid transparent',
                paddingLeft: '12px',
                transition: 'all 0.2s'
              }}
              onMouseEnter={(e) => e.currentTarget.style.background = '#232F3E'}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = isActive('/admin');
              }}
            >
              📊 Dashboard
            </Link>

            <Link
              to="/admin/products"
              style={{
                padding: '12px 16px',
                color: 'white',
                textDecoration: 'none',
                fontSize: '13px',
                cursor: 'pointer',
                background: isActive('/admin/products'),
                borderLeft: isActive('/admin/products') !== 'transparent' ? '4px solid #FF9900' : '4px solid transparent',
                paddingLeft: '12px',
                transition: 'all 0.2s'
              }}
              onMouseEnter={(e) => e.currentTarget.style.background = '#232F3E'}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = isActive('/admin/products');
              }}
            >
              📦 Products
            </Link>

            <Link
              to="/admin/orders"
              style={{
                padding: '12px 16px',
                color: 'white',
                textDecoration: 'none',
                fontSize: '13px',
                cursor: 'pointer',
                background: isActive('/admin/orders'),
                borderLeft: isActive('/admin/orders') !== 'transparent' ? '4px solid #FF9900' : '4px solid transparent',
                paddingLeft: '12px',
                transition: 'all 0.2s'
              }}
              onMouseEnter={(e) => e.currentTarget.style.background = '#232F3E'}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = isActive('/admin/orders');
              }}
            >
              📋 Orders
            </Link>

            <Link
              to="/admin/catalog"
              style={{
                padding: '12px 16px',
                color: 'white',
                textDecoration: 'none',
                fontSize: '13px',
                cursor: 'pointer',
                background: isActive('/admin/catalog'),
                borderLeft: isActive('/admin/catalog') !== 'transparent' ? '4px solid #FF9900' : '4px solid transparent',
                paddingLeft: '12px',
                transition: 'all 0.2s'
              }}
              onMouseEnter={(e) => e.currentTarget.style.background = '#232F3E'}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = isActive('/admin/catalog');
              }}
            >
              🗂️ Catalog
            </Link>

            <Link
              to="/admin/promotions"
              style={{
                padding: '12px 16px',
                color: 'white',
                textDecoration: 'none',
                fontSize: '13px',
                cursor: 'pointer',
                background: isActive('/admin/promotions'),
                borderLeft: isActive('/admin/promotions') !== 'transparent' ? '4px solid #FF9900' : '4px solid transparent',
                paddingLeft: '12px',
                transition: 'all 0.2s'
              }}
              onMouseEnter={(e) => e.currentTarget.style.background = '#232F3E'}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = isActive('/admin/promotions');
              }}
            >
              🏷️ Promotions
            </Link>

            <Link
              to="/"
              style={{
                padding: '12px 16px',
                color: 'white',
                textDecoration: 'none',
                fontSize: '13px',
                cursor: 'pointer',
                marginTop: '24px',
                borderTop: '1px solid #232F3E',
                paddingTop: '16px'
              }}
              onMouseEnter={(e) => e.currentTarget.style.background = '#232F3E'}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = 'transparent';
              }}
            >
              ← Back to Store
            </Link>
          </nav>
        </div>
      </div>

      {/* Main Content */}
      <div style={{ background: '#EAEDED', overflowY: 'auto' }}>
        {children}
      </div>
    </div>
  );
}
