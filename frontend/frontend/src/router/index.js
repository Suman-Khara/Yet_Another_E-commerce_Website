import { createRouter, createWebHistory } from 'vue-router';
import Home from '@/views/Home.vue';

// Entry Components
import SignUp from '@/components/Entry/SignUp.vue';
import Login from '@/components/Entry/Login.vue';

// Customer Components
import CustomerSignUp from '@/components/Customer/CustomerSignUp.vue';
import CustomerLogIn from '@/components/Customer/CustomerLogIn.vue';
import CustomerProfile from '@/components/Customer/CustomerProfile.vue';
import Cart from '@/components/Customer/Cart.vue';
import OrderHistory from '@/components/Customer/OrderHistory.vue';
import ProductDetails from '@/components/Customer/ProductDetails.vue';
import ProductList from '@/components/Customer/ProductList.vue';

// Seller Components
import SellerSignUp from '@/components/Seller/SellerSignUp.vue';
import SellerLogIn from '@/components/Seller/SellerLogIn.vue';
import SellerProfile from '@/components/Seller/SellerProfile.vue';
import AddProduct from '@/components/Seller/AddProduct.vue';
import SellerDashboard from '@/components/Seller/Dashboard.vue';
import EditProduct from '@/components/Seller/EditProduct.vue';
import SellerOrderHistory from '@/components/Seller/OrderHistory.vue';
import OrderRequests from '@/components/Seller/OrderRequests.vue';

// Delivery Components
import DeliverySignUp from '@/components/Delivery/DeliverySignUp.vue';
import DeliveryLogIn from '@/components/Delivery/DeliveryLogIn.vue';
import DeliveryProfile from '@/components/Delivery/DeliveryProfile.vue';
import DeliveryDashboard from '@/components/Delivery/Dashboard.vue';
import DeliveryHistory from '@/components/Delivery/DeliveryHistory.vue';
import OrderDetails from '@/components/Delivery/OrderDetails.vue';

const routes = [
  { path: '/', name: 'Home', component: Home },

  // Entry Routes
  { path: '/signup', name: 'SignUp', component: SignUp },
  { path: '/login', name: 'Login', component: Login },

  // Customer Routes
  { path: '/customer/signup', name: 'CustomerSignUp', component: CustomerSignUp },
  { path: '/customer/login', name: 'CustomerLogIn', component: CustomerLogIn },
  { path: "/customer/profile/:username", name: "CustomerProfile", component: CustomerProfile },
  { path: '/customer/cart', name: 'Cart', component: Cart },
  { path: '/customer/order-history', name: 'OrderHistory', component: OrderHistory },
  { path: '/customer/products', name: 'ProductList', component: ProductList },
  { path: '/customer/products/:id', name: 'ProductDetails', component: ProductDetails },

  // Seller Routes
  { path: '/seller/signup', name: 'SellerSignUp', component: SellerSignUp },
  { path: '/seller/login', name: 'SellerLogIn', component: SellerLogIn },
  { path: "/seller/profile/:storeName", name: "SellerProfile", component: SellerProfile },
  { path: '/seller/dashboard', name: 'SellerDashboard', component: SellerDashboard },
  { path: '/seller/add-product', name: 'AddProduct', component: AddProduct },
  { path: '/seller/edit-product/:id', name: 'EditProduct', component: EditProduct },
  { path: '/seller/order-history', name: 'SellerOrderHistory', component: SellerOrderHistory },
  { path: '/seller/order-requests', name: 'OrderRequests', component: OrderRequests },

  // Delivery Partner Routes
  { path: '/delivery/signup', name: 'DeliverySignUp', component: DeliverySignUp },
  { path: '/delivery/login', name: 'DeliveryLogIn', component: DeliveryLogIn },
  { path: "/delivery/profile/:username", name: "DeliveryProfile", component: DeliveryProfile },
  { path: '/delivery/dashboard', name: 'DeliveryDashboard', component: DeliveryDashboard },
  { path: '/delivery/history', name: 'DeliveryHistory', component: DeliveryHistory },
  { path: '/delivery/order-details/:id', name: 'OrderDetails', component: OrderDetails },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;