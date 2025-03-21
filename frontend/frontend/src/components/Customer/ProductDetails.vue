<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const product = ref(null)
const errorMessage = ref('')
const userReview = ref(null)
const otherReviews = ref([])
const isReviewModalOpen = ref(false)
const newRating = ref(0)
const newComment = ref('')

const fetchProductDetails = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/ecommerce/products/${route.params.id}/`)
    product.value = response.data
    if (response.data.user_review) {
      userReview.value = response.data.user_review
    }
    otherReviews.value = response.data.other_reviews
  } catch (error) {
    console.error('Error fetching product details:', error)
    errorMessage.value = 'Failed to load product details.'
  }
}

const addToCart = async () => {
  try {
    const token = localStorage.getItem("token");
    const response = await axios.post('http://127.0.0.1:8000/cart/add/', {
      product_id: product.value.product_id
    }, {
      headers: { Authorization: `Token ${token}` },
      withCredentials: true
    });

    alert(response.data.message);
  } catch (error) {
    if (error.response && error.response.data.error) {
      alert(error.response.data.error); // Display specific error from the backend
    } else {
      console.error('Error adding to cart:', error);
      alert('Failed to add product to cart.');
    }
  }
};

const openReviewModal = () => {
  isReviewModalOpen.value = true
  if (userReview.value) {
    newRating.value = userReview.value.rating
    newComment.value = userReview.value.comment
  } else {
    newRating.value = 0
    newComment.value = ''
  }
}

const setRating = (star) => {
  newRating.value = star
}

const submitReview = async () => {
  try {
    await axios.post('http://127.0.0.1:8000/ecommerce/products/review/', {
      product_id: product.value.product_id,
      rating: newRating.value,
      comment: newComment.value
    }, { withCredentials: true })
    alert('Review submitted successfully!')
    isReviewModalOpen.value = false
    // Optionally, re-fetch product details here
  } catch (error) {
    console.error('Error submitting review:', error)
    alert('Failed to submit review.')
  }
}

onMounted(fetchProductDetails)

const testPost = async () => {
  try {
    // Change the URL if needed; ensure it matches your Django URL exactly
    const response = await axios.post('http://127.0.0.1:8000/ecommerce/test/', {
      sample: 'data',
      username: localStorage.getItem('username'),
      product_id: product.value.product_id
    }, {
      withCredentials: true,
      headers: {
        'Authorization': `Token ${localStorage.getItem('token')}`
      }
    })
    console.log('Response:', response.data)
    alert('POST request successful! Check the console for details.')
  } catch (error) {
    console.error('Error in test POST:', error)
    alert('Failed to send POST request.')
  }
}
</script>

<template>
  <div style="padding: 2rem; text-align: center;">
    <button @click="testPost">Test POST Request</button>
  </div>
  <div v-if="product" class="container">
    <div class="product-details">
      <!-- Left: Product Image -->
      <img :src="product.image_url || product.thumbnail_url" :alt="product.name" class="product-image" />
      
      <!-- Right: Product Info -->
      <div class="info">
        <h1>{{ product.name }}</h1>
        <p v-if="product.discount" class="old-price">${{ product.price }}</p>
        <p class="new-price">${{ (product.price * (1 - product.discount / 100)).toFixed(2) }} ({{ product.discount }}% off)</p>
        <p>{{ product.description }}</p>
        <p><strong>Category:</strong> {{ product.category }}</p>
        <p><strong>Tags:</strong> {{ product.tags.join(', ') }}</p>
        <p><strong>Seller:</strong> {{ product.store_name }}</p>
        <p><strong>Stock:</strong> {{ product.stock }}</p>
        <p>
          <strong>Average Rating:</strong> 
          {{ product.rating }} ★ ({{ product.total_reviews }} Reviews)
        </p>
        <button @click="addToCart" class="add-to-cart-btn">Add to Cart</button>
        <button @click="openReviewModal" class="review-btn">
          {{ userReview ? 'Edit Your Review' : 'Add Review' }}
        </button>
      </div>
    </div>

    <!-- User's Review -->
    <div v-if="userReview" class="review-section">
      <h3>Your Review</h3>
      <p><strong>Rating:</strong> {{ userReview.rating }} ★</p>
      <p>{{ userReview.comment }}</p>
    </div>

    <!-- Other Reviews -->
    <div class="review-section">
      <h3>Other Reviews</h3>
      <div v-if="otherReviews.length === 0">No reviews yet.</div>
      <div v-for="review in otherReviews" :key="review.id" class="review-card">
        <p><strong>{{ review.username }}</strong></p>
        <p>{{ review.rating }} ★ - <span>{{ new Date(review.created_at).toLocaleDateString() }}</span></p>
        <p>{{ review.comment }}</p>
      </div>
    </div>

    <!-- Review Modal -->
    <div v-if="isReviewModalOpen" class="modal">
      <div class="modal-content">
        <h3>{{ userReview ? 'Edit Your Review' : 'Add Review' }}</h3>
        
        <!-- Star Rating System -->
        <div class="rating-container">
          <span>{{ newRating }}</span>
          <div class="stars">
            <span 
              v-for="star in 5" 
              :key="star" 
              @click="setRating(star)" 
              :class="{ 'filled': star <= newRating }">
              ★
            </span>
          </div>
        </div>

        <!-- Comment Section -->
        <textarea v-model="newComment" placeholder="Leave a comment (optional)" />

        <!-- Action Buttons -->
        <div class="buttons">
          <button @click="submitReview">Submit</button>
          <button @click="isReviewModalOpen = false">Cancel</button>
        </div>
      </div>
    </div>

  </div>
  
  <p v-if="errorMessage">{{ errorMessage }}</p>
</template>

<style scoped>
.container {
  padding: 2rem;
}

.product-details {
  display: flex;
  gap: 2rem;
}

.product-image {
  width: 400px;
  height: 400px;
  object-fit: cover;
  border-radius: 12px;
}

.info {
  flex: 1;
}

h1 {
  font-size: 2.5rem;
}

.old-price {
  text-decoration: line-through;
  color: red;
}

.new-price {
  font-size: 1.5rem;
  color: green;
}

button {
  background: transparent; /* No default background */
  border: 2px solid #41b883; /* Vue green border */
  padding: 10px;
  font-size: 16px;
  font-family:
    Inter,
    -apple-system,
    BlinkMacSystemFont,
    'Segoe UI',
    Roboto,
    Oxygen,
    Ubuntu,
    Cantarell,
    'Fira Sans',
    'Droid Sans',
    'Helvetica Neue',
    sans-serif;
  color: white; /* Default text color */
  cursor: pointer;
  transition: color 0.3s ease-in-out, border-color 0.3s ease-in-out;
  border-radius: 5px;
  width: 100%;
}

button:hover {
  color: #b3a100; /* Change text color on hover */
  border-color: #b3a100; /* Keep border color consistent */
}

.review-section {
  margin-top: 3rem;
}

.review-card {
  background: #f0f0f038;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 1);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: transparent;
  padding: 2rem;
  width: 400px;
  border-radius: 12px;
  color: white;
  box-shadow: 0 4px 20px #b3a100;
  text-align: center;
}

.rating-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.stars span {
  font-size: 30px;
  color: #ccc;
  cursor: pointer;
  transition: color 0.3s;
}

.stars span.filled {
  color: #ffd700;
}

textarea {
  width: 100%;
  height: 100px;
  margin-top: 1rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid white;
  border-radius: 8px;
  padding: 1rem;
  color: white;
}

textarea::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

</style>