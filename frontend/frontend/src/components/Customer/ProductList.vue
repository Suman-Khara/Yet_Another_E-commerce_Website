<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const searchQuery = ref('')
const isDrawerOpen = ref(false)
const products = ref([])
const errorMessage = ref('')

const fetchProducts = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/ecommerce/products/')
    products.value = response.data
  } catch (error) {
    console.error('Error fetching products:', error)
    errorMessage.value = 'Failed to load products. Please try again later.'
  }
}

onMounted(fetchProducts)

const filteredProducts = computed(() => {
  return products.value.filter(product => {
    const query = searchQuery.value.toLowerCase()
    return (
      product.name.toLowerCase().includes(query) ||
      product.category.toLowerCase().includes(query) ||
      (product.tags?.some(tag => tag.toLowerCase().includes(query)) ?? false)
    )
  })
})

const username = localStorage.getItem('username')
console.log('Username:', username)
const navigateTo = (path) => {
  if (path.includes('/customer/profile/')) {
    if (username) {
      router.push(`/customer/profile/${username}`)
    } else {
      console.error('Username not available')
    }
  } else {
    router.push(path)
  }
}

const navigateToProduct = (id) => {
  router.push(`/customer/products/${id}`)
}

const logout = () => {
  console.log('Logging out...')
}
</script>

<template>
  <div class="container">
    <!-- Top Section -->
    <div class="header">
      <h2>Product List</h2>
    </div>
    
    <div class="menu-icon" @click="isDrawerOpen = !isDrawerOpen">☰</div>
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

    <!-- Error Message -->
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

    <!-- Search Bar -->
    <input 
      type="text" 
      v-model="searchQuery" 
      placeholder="Search products..."
      class="search-bar"
    />

    <!-- Product List -->
    <div class="product-list" v-if="filteredProducts.length">
      <div 
        v-for="product in filteredProducts" 
        :key="product.product_id" 
        class="product-card"
        @click="navigateToProduct(product.product_id)"
      >
        <img :src="product.image_url" :alt="product.name" class="product-image" loading="lazy"/>
        <div class="product-info">
          <h3 class="product-name">{{ product.name }}</h3>
          <p v-if="product.discount" class="old-price">${{ product.price }}</p>
          <p class="new-price">
            ${{ product.discount ? (product.price * (1 - product.discount / 100)).toFixed(2) : product.price }}
          </p>
          <p class="stock">In Stock: {{ product.stock }}</p>
        </div>
      </div>
    </div>
    <p v-else-if="!errorMessage">No products found.</p>
  </div>
</template>

<style scoped>
.container {
  width: 90%;
  max-width: 1200px;
  margin: auto;
  padding-top: 80px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

h2 {
  text-align: center;
  flex: 1;
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

.search-bar {
  width: 100%;
  padding: 0.8rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 5px;
  margin-bottom: 1rem;
}

.error-message {
  color: red;
  margin-bottom: 1rem;
}

.product-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.product-card {
  display: flex;
  align-items: center;
  background: #f0f0f0db;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  cursor: pointer;
}

.product-card:hover {
  background: #e0e0e0;
}

.product-image {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 8px;
  margin-right: 1rem;
}

.product-info {
  flex: 1;
}

.product-name {
  font-size: 1.2rem;
  font-weight: bold;
  color: black;
}

.old-price {
  text-decoration: line-through;
  color: red;
}

.new-price {
  font-size: 1.1rem;
  font-weight: bold;
  color: green;
}

.stock {
  font-size: 0.9rem;
  color: #555;
}
</style>
