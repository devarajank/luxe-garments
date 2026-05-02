import { useEffect, useState } from 'react';
import { useSearchParams, useNavigate, Link } from 'react-router-dom';
import { useCart } from '../context/CartContext';

const CATEGORIES = [
  {
    name: 'Electronics',
    slug: 'electronics',
    subcategories: ['Smartphones', 'Laptops', 'Tablets', 'Accessories', 'Audio']
  },
  {
    name: 'Fashion',
    slug: 'fashion',
    subcategories: ['Men', 'Women', 'Kids', 'Shoes', 'Accessories']
  },
  {
    name: 'Home & Kitchen',
    slug: 'home',
    subcategories: ['Kitchen', 'Bedding', 'Furniture', 'Decor', 'Appliances']
  },
  {
    name: 'Books',
    slug: 'books',
    subcategories: ['Fiction', 'Non-Fiction', 'Educational', 'Comics', 'Reference']
  },
  {
    name: 'Sports',
    slug: 'sports',
    subcategories: ['Equipment', 'Apparel', 'Outdoor', 'Fitness', 'Games']
  },
  {
    name: 'Beauty',
    slug: 'beauty',
    subcategories: ['Skincare', 'Makeup', 'Haircare', 'Fragrance', 'Wellness']
  }
];

export default function Search() {
  const [searchParams] = useSearchParams();
  const query = searchParams.get('q') || '';
  const category = searchParams.get('category') || '';
  const subcategory = searchParams.get('subcategory') || '';
  const { addToCart } = useCart();

  // Get relevant subcategories for the current category
  const currentCategoryData = CATEGORIES.find(cat => cat.slug === category);
  const filterOptions = currentCategoryData ? currentCategoryData.subcategories : CATEGORIES.map(cat => cat.name);

  const navigate = useNavigate();

  const handleSubcategoryChange = (option) => {
    const slug = option.toLowerCase().replace(/\s+/g, '');
    const params = new URLSearchParams();
    if (query) params.set('q', query);
    if (category) params.set('category', category);
    if (subcategory !== slug) params.set('subcategory', slug);
    navigate(`/search?${params.toString()}`);
  };

  const [products, setProducts] = useState([]);
  const [filters, setFilters] = useState({
    minPrice: 0,
    maxPrice: 500000,
    rating: 0,
  });
  const [sortBy, setSortBy] = useState('featured');

  useEffect(() => {
    const params = new URLSearchParams();
    if (query) params.append('search', query);
    if (category) params.append('category', category);
    if (subcategory) params.append('subcategory', subcategory);
    params.append('min_price', filters.minPrice);
    params.append('max_price', filters.maxPrice);
    params.append('sort_by', sortBy === 'price-low' ? 'price_asc' : sortBy === 'price-high' ? 'price_desc' : sortBy);
    params.append('limit', 20);

    fetch(`/api/products/?${params}`)
      .then(res => res.json())
      .then(data => setProducts(data.products || []))
      .catch(err => console.error('Search error:', err));
  }, [query, category, subcategory, filters, sortBy]);

  const resultCount = products.length;

  return (
    <div style={{ display: 'flex', minHeight: '100vh', background: 'var(--bg)', gap: '20px', padding: '20px 24px', maxWidth: '1400px', margin: '0 auto', width: '100%', boxSizing: 'border-box' }}>
      {/* Left Sidebar - Filters */}
      <div className="search-sidebar">
        <h3 style={{ fontSize: '14px', fontWeight: 700, marginBottom: '16px', color: 'var(--dark)', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Filters</h3>

        {/* Department / Subcategory Filter */}
        <div className="filter-section">
          <div className="filter-title">{category ? 'Subcategories' : 'Categories'}</div>
          {filterOptions.map(option => (
            <div key={option} className="filter-option">
              <input
                type="checkbox"
                id={`filter-${option}`}
                checked={subcategory === option.toLowerCase().replace(/\s+/g, '')}
                onChange={() => handleSubcategoryChange(option)}
              />
              <label htmlFor={`filter-${option}`}>{option}</label>
            </div>
          ))}
        </div>

        {/* Price Filter */}
        <div className="filter-section">
          <div className="filter-title">Price</div>
          <div className="filter-option">
            <input type="radio" name="price" id="price1" checked={filters.maxPrice === 1000} onChange={() => setFilters({ ...filters, minPrice: 0, maxPrice: 1000 })} />
            <label htmlFor="price1">Under ₹1,000</label>
          </div>
          <div className="filter-option">
            <input type="radio" name="price" id="price2" checked={filters.maxPrice === 5000} onChange={() => setFilters({ ...filters, minPrice: 1000, maxPrice: 5000 })} />
            <label htmlFor="price2">₹1,000 - ₹5,000</label>
          </div>
          <div className="filter-option">
            <input type="radio" name="price" id="price3" checked={filters.maxPrice === 10000} onChange={() => setFilters({ ...filters, minPrice: 5000, maxPrice: 10000 })} />
            <label htmlFor="price3">₹5,000 - ₹10,000</label>
          </div>
          <div className="filter-option">
            <input type="radio" name="price" id="price4" checked={filters.maxPrice === 500000} onChange={() => setFilters({ ...filters, minPrice: 10000, maxPrice: 500000 })} />
            <label htmlFor="price4">Above ₹10,000</label>
          </div>
        </div>

        {/* Rating Filter */}
        <div className="filter-section">
          <div className="filter-title">Rating</div>
          {[4, 3, 2, 1].map(rating => (
            <div key={rating} className="filter-option">
              <input type="radio" name="rating" id={`rating${rating}`} onChange={() => setFilters({ ...filters, rating })} />
              <label htmlFor={`rating${rating}`}>{'★'.repeat(rating)} & up</label>
            </div>
          ))}
        </div>

        {/* Prime Filter */}
        <div className="filter-section">
          <div className="filter-option">
            <input type="checkbox" id="prime" />
            <label htmlFor="prime" style={{ fontWeight: 'bold' }}>Prime Eligible</label>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div style={{ flex: 1, minWidth: 0 }}>
        {/* Header with sort */}
        <div className="section">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
            <div>
              <h2 style={{ fontSize: '18px', fontWeight: 'bold' }}>
                Search Results {query && `for "${query}"`}
              </h2>
              <p style={{ fontSize: '12px', color: '#666', marginTop: '4px' }}>
                1–20 of {resultCount} results
              </p>
            </div>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              style={{
                padding: '8px 12px',
                border: '1px solid #ddd',
                borderRadius: '4px',
                fontSize: '13px',
                cursor: 'pointer'
              }}
            >
              <option value="featured">Featured</option>
              <option value="price-low">Price: Low to High</option>
              <option value="price-high">Price: High to Low</option>
              <option value="rating">Avg. Customer Review</option>
              <option value="newest">Newest Arrivals</option>
            </select>
          </div>
        </div>

        {/* Product Grid */}
        <div className="product-grid" style={{ marginTop: '16px' }}>
          {products.length > 0 ? (
            products.map(product => (
              <Link key={product.id} to={`/product/${product.id}`} style={{ textDecoration: 'none' }}>
                <div className="product-card">
                  <div className="product-image">
                    {product.image_url ? (
                      <img
                        src={product.image_url}
                        alt={product.name}
                        style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                      />
                    ) : (
                      <div style={{ fontSize: '48px', display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%' }}>
                        🛍️
                      </div>
                    )}
                  </div>
                  <h3 className="product-name">{product.name}</h3>
                  <div className="product-rating">
                    <span className="stars">★★★★★</span>
                    <span className="count">(245)</span>
                  </div>
                  <div className="product-price">
                    <span>₹{product.price}</span>
                    <span className="original">₹{Math.round(product.price * 1.2)}</span>
                  </div>
                  <div className="product-prime">✓ Free Delivery</div>
                  <button
                    className="product-add-btn"
                    onClick={(e) => {
                      e.preventDefault();
                      e.stopPropagation();
                      addToCart(product, 1);
                    }}
                  >
                    Add to Cart
                  </button>
                </div>
              </Link>
            ))
          ) : (
            <div style={{ gridColumn: '1 / -1', textAlign: 'center', padding: '48px 0' }}>
              <p style={{ color: '#666' }}>No products found</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
