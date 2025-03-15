import { createRouter, createWebHistory } from 'vue-router';
import Home from '@/views/Home.vue';

// Entry Components
import SignUp from '@/components/Entry/SignUp.vue';
import Login from '@/components/Entry/Login.vue';

// Customer Components
import CustomerSignUp from '@/components/Customer/CustomerSignUp.vue';
import CustomerLogIn from '@/components/Customer/CustomerLogIn.vue';
import CustomerProfile from '@/components/Customer/CustomerProfile.vue';

// Seller Components
import SellerSignUp from '@/components/Seller/SellerSignUp.vue';
import SellerLogIn from '@/components/Seller/SellerLogIn.vue';
import SellerProfile from '@/components/Seller/SellerProfile.vue';

// Delivery Components
import DeliverySignUp from '@/components/Delivery/DeliverySignUp.vue';
import DeliveryLogIn from '@/components/Delivery/DeliveryLogIn.vue';
import DeliveryProfile from '@/components/Delivery/DeliveryProfile.vue';

const routes = [
  { path: '/', name: 'Home', component: Home },

  // Entry Routes
  { path: '/signup', name: 'SignUp', component: SignUp },
  { path: '/login', name: 'Login', component: Login },

  // Customer Routes
  { path: '/customer/signup', name: 'CustomerSignUp', component: CustomerSignUp },
  { path: '/customer/login', name: 'CustomerLogIn', component: CustomerLogIn },
  { path: "/customer/profile/:username", name: "CustomerProfile", component: CustomerProfile },

  // Seller Routes
  { path: '/seller/signup', name: 'SellerSignUp', component: SellerSignUp },
  { path: '/seller/login', name: 'SellerLogIn', component: SellerLogIn },
  { path: "/seller/profile/:storeName", name: "SellerProfile", component: SellerProfile },

  // Delivery Partner Routes
  { path: '/delivery/signup', name: 'DeliverySignUp', component: DeliverySignUp },
  { path: '/delivery/login', name: 'DeliveryLogIn', component: DeliveryLogIn },
  { path: "/delivery/profile/:username", name: "DeliveryProfile", component: DeliveryProfile },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;