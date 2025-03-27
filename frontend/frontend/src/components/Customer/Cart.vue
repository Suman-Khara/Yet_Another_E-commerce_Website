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
  <div class="cart-container">
    <!-- Left Section: Cart Items -->
    <div class="cart-items">
      <div v-if="cartItems.length === 0">Your cart is empty.</div>
      <div v-else>
        <div v-for="item in cartItems" :key="item.id" class="cart-item-card">
          <div class="product-info">
            <span class="product-name">{{ item.product_name }}</span>
            <span class="product-price">${{ item.total_price }}</span>
          </div>
          <div class="quantity-control">
            <button @click="updateQuantity(item.product_id, item.quantity - 1)" :disabled="item.quantity <= 1">-</button>
            <span>{{ item.quantity }}</span>
            <button @click="updateQuantity(item.product_id, item.quantity + 1)" :disabled="item.quantity >= item.stock">+</button>
            <button class="delete-button" @click="removeItem(item.product_id)">Delete</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Right Section: Total and Checkout -->
    <div class="cart-summary">
      <h2>Total: ${{ totalAmount }}</h2>
      <button class="checkout-button" @click="checkout">Checkout</button>
    </div>

    <!-- Checkout Modal -->
    <div v-if="isCheckoutModalOpen" class="checkout-modal">
      <h1>Checkout</h1>

      <!-- Address Input -->
      <label for="address">Address:</label>
      <input id="address" type="text" v-model="checkoutAddress" placeholder="Enter your address" />

      <!-- Payment Mode Selection -->
      <div class="payment-mode">
        <label>Mode of Payment:</label>
        <div>
          <input type="radio" id="card" value="CARD" v-model="paymentMode" />
          <label for="card">Card</label>
          <input type="radio" id="cash" value="COD" v-model="paymentMode" />
          <label for="cash">Cash on Delivery</label>
          <input type="radio" id="upi" value="UPI" v-model="paymentMode" />
          <label for="upi">UPI</label>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="modal-buttons">
        <button class="cancel-button" @click="isCheckoutModalOpen = false">Cancel</button>
        <button class="place-order-button" @click="placeOrder">Place Order</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      cartItems: [],
      isCheckoutModalOpen: false,
      checkoutAddress: '',
      paymentMode: 'Card',
      isDrawerOpen: false,
      username: localStorage.getItem('username')
    }
  },
  computed: {
    totalAmount() {
      return this.cartItems.reduce((sum, item) => sum + item.total_price, 0)
    }
  },
  methods: {
    async fetchCart() {
      try {
        const token = localStorage.getItem('token')
        const response = await axios.get('http://127.0.0.1:8000/cart/', {
          headers: { Authorization: `Token ${token}` }
        })
        this.cartItems = response.data.cart_items
      } catch (error) {
        console.error('Error fetching cart:', error)
        alert('Failed to load cart.')
      }
    },
    async updateQuantity(productId, newQuantity) {
      try {
        const token = localStorage.getItem('token')
        await axios.post('http://127.0.0.1:8000/cart/update/', {
          product_id: productId,
          quantity: newQuantity
        }, {
          headers: { Authorization: `Token ${token}` }
        })
        this.fetchCart()
      } catch (error) {
        console.error('Error updating quantity:', error)
        alert(error.response?.data?.error || 'Failed to update quantity.')
      }
    },
    async removeItem(productId) {
      try {
        const token = localStorage.getItem('token')
        const response = await axios.post('http://127.0.0.1:8000/cart/remove/', {
          product_id: productId
        }, {
          headers: { Authorization: `Token ${token}` }
        })
        alert(response.data.message || 'Item removed from cart.')
        this.fetchCart()
      } catch (error) {
        console.error('Error removing item:', error)
        alert(error.response?.data?.error || 'Failed to remove item from cart.')
      }
    },
    checkout() {
      this.isCheckoutModalOpen = true
    },
    async placeOrder() {
      if (!this.checkoutAddress.trim()) {
        alert('Please provide a valid address.')
        return
      }

      try {
        const token = localStorage.getItem('token')
        const response = await axios.post('http://127.0.0.1:8000/cart/checkout/', {
          address: this.checkoutAddress,
          payment_mode: this.paymentMode
        }, {
          headers: { Authorization: `Token ${token}` }
        })
        alert(response.data.message || 'Order placed successfully!')
        this.cartItems = []
        this.isCheckoutModalOpen = false
      } catch (error) {
        console.error('Error placing order:', error)
        alert(error.response?.data?.error || 'Failed to place order.')
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
    this.fetchCart()
  }
}
</script>

<style scoped>
.cart-container {
  display: flex;
  justify-content: space-between;
  padding: 20px;
}

.cart-items {
  flex: 2;
  margin-right: 20px;
}

.cart-item-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f9f9f956;
  padding: 15px;
  margin-bottom: 10px;
  border-radius: 8px;
}

.product-info {
  display: flex;
  flex-direction: column;
}

.product-name {
  font-weight: bold;
}

.product-price {
  color: #ffffff;
}

.quantity-control button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 5px 12px;
  margin: 0 5px;
  border-radius: 5px;
  cursor: pointer;
}

.quantity-control button:disabled {
  background-color: #ccc;
}

.cart-summary {
  flex: 1;
  background: #ffffff49;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
}

h2 {
  margin-bottom: 20px;
}

/* Checkout Modal */
.checkout-modal {
  position: fixed;
  top: 20%;
  left: 30%;
  width: 40%;
  background-color: black;
  border-radius: 10px;
  padding: 30px;
  box-shadow: 0 4px 20px rgba(0, 255, 170, 1); /* Green shadow */
}

h1 {
  margin-bottom: 20px;
  font-size: 24px;
}

label {
  display: block;
  margin-bottom: 8px;
}

input[type="text"] {
  width: 100%;
  padding: 8px;
  margin-bottom: 15px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.payment-mode div {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

input[type="radio"] {
  margin-right: 5px;
}

.modal-buttons {
  display: flex;
  justify-content: space-between;
}

.cancel-button {
  background-color: #ccc;
  color: black;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.place-order-button {
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
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
