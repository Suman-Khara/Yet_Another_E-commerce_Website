<template>
  <div class="menu-icon" @click="toggleDrawer">☰</div>
  <!-- Side Drawer -->
  <div class="side-drawer" v-if="isDrawerOpen">
    <ul>
      <li @click="navigateTo('/customer/profile/' + username)">Profile</li>
      <li @click="navigateTo('/customer/order-history')">Order History</li>
      <li @click="navigateTo('/customer/cart')">Cart</li>
      <li @click="navigateTo('/customer/products')">Product List</li>
      <li @click="logout">Log Out</li>
    </ul>
  </div>
  <div class="order-history-container">
    <h1>Order History</h1>
    <table v-if="orders.length > 0" class="order-table">
      <thead>
        <tr>
          <th>Order ID</th>
          <th>Items</th>
          <th>Total Amount ($)</th>
          <th>Address</th>
          <th>Payment Mode</th>
          <th>Created At</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="order in orders" :key="order.order_id">
          <td>{{ order.order_id }}</td>
          <td>
            <ul>
              <li v-for="item in order.items" :key="item.product_name">
                {{ `${item.product_name} (${item.count})` }}
              </li>
            </ul>
          </td>
          <td>{{ order.total_amount }}</td>
          <td>{{ order.address }}</td>
          <td>{{ order.payment_mode }}</td>
          <td>{{ new Date(order.created_at).toLocaleString() }}</td>
        </tr>
      </tbody>
    </table>
    <div v-else>No orders found.</div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      orders: [],
      isDrawerOpen: false,
      username: localStorage.getItem('username')
    }
  },
  methods: {
    async fetchOrders() {
      try {
        const token = localStorage.getItem('token')
        const response = await axios.get('http://127.0.0.1:8000/ecommerce/order-history/', {
          headers: { Authorization: `Token ${token}` }
        })
        this.orders = response.data.orders
      } catch (error) {
        console.error('Error fetching orders:', error)
        alert('Failed to fetch order history.')
      }
    },
    navigateTo(route) {
      this.$router.push(route);
      this.isDrawerOpen = false;
    },
    toggleDrawer() {
      this.isDrawerOpen = !this.isDrawerOpen;
    }
  },
  mounted() {
    this.fetchOrders()
  }
}
</script>

<style scoped>
.order-history-container {
  padding: 20px;
}

h1 {
  margin-bottom: 20px;
}

.order-table {
  width: 100%;
  border-collapse: collapse;
}

.order-table th, .order-table td {
  border: 1px solid #ccc;
  padding: 10px;
  text-align: center;
}

.order-table th {
  background-color: #345360;
}

ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.menu-icon {
  position: absolute;
  top: 70px;
  right: 10px;
  font-size: 2rem; /* Increased size */
  cursor: pointer;
}

.side-drawer {
  position: absolute;
  top: 110px; /* Slightly below the icon */
  right: 10px;
  width: 220px; /* Increased width */
  background-color: #222;
  color: white;
  padding: 1.5rem; /* More padding for better visibility */
  border-radius: 12px; /* More rounded edges */
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3); /* Deeper shadow for effect */
}

.side-drawer ul {
  list-style-type: none;
  padding: 0;
}

.side-drawer li {
  padding: 12px;
  cursor: pointer;
  border-bottom: 1px solid #444;
}

.side-drawer li:hover {
  background-color: #555;
}

</style>
