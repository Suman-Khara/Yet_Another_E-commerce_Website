<template>
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
      <h3>Checkout</h3>
      
      <label>Address:</label>
      <input type="text" v-model="checkoutAddress" />
      <button @click="useMyAddress">My Address</button>
      
      <label>Mode of Payment:</label>
      <select v-model="paymentMode">
        <option>UPI</option>
        <option>Cash on Delivery</option>
        <option>Card</option>
      </select>
      
      <button @click="placeOrder">Order Now</button>
      <button @click="isCheckoutModalOpen = false">Cancel</button>
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
      paymentMode: 'UPI',
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
    async useMyAddress() {
      try {
        const token = localStorage.getItem('token')
        const response = await axios.get('http://127.0.0.1:8000/cart/my-address/', {
          headers: { Authorization: `Token ${token}` }
        })
        this.checkoutAddress = response.data.address
      } catch (error) {
        console.error('Error fetching address:', error)
        alert('Failed to fetch address.')
      }
    },
    async placeOrder() {
      if (!this.checkoutAddress.trim()) {
        alert('Please provide a valid address.')
        return
      }
      
      try {
        const token = localStorage.getItem('token')
        await axios.post('http://127.0.0.1:8000/cart/checkout/', {
          address: this.checkoutAddress,
          payment_mode: this.paymentMode
        }, {
          headers: { Authorization: `Token ${token}` }
        })
        alert('Order placed successfully!')
        this.cartItems = []
        this.isCheckoutModalOpen = false
      } catch (error) {
        console.error('Error placing order:', error)
        alert(error.response?.data?.error || 'Failed to place order.')
      }
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

.checkout-modal {
  position: fixed;
  top: 20%;
  left: 30%;
  width: 40%;
  background-color: grey;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.checkout-modal button {
  margin-top: 10px;
  padding: 10px;
  cursor: pointer;
}
</style>