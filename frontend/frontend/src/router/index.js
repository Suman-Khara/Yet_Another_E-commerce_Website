import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import SignUp from '../components/SignUp.vue'
import CustomerSignUp from '../components/CustomerSignUp.vue'
import SellerSignUp from '../components/SellerSignUp.vue'
import DeliverySignUp from '../components/DeliverySignUp.vue'
import Login from '../components/Login.vue'
import CustomerLogIn from '../components/CustomerLogIn.vue'
import SellerLogIn from '../components/SellerLogIn.vue'
import DeliveryLogIn from '../components/DeliveryLogIn.vue'
import CustomerProfile from '../components/CustomerProfile.vue'
import SellerProfile from '../components/SellerProfile.vue'
import DeliveryProfile from '../components/DeliveryProfile.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/signup', name: 'SignUp', component: SignUp },
  { path: '/signup/customer', name: 'CustomerSignUp', component: CustomerSignUp },
  { path: '/signup/seller', name: 'SellerSignUp', component: SellerSignUp },
  { path: '/signup/delivery', name: 'DeliverySignUp', component: DeliverySignUp },
  { path: '/login', name: 'Login', component: Login },
  { path: '/login/customer', name: 'CustomerLogIn', component: CustomerLogIn },
  { path: '/login/seller', name: 'SellerLogIn', component: SellerLogIn },
  { path: '/login/delivery', name: 'DeliveryLogIn', component: DeliveryLogIn },
  {
    path: "/customer/profile/:username",
    name: "CustomerProfile",
    component: CustomerProfile
  },
  { path: '/profile/seller', name: 'SellerProfile', component: SellerProfile },
  { path: '/profile/delivery', name: 'DeliveryProfile', component: DeliveryProfile },
]
const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
