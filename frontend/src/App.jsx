import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './styles.css';
import { CartProvider } from './context/CartContext';
import { AuthProvider } from './context/AuthContext';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Search from './pages/Search';
import ProductDetail from './pages/ProductDetail';
import Cart from './pages/Cart';
import Checkout from './pages/Checkout';
import Login from './pages/Login';
import ForgotPassword from './pages/ForgotPassword';
import ResetPassword from './pages/ResetPassword';
import Orders from './pages/Orders';
import Account from './pages/Account';
import AdminLayout from './pages/Admin/AdminLayout';
import AdminDashboard from './pages/Admin/AdminDashboard';
import AdminProducts from './pages/Admin/AdminProducts';
import AdminOrders from './pages/Admin/AdminOrders';
import AdminCatalog from './pages/Admin/AdminCatalog';
import AdminPromotions from './pages/Admin/AdminPromotions';

function App() {
  return (
    <AuthProvider>
    <CartProvider>
      <Router>
        <Routes>
          {/* Admin Routes */}
          <Route
            path="/admin/*"
            element={
              <AdminLayout>
                <Routes>
                  <Route path="/" element={<AdminDashboard />} />
                  <Route path="/products" element={<AdminProducts />} />
                  <Route path="/orders" element={<AdminOrders />} />
                  <Route path="/catalog" element={<AdminCatalog />} />
                  <Route path="/promotions" element={<AdminPromotions />} />
                </Routes>
              </AdminLayout>
            }
          />

          {/* Store Routes */}
          <Route
            path="/*"
            element={
              <>
                <Navbar />
                <Routes>
                  <Route path="/" element={<Home />} />
                  <Route path="/search" element={<Search />} />
                  <Route path="/product/:id" element={<ProductDetail />} />
                  <Route path="/cart" element={<Cart />} />
                  <Route path="/checkout" element={<Checkout />} />
                  <Route path="/login" element={<Login />} />
                  <Route path="/forgot-password" element={<ForgotPassword />} />
                  <Route path="/reset-password" element={<ResetPassword />} />
                  <Route path="/orders" element={<Orders />} />
                  <Route path="/account" element={<Account />} />
                </Routes>
              </>
            }
          />
        </Routes>
      </Router>
    </CartProvider>
    </AuthProvider>
  );
}

export default App;
