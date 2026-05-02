import { useEffect, useState } from 'react';

export default function AdminProducts() {
  const [products, setProducts] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    price: '',
    category: '',
    description: ''
  });
  const [uploadingId, setUploadingId] = useState(null);
  const [uploadError, setUploadError] = useState(null);

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = () => {
    fetch('/api/products/?limit=100')
      .then(res => res.json())
      .then(data => setProducts(data.products || []))
      .catch(err => console.error('Error:', err));
  };

  const handleFormChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleAddProduct = () => {
    if (!formData.name || !formData.price) {
      alert('Please fill in all fields');
      return;
    }

    // For demo, just add to local list (backend integration would go here)
    const newProduct = {
      id: `prod-${Date.now()}`,
      ...formData,
      price: parseFloat(formData.price),
      created_at: new Date().toISOString()
    };

    setProducts(prev => [newProduct, ...prev]);
    setFormData({ name: '', price: '', category: '', description: '' });
    setShowForm(false);
    alert('Product added successfully!');
  };

  const handleDelete = (productId) => {
    if (confirm('Are you sure you want to delete this product?')) {
      setProducts(prev => prev.filter(p => p.id !== productId));
      alert('Product deleted!');
    }
  };

  const handleImageUpload = async (productId, file) => {
    const allowed = ['image/jpeg', 'image/png', 'image/webp'];
    if (!allowed.includes(file.type)) {
      setUploadError(`Only JPG, PNG, and WebP images are allowed.`);
      return;
    }

    setUploadingId(productId);
    setUploadError(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch(`/api/products/${productId}/image`, {
        method: 'POST',
        headers: {
          'x-user-role': 'admin',
          'x-user-id': 'admin',
        },
        body: formData,
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || 'Upload failed');
      }

      const updated = await res.json();
      setProducts(prev => prev.map(p => p.id === productId ? { ...p, image_url: updated.image_url } : p));
    } catch (err) {
      setUploadError(`Upload failed: ${err.message}`);
    } finally {
      setUploadingId(null);
    }
  };

  const handleImageDelete = async (productId) => {
    if (!confirm('Remove this product image?')) return;

    setUploadingId(productId);
    try {
      const res = await fetch(`/api/products/${productId}/image`, {
        method: 'DELETE',
        headers: { 'x-user-role': 'admin', 'x-user-id': 'admin' },
      });
      if (!res.ok) throw new Error('Delete failed');
      const updated = await res.json();
      setProducts(prev => prev.map(p => p.id === productId ? { ...p, image_url: updated.image_url } : p));
    } catch (err) {
      setUploadError(`Remove failed: ${err.message}`);
    } finally {
      setUploadingId(null);
    }
  };

  return (
    <div style={{ padding: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <h1 style={{ fontSize: '28px', fontWeight: 'bold' }}>Products</h1>
        <button
          onClick={() => setShowForm(!showForm)}
          style={{
            background: '#FF9900',
            color: 'black',
            padding: '10px 16px',
            borderRadius: '4px',
            border: 'none',
            cursor: 'pointer',
            fontWeight: 'bold',
            fontSize: '13px'
          }}
        >
          {showForm ? '✕ Cancel' : '+ Add Product'}
        </button>
      </div>

      {/* Add Product Form */}
      {showForm && (
        <div style={{ background: '#FFFFFF', padding: '20px', borderRadius: '4px', marginBottom: '24px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
          <h2 style={{ fontSize: '16px', fontWeight: 'bold', marginBottom: '16px' }}>Add New Product</h2>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', marginBottom: '16px' }}>
            <input
              type="text"
              name="name"
              placeholder="Product Name"
              value={formData.name}
              onChange={handleFormChange}
              style={{ padding: '10px', border: '1px solid #ddd', borderRadius: '4px', fontSize: '13px' }}
            />
            <input
              type="number"
              name="price"
              placeholder="Price"
              value={formData.price}
              onChange={handleFormChange}
              style={{ padding: '10px', border: '1px solid #ddd', borderRadius: '4px', fontSize: '13px' }}
            />
            <input
              type="text"
              name="category"
              placeholder="Category"
              value={formData.category}
              onChange={handleFormChange}
              style={{ padding: '10px', border: '1px solid #ddd', borderRadius: '4px', fontSize: '13px' }}
            />
            <input
              type="text"
              name="description"
              placeholder="Description"
              value={formData.description}
              onChange={handleFormChange}
              style={{ padding: '10px', border: '1px solid #ddd', borderRadius: '4px', fontSize: '13px' }}
            />
          </div>
          <button
            onClick={handleAddProduct}
            style={{
              background: '#007600',
              color: 'white',
              padding: '10px 16px',
              borderRadius: '4px',
              border: 'none',
              cursor: 'pointer',
              fontWeight: 'bold',
              fontSize: '13px'
            }}
          >
            Save Product
          </button>
        </div>
      )}

      {/* Error Banner */}
      {uploadError && (
        <div style={{
          background: '#fff3cd',
          border: '1px solid #ffc107',
          padding: '10px 16px',
          borderRadius: '4px',
          marginBottom: '16px',
          fontSize: '12px',
          color: '#856404',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}>
          {uploadError}
          <button
            onClick={() => setUploadError(null)}
            style={{ background: 'none', border: 'none', cursor: 'pointer', fontWeight: 'bold', fontSize: '14px', color: '#856404' }}
          >
            ×
          </button>
        </div>
      )}

      {/* Products Table */}
      <div style={{ background: '#FFFFFF', padding: '20px', borderRadius: '4px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ borderBottom: '2px solid #f0f0f0' }}>
                <th style={{ padding: '12px', textAlign: 'left', fontSize: '13px', fontWeight: 'bold' }}>Image</th>
                <th style={{ padding: '12px', textAlign: 'left', fontSize: '13px', fontWeight: 'bold' }}>Name</th>
                <th style={{ padding: '12px', textAlign: 'left', fontSize: '13px', fontWeight: 'bold' }}>Price</th>
                <th style={{ padding: '12px', textAlign: 'left', fontSize: '13px', fontWeight: 'bold' }}>Category</th>
                <th style={{ padding: '12px', textAlign: 'center', fontSize: '13px', fontWeight: 'bold' }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {products.map(product => (
                <tr key={product.id} style={{ borderBottom: '1px solid #f0f0f0' }}>
                  <td style={{ padding: '12px', fontSize: '12px' }}>
                    <label
                      htmlFor={`img-upload-${product.id}`}
                      style={{ cursor: 'pointer', display: 'inline-block' }}
                      title="Click to upload image"
                    >
                      {uploadingId === product.id ? (
                        <div style={{
                          width: '50px', height: '50px', background: '#f0f0f0', borderRadius: '4px',
                          display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '10px', color: '#666'
                        }}>
                          ...
                        </div>
                      ) : product.image_url ? (
                        <img
                          src={product.image_url}
                          alt={product.name}
                          style={{
                            width: '50px', height: '50px', objectFit: 'cover', borderRadius: '4px',
                            border: '2px solid transparent', transition: 'border-color 0.15s'
                          }}
                          onMouseEnter={e => e.currentTarget.style.borderColor = '#FF9900'}
                          onMouseLeave={e => e.currentTarget.style.borderColor = 'transparent'}
                        />
                      ) : (
                        <div style={{
                          width: '50px', height: '50px', background: '#f0f0f0', borderRadius: '4px',
                          display: 'flex', alignItems: 'center', justifyContent: 'center',
                          fontSize: '20px', color: '#999', border: '2px dashed #ccc'
                        }}>
                          +
                        </div>
                      )}
                      <input
                        id={`img-upload-${product.id}`}
                        type="file"
                        accept="image/jpeg,image/png,image/webp"
                        style={{ display: 'none' }}
                        onChange={e => {
                          const file = e.target.files[0];
                          if (file) handleImageUpload(product.id, file);
                          e.target.value = '';
                        }}
                      />
                    </label>
                    {product.image_url && product.image_url.startsWith('/uploads/') && (
                      <button
                        onClick={() => handleImageDelete(product.id)}
                        title="Remove image"
                        style={{
                          display: 'block', marginTop: '3px', fontSize: '9px', color: '#B12704',
                          background: 'none', border: 'none', cursor: 'pointer', padding: 0
                        }}
                      >
                        remove
                      </button>
                    )}
                  </td>
                  <td style={{ padding: '12px', fontSize: '12px' }}>{product.name}</td>
                  <td style={{ padding: '12px', fontSize: '12px' }}>₹{product.price}</td>
                  <td style={{ padding: '12px', fontSize: '12px' }}>{product.category || '-'}</td>
                  <td style={{ padding: '12px', textAlign: 'center', fontSize: '12px' }}>
                    <button
                      onClick={() => handleDelete(product.id)}
                      style={{
                        background: '#B12704',
                        color: 'white',
                        padding: '6px 12px',
                        borderRadius: '3px',
                        border: 'none',
                        cursor: 'pointer',
                        fontSize: '11px',
                        fontWeight: 'bold'
                      }}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <p style={{ marginTop: '16px', fontSize: '12px', color: '#666' }}>
          Total: {products.length} products
        </p>
      </div>
    </div>
  );
}
