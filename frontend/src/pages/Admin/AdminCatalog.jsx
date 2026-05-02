import { useState } from 'react';

const CATALOG = {
  'Electronics': {
    icon: '📱',
    subcategories: {
      'Smartphones': [
        { id: 'ELEC-001', name: 'iPhone 15 Pro', price: 79999, stock: 25 },
        { id: 'ELEC-002', name: 'Samsung Galaxy S24', price: 74999, stock: 18 },
        { id: 'ELEC-003', name: 'Google Pixel 8', price: 59999, stock: 22 },
        { id: 'ELEC-004', name: 'OnePlus 12', price: 54999, stock: 30 },
        { id: 'ELEC-005', name: 'Xiaomi 14 Ultra', price: 49999, stock: 28 }
      ],
      'Laptops': [
        { id: 'ELEC-006', name: 'MacBook Pro M3', price: 149999, stock: 12 },
        { id: 'ELEC-007', name: 'Dell XPS 15', price: 129999, stock: 15 },
        { id: 'ELEC-008', name: 'HP Pavilion 15', price: 59999, stock: 20 },
        { id: 'ELEC-009', name: 'Lenovo ThinkPad', price: 74999, stock: 17 },
        { id: 'ELEC-010', name: 'ASUS VivoBook', price: 54999, stock: 25 }
      ],
      'Tablets': [
        { id: 'ELEC-011', name: 'iPad Pro 12.9"', price: 89999, stock: 14 },
        { id: 'ELEC-012', name: 'Samsung Galaxy Tab S9', price: 64999, stock: 19 },
        { id: 'ELEC-013', name: 'iPad Air', price: 59999, stock: 21 },
        { id: 'ELEC-014', name: 'Lenovo Tab P11', price: 34999, stock: 26 },
        { id: 'ELEC-015', name: 'Microsoft Surface Go', price: 49999, stock: 16 }
      ],
      'Accessories': [
        { id: 'ELEC-016', name: 'USB-C Cable', price: 499, stock: 100 },
        { id: 'ELEC-017', name: 'Phone Stand', price: 799, stock: 85 },
        { id: 'ELEC-018', name: 'Screen Protector', price: 399, stock: 120 },
        { id: 'ELEC-019', name: 'Phone Case', price: 599, stock: 95 },
        { id: 'ELEC-020', name: 'Charging Dock', price: 1499, stock: 45 }
      ],
      'Audio': [
        { id: 'ELEC-021', name: 'Sony WH-1000XM5', price: 29999, stock: 18 },
        { id: 'ELEC-022', name: 'Bose QC45', price: 34999, stock: 12 },
        { id: 'ELEC-023', name: 'JBL Flip 6', price: 14999, stock: 35 },
        { id: 'ELEC-024', name: 'Apple AirPods Pro', price: 24999, stock: 28 },
        { id: 'ELEC-025', name: 'Samsung Galaxy Buds', price: 12999, stock: 40 }
      ]
    }
  },
  'Fashion': {
    icon: '👕',
    subcategories: {
      'Men': [
        { id: 'FASH-001', name: 'Cotton T-Shirt', price: 799, stock: 150 },
        { id: 'FASH-002', name: 'Denim Jeans', price: 2499, stock: 80 },
        { id: 'FASH-003', name: 'Formal Shirt', price: 1999, stock: 65 },
        { id: 'FASH-004', name: 'Blazer', price: 5999, stock: 30 },
        { id: 'FASH-005', name: 'Casual Shorts', price: 1299, stock: 95 }
      ],
      'Women': [
        { id: 'FASH-006', name: 'Cotton Saree', price: 2999, stock: 45 },
        { id: 'FASH-007', name: 'Kurti', price: 1499, stock: 70 },
        { id: 'FASH-008', name: 'Salwar Suit', price: 3499, stock: 55 },
        { id: 'FASH-009', name: 'Ethnic Dress', price: 4999, stock: 38 },
        { id: 'FASH-010', name: 'Top', price: 999, stock: 120 }
      ],
      'Kids': [
        { id: 'FASH-011', name: 'Kids T-Shirt', price: 599, stock: 110 },
        { id: 'FASH-012', name: 'Kids Shorts', price: 899, stock: 85 },
        { id: 'FASH-013', name: 'Kids Dress', price: 1299, stock: 60 },
        { id: 'FASH-014', name: 'Kids Jacket', price: 1999, stock: 45 },
        { id: 'FASH-015', name: 'Kids Hoodie', price: 1499, stock: 75 }
      ],
      'Shoes': [
        { id: 'FASH-016', name: 'Running Shoes', price: 4999, stock: 55 },
        { id: 'FASH-017', name: 'Sports Shoes', price: 3999, stock: 68 },
        { id: 'FASH-018', name: 'Casual Sneakers', price: 2999, stock: 78 },
        { id: 'FASH-019', name: 'Formal Shoes', price: 3499, stock: 42 },
        { id: 'FASH-020', name: 'Flip Flops', price: 599, stock: 130 }
      ],
      'Accessories': [
        { id: 'FASH-021', name: 'Leather Belt', price: 999, stock: 95 },
        { id: 'FASH-022', name: 'Scarf', price: 699, stock: 110 },
        { id: 'FASH-023', name: 'Sunglasses', price: 1999, stock: 75 },
        { id: 'FASH-024', name: 'Watch', price: 3999, stock: 48 },
        { id: 'FASH-025', name: 'Bag', price: 2499, stock: 62 }
      ]
    }
  },
  'Home & Kitchen': {
    icon: '🏠',
    subcategories: {
      'Kitchen': [
        { id: 'HOME-001', name: 'Stainless Steel Pan Set', price: 2999, stock: 35 },
        { id: 'HOME-002', name: 'Non-Stick Cookware', price: 3499, stock: 28 },
        { id: 'HOME-003', name: 'Mixing Bowls Set', price: 899, stock: 65 },
        { id: 'HOME-004', name: 'Knife Set', price: 1999, stock: 48 },
        { id: 'HOME-005', name: 'Cutting Board', price: 499, stock: 90 }
      ],
      'Bedding': [
        { id: 'HOME-006', name: 'Cotton Bed Sheet', price: 1299, stock: 55 },
        { id: 'HOME-007', name: 'Pillow Set', price: 1999, stock: 42 },
        { id: 'HOME-008', name: 'Comforter', price: 3999, stock: 30 },
        { id: 'HOME-009', name: 'Mattress Protector', price: 899, stock: 70 },
        { id: 'HOME-010', name: 'Blanket', price: 1499, stock: 58 }
      ],
      'Furniture': [
        { id: 'HOME-011', name: 'Wooden Chair', price: 4999, stock: 25 },
        { id: 'HOME-012', name: 'Dining Table', price: 12999, stock: 12 },
        { id: 'HOME-013', name: 'Bookshelf', price: 7999, stock: 18 },
        { id: 'HOME-014', name: 'Sofa', price: 24999, stock: 8 },
        { id: 'HOME-015', name: 'Side Table', price: 3999, stock: 35 }
      ],
      'Decor': [
        { id: 'HOME-016', name: 'Wall Art', price: 1999, stock: 45 },
        { id: 'HOME-017', name: 'Throw Pillows', price: 799, stock: 80 },
        { id: 'HOME-018', name: 'Curtains', price: 2499, stock: 38 },
        { id: 'HOME-019', name: 'Plant Pot', price: 599, stock: 95 },
        { id: 'HOME-020', name: 'Mirror', price: 1999, stock: 52 }
      ],
      'Appliances': [
        { id: 'HOME-021', name: 'Microwave Oven', price: 8999, stock: 20 },
        { id: 'HOME-022', name: 'Toaster', price: 1999, stock: 48 },
        { id: 'HOME-023', name: 'Coffee Maker', price: 2999, stock: 35 },
        { id: 'HOME-024', name: 'Blender', price: 3499, stock: 42 },
        { id: 'HOME-025', name: 'Vacuum Cleaner', price: 12999, stock: 15 }
      ]
    }
  },
  'Books': {
    icon: '📚',
    subcategories: {
      'Fiction': [
        { id: 'BOOK-001', name: 'The Great Gatsby', price: 399, stock: 75 },
        { id: 'BOOK-002', name: 'To Kill a Mockingbird', price: 349, stock: 68 },
        { id: 'BOOK-003', name: '1984', price: 399, stock: 82 },
        { id: 'BOOK-004', name: 'Pride and Prejudice', price: 349, stock: 71 },
        { id: 'BOOK-005', name: 'The Hobbit', price: 449, stock: 65 }
      ],
      'Non-Fiction': [
        { id: 'BOOK-006', name: 'Atomic Habits', price: 449, stock: 58 },
        { id: 'BOOK-007', name: 'Thinking Fast and Slow', price: 599, stock: 42 },
        { id: 'BOOK-008', name: 'Sapiens', price: 549, stock: 51 },
        { id: 'BOOK-009', name: 'The Innovators', price: 499, stock: 38 },
        { id: 'BOOK-010', name: 'Educated', price: 449, stock: 55 }
      ],
      'Educational': [
        { id: 'BOOK-011', name: 'Math Textbook', price: 299, stock: 95 },
        { id: 'BOOK-012', name: 'Science Guide', price: 349, stock: 85 },
        { id: 'BOOK-013', name: 'English Grammar', price: 279, stock: 105 },
        { id: 'BOOK-014', name: 'History Notes', price: 249, stock: 78 },
        { id: 'BOOK-015', name: 'Coding Basics', price: 399, stock: 62 }
      ],
      'Comics': [
        { id: 'BOOK-016', name: 'Manga Vol 1', price: 299, stock: 65 },
        { id: 'BOOK-017', name: 'Graphic Novel', price: 499, stock: 45 },
        { id: 'BOOK-018', name: 'Comic Series', price: 199, stock: 88 },
        { id: 'BOOK-019', name: 'Anime Comics', price: 349, stock: 52 },
        { id: 'BOOK-020', name: 'Adventure Comics', price: 279, stock: 70 }
      ],
      'Reference': [
        { id: 'BOOK-021', name: 'Dictionary', price: 599, stock: 35 },
        { id: 'BOOK-022', name: 'Encyclopedia', price: 799, stock: 25 },
        { id: 'BOOK-023', name: 'Atlas', price: 499, stock: 40 },
        { id: 'BOOK-024', name: 'Thesaurus', price: 449, stock: 38 },
        { id: 'BOOK-025', name: 'Almanac', price: 349, stock: 48 }
      ]
    }
  },
  'Sports': {
    icon: '⚽',
    subcategories: {
      'Equipment': [
        { id: 'SPORT-001', name: 'Football', price: 799, stock: 65 },
        { id: 'SPORT-002', name: 'Cricket Bat', price: 2999, stock: 42 },
        { id: 'SPORT-003', name: 'Tennis Racket', price: 3999, stock: 28 },
        { id: 'SPORT-004', name: 'Basketball', price: 999, stock: 55 },
        { id: 'SPORT-005', name: 'Badminton Set', price: 1499, stock: 38 }
      ],
      'Apparel': [
        { id: 'SPORT-006', name: 'Sports Jersey', price: 1299, stock: 85 },
        { id: 'SPORT-007', name: 'Gym Shorts', price: 899, stock: 95 },
        { id: 'SPORT-008', name: 'Sports Bra', price: 1499, stock: 65 },
        { id: 'SPORT-009', name: 'Track Pants', price: 1999, stock: 48 },
        { id: 'SPORT-010', name: 'Compression Wear', price: 1699, stock: 52 }
      ],
      'Outdoor': [
        { id: 'SPORT-011', name: 'Tent', price: 4999, stock: 20 },
        { id: 'SPORT-012', name: 'Camping Bag', price: 3499, stock: 25 },
        { id: 'SPORT-013', name: 'Sleeping Bag', price: 2999, stock: 32 },
        { id: 'SPORT-014', name: 'Hiking Boot', price: 3999, stock: 38 },
        { id: 'SPORT-015', name: 'Backpack', price: 2499, stock: 45 }
      ],
      'Fitness': [
        { id: 'SPORT-016', name: 'Dumbbell Set', price: 3999, stock: 35 },
        { id: 'SPORT-017', name: 'Resistance Band', price: 499, stock: 120 },
        { id: 'SPORT-018', name: 'Yoga Mat', price: 899, stock: 85 },
        { id: 'SPORT-019', name: 'Jump Rope', price: 299, stock: 95 },
        { id: 'SPORT-020', name: 'Fitness Tracker', price: 4999, stock: 42 }
      ],
      'Games': [
        { id: 'SPORT-021', name: 'Board Game', price: 999, stock: 65 },
        { id: 'SPORT-022', name: 'Chess Set', price: 1499, stock: 48 },
        { id: 'SPORT-023', name: 'Puzzle Game', price: 599, stock: 78 },
        { id: 'SPORT-024', name: 'Card Game', price: 299, stock: 95 },
        { id: 'SPORT-025', name: 'Video Game Console', price: 34999, stock: 15 }
      ]
    }
  },
  'Beauty': {
    icon: '💄',
    subcategories: {
      'Skincare': [
        { id: 'BEAUTY-001', name: 'Face Wash', price: 399, stock: 95 },
        { id: 'BEAUTY-002', name: 'Moisturizer', price: 699, stock: 75 },
        { id: 'BEAUTY-003', name: 'Face Mask', price: 299, stock: 110 },
        { id: 'BEAUTY-004', name: 'Sunscreen', price: 499, stock: 85 },
        { id: 'BEAUTY-005', name: 'Serum', price: 899, stock: 62 }
      ],
      'Makeup': [
        { id: 'BEAUTY-006', name: 'Foundation', price: 599, stock: 72 },
        { id: 'BEAUTY-007', name: 'Lipstick', price: 399, stock: 95 },
        { id: 'BEAUTY-008', name: 'Eyeshadow Palette', price: 899, stock: 48 },
        { id: 'BEAUTY-009', name: 'Mascara', price: 349, stock: 88 },
        { id: 'BEAUTY-010', name: 'Blush', price: 449, stock: 78 }
      ],
      'Haircare': [
        { id: 'BEAUTY-011', name: 'Shampoo', price: 299, stock: 105 },
        { id: 'BEAUTY-012', name: 'Conditioner', price: 329, stock: 98 },
        { id: 'BEAUTY-013', name: 'Hair Oil', price: 199, stock: 125 },
        { id: 'BEAUTY-014', name: 'Hair Mask', price: 449, stock: 65 },
        { id: 'BEAUTY-015', name: 'Hair Serum', price: 379, stock: 82 }
      ],
      'Fragrance': [
        { id: 'BEAUTY-016', name: 'Perfume', price: 1999, stock: 42 },
        { id: 'BEAUTY-017', name: 'Body Spray', price: 399, stock: 95 },
        { id: 'BEAUTY-018', name: 'Cologne', price: 1499, stock: 52 },
        { id: 'BEAUTY-019', name: 'Deodorant', price: 249, stock: 110 },
        { id: 'BEAUTY-020', name: 'Fragrance Oil', price: 599, stock: 68 }
      ],
      'Wellness': [
        { id: 'BEAUTY-021', name: 'Vitamin Supplement', price: 449, stock: 78 },
        { id: 'BEAUTY-022', name: 'Protein Powder', price: 999, stock: 55 },
        { id: 'BEAUTY-023', name: 'Multivitamin', price: 399, stock: 92 },
        { id: 'BEAUTY-024', name: 'Herbal Tea', price: 299, stock: 85 },
        { id: 'BEAUTY-025', name: 'Wellness Drink', price: 599, stock: 72 }
      ]
    }
  }
};

export default function AdminCatalog() {
  const [expandedCategory, setExpandedCategory] = useState(null);
  const [expandedSubcategory, setExpandedSubcategory] = useState(null);

  const getCategoryKey = (category, subcategory) => `${category}__${subcategory}`;

  return (
    <div style={{ padding: '24px' }}>
      <h1 style={{ fontSize: '28px', fontWeight: 'bold', marginBottom: '24px' }}>Catalog</h1>

      <div style={{ background: '#FFFFFF', borderRadius: '4px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
        {Object.entries(CATALOG).map(([categoryName, categoryData]) => (
          <div key={categoryName} style={{ borderBottom: '1px solid #f0f0f0' }}>
            {/* Category Header */}
            <div
              onClick={() => setExpandedCategory(expandedCategory === categoryName ? null : categoryName)}
              style={{
                padding: '16px',
                cursor: 'pointer',
                background: expandedCategory === categoryName ? '#f9f9f9' : 'transparent',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                borderLeft: expandedCategory === categoryName ? '4px solid #FF9900' : '4px solid transparent',
                transition: 'all 0.2s'
              }}
              onMouseEnter={(e) => e.currentTarget.style.background = '#f9f9f9'}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = expandedCategory === categoryName ? '#f9f9f9' : 'transparent';
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                <span style={{ fontSize: '20px' }}>{categoryData.icon}</span>
                <span style={{ fontSize: '15px', fontWeight: 'bold', color: '#111' }}>{categoryName}</span>
              </div>
              <span style={{ fontSize: '12px', color: '#666' }}>
                {expandedCategory === categoryName ? '▼' : '▶'}
              </span>
            </div>

            {/* Subcategories */}
            {expandedCategory === categoryName && (
              <div style={{ background: '#fafafa' }}>
                {Object.entries(categoryData.subcategories).map(([subcategoryName, subProducts]) => {
                  const subKey = getCategoryKey(categoryName, subcategoryName);
                  const isExpanded = expandedSubcategory === subKey;

                  return (
                    <div key={subcategoryName} style={{ borderTop: '1px solid #f0f0f0' }}>
                      {/* Subcategory Header */}
                      <div
                        onClick={() => setExpandedSubcategory(isExpanded ? null : subKey)}
                        style={{
                          padding: '12px 16px 12px 32px',
                          cursor: 'pointer',
                          background: isExpanded ? '#f0f0f0' : 'transparent',
                          display: 'flex',
                          justifyContent: 'space-between',
                          alignItems: 'center',
                          transition: 'all 0.2s'
                        }}
                        onMouseEnter={(e) => e.currentTarget.style.background = '#f0f0f0'}
                        onMouseLeave={(e) => {
                          e.currentTarget.style.background = isExpanded ? '#f0f0f0' : 'transparent';
                        }}
                      >
                        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                          <span style={{ fontSize: '13px', fontWeight: '600', color: '#333' }}>
                            {subcategoryName}
                          </span>
                          <span style={{ fontSize: '11px', color: '#999', background: '#e0e0e0', padding: '2px 6px', borderRadius: '2px' }}>
                            {subProducts.length}
                          </span>
                        </div>
                        <span style={{ fontSize: '11px', color: '#666' }}>
                          {isExpanded ? '▼' : '▶'}
                        </span>
                      </div>

                      {/* Products List */}
                      {isExpanded && (
                        <div style={{ background: '#FFFFFF', borderLeft: '3px solid #FF9900', marginLeft: '32px' }}>
                          {subProducts.length > 0 ? (
                            <div style={{ padding: '0' }}>
                              <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                                <thead>
                                  <tr style={{ borderBottom: '1px solid #f0f0f0', background: '#f9f9f9' }}>
                                    <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: '12px', fontWeight: 'bold' }}>Product ID</th>
                                    <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: '12px', fontWeight: 'bold' }}>Name</th>
                                    <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: '12px', fontWeight: 'bold' }}>Price</th>
                                    <th style={{ padding: '12px 16px', textAlign: 'center', fontSize: '12px', fontWeight: 'bold' }}>Action</th>
                                  </tr>
                                </thead>
                                <tbody>
                                  {subProducts.map(product => (
                                    <tr key={product.id} style={{ borderBottom: '1px solid #f0f0f0' }}>
                                      <td style={{ padding: '12px 16px', fontSize: '11px', color: '#666' }}>{product.id}</td>
                                      <td style={{ padding: '12px 16px', fontSize: '12px', fontWeight: '500' }}>{product.name}</td>
                                      <td style={{ padding: '12px 16px', fontSize: '12px', fontWeight: 'bold', color: '#FF9900' }}>₹{product.price}</td>
                                      <td style={{ padding: '12px 16px', textAlign: 'center' }}>
                                        <button
                                          style={{
                                            background: 'none',
                                            border: 'none',
                                            color: '#B12704',
                                            cursor: 'pointer',
                                            fontSize: '12px',
                                            textDecoration: 'underline',
                                            fontWeight: 'bold'
                                          }}
                                        >
                                          Edit
                                        </button>
                                      </td>
                                    </tr>
                                  ))}
                                </tbody>
                              </table>
                            </div>
                          ) : (
                            <div style={{ padding: '16px', textAlign: 'center', color: '#999', fontSize: '12px' }}>
                              No products in this subcategory
                            </div>
                          )}
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Summary */}
      <div style={{ marginTop: '24px', padding: '16px', background: '#FFFFFF', borderRadius: '4px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
        <p style={{ fontSize: '13px', color: '#666' }}>
          <strong>Summary:</strong> {Object.keys(CATALOG).length} categories with {Object.values(CATALOG).reduce((sum, cat) => sum + Object.keys(cat.subcategories).length, 0)} subcategories • 150 total products
        </p>
      </div>
    </div>
  );
}
