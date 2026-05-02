import { useEffect, useState } from 'react';

export default function AdminDashboard() {
  const [stats, setStats] = useState({
    totalProducts: 0,
    totalOrders: 0,
    totalRevenue: 0,
    totalUsers: 0
  });
  const [products, setProducts] = useState([]);

  useEffect(() => {
    // Fetch products
    fetch('/api/products/?limit=100')
      .then(res => res.json())
      .then(data => {
        const prods = data.products || [];
        setProducts(prods);
        setStats(prev => ({
          ...prev,
          totalProducts: prods.length
        }));
      })
      .catch(err => console.error('Error:', err));
  }, []);

  return (
    <div style={{ padding: '24px' }}>
      <h1 style={{ fontSize: '28px', fontWeight: 'bold', marginBottom: '24px' }}>Dashboard</h1>

      {/* Stats Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px', marginBottom: '32px' }}>
        <div style={{ background: '#FFFFFF', padding: '20px', borderRadius: '4px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
          <p style={{ color: '#666', fontSize: '12px', marginBottom: '8px' }}>Total Products</p>
          <p style={{ fontSize: '32px', fontWeight: 'bold', color: '#FF9900' }}>{stats.totalProducts}</p>
        </div>
        <div style={{ background: '#FFFFFF', padding: '20px', borderRadius: '4px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
          <p style={{ color: '#666', fontSize: '12px', marginBottom: '8px' }}>Total Orders</p>
          <p style={{ fontSize: '32px', fontWeight: 'bold', color: '#007185' }}>0</p>
        </div>
        <div style={{ background: '#FFFFFF', padding: '20px', borderRadius: '4px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
          <p style={{ color: '#666', fontSize: '12px', marginBottom: '8px' }}>Total Revenue</p>
          <p style={{ fontSize: '32px', fontWeight: 'bold', color: '#007600' }}>₹0</p>
        </div>
        <div style={{ background: '#FFFFFF', padding: '20px', borderRadius: '4px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
          <p style={{ color: '#666', fontSize: '12px', marginBottom: '8px' }}>Total Users</p>
          <p style={{ fontSize: '32px', fontWeight: 'bold', color: '#B12704' }}>0</p>
        </div>
      </div>

      {/* Recent Products */}
      <div style={{ background: '#FFFFFF', padding: '20px', borderRadius: '4px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
        <h2 style={{ fontSize: '18px', fontWeight: 'bold', marginBottom: '16px' }}>Recent Products</h2>
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ borderBottom: '2px solid #f0f0f0' }}>
                <th style={{ padding: '12px', textAlign: 'left', fontSize: '13px', fontWeight: 'bold' }}>ID</th>
                <th style={{ padding: '12px', textAlign: 'left', fontSize: '13px', fontWeight: 'bold' }}>Name</th>
                <th style={{ padding: '12px', textAlign: 'left', fontSize: '13px', fontWeight: 'bold' }}>Price</th>
                <th style={{ padding: '12px', textAlign: 'left', fontSize: '13px', fontWeight: 'bold' }}>Category</th>
              </tr>
            </thead>
            <tbody>
              {products.slice(0, 5).map(product => (
                <tr key={product.id} style={{ borderBottom: '1px solid #f0f0f0' }}>
                  <td style={{ padding: '12px', fontSize: '12px' }}>{product.id}</td>
                  <td style={{ padding: '12px', fontSize: '12px' }}>{product.name}</td>
                  <td style={{ padding: '12px', fontSize: '12px' }}>₹{product.price}</td>
                  <td style={{ padding: '12px', fontSize: '12px' }}>{product.category || '-'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
