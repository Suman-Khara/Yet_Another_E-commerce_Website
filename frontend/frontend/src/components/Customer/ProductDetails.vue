<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const product = ref(null);
const reviews = ref([]);
const userReview = ref(null);
const showModal = ref(false);
const rating = ref(0);
const comment = ref('');

const fetchData = async () => {
  try {
    // Fetch both product details and reviews
    const [productResponse, reviewsResponse] = await Promise.all([
      axios.get(`http://127.0.0.1:8000/ecommerce/products/${route.params.id}/`, { withCredentials: true }),
      axios.get(`http://127.0.0.1:8000/ecommerce/products/${route.params.id}/reviews/`, { withCredentials: true })
    ]);

    // Product data processing
    product.value = {
      ...productResponse.data,
      seller: { store_name: productResponse.data.seller_name },
      category: { name: productResponse.data.category_name },
      tags: productResponse.data.tags.map(tag => ({ name: tag })),
    };

    // Review data processing
    reviews.value = reviewsResponse.data.reviews;
    userReview.value = reviewsResponse.data.user_review;

    if (userReview.value) {
      rating.value = userReview.value.rating;
      comment.value = userReview.value.comment;
    }
  } catch (error) {
    console.error('Error fetching data:', error);
  }
};

const submitReview = async () => {
  try {
    if (userReview.value) {
      await axios.put(
        `http://127.0.0.1:8000/ecommerce/products/${route.params.id}/reviews/${userReview.value.customer.username}/`,
        { rating: rating.value, comment: comment.value },
        { withCredentials: true }
      );
    } else {
      await axios.post(
        `http://127.0.0.1:8000/ecommerce/products/${route.params.id}/reviews/`,
        { rating: rating.value, comment: comment.value },
        { withCredentials: true }
      );
    }
    await fetchData();
    showModal.value = false;
  } catch (error) {
    console.error('Error submitting review:', error);
  }
};

const selectRating = (selectedRating) => {
  rating.value = selectedRating;
};

onMounted(fetchData);
</script>

<template>
  <div v-if="product" class="container">
    <div class="product-section">
      <img :src="product.image_url" alt="Product Image" class="product-image" />
      <div class="product-details">
        <h1 class="product-name">{{ product.name }}</h1>
        <div class="pricing">
          <span v-if="product.discount" class="old-price">${{ product.price }}</span>
          <span class="new-price">${{ (product.price * (1 - product.discount / 100)).toFixed(2) }}</span>
          <span v-if="product.discount" class="discount">({{ product.discount }}% off)</span>
        </div>
        <p class="description">{{ product.description }}</p>
        <p>Category: {{ product.category?.name || 'N/A' }}</p>
        <p>Tags: {{ product.tags.map(tag => tag.name).join(', ') }}</p>
        <p>Seller: {{ product.seller.store_name }}</p>
        <p>In Stock: {{ product.stock }}</p>
        <p>Rating: {{ product.rating.toFixed(1) }} ★ ({{ product.total_reviews }} Reviews)</p>

        <button @click="showModal = true">{{ userReview ? 'Edit Your Review' : 'Add a Review' }}</button>
      </div>
    </div>

    <!-- Review Modal -->
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <h2>{{ userReview ? 'Edit Your Review' : 'Add a Review' }}</h2>
        <label>Rating: </label>
        <div class="star-rating">
          <span v-for="star in 5" :key="star" @click="selectRating(star)">
            {{ star <= rating ? '★' : '☆' }}
          </span>
        </div>
        <label>Comment (Optional):</label>
        <textarea v-model="comment"></textarea>
        <div class="modal-actions">
          <button @click="submitReview">Submit</button>
          <button @click="showModal = false">Cancel</button>
        </div>
      </div>
    </div>

    <!-- Reviews Section -->
    <div class="reviews-section">
      <h3>Reviews</h3>
      <div v-if="userReview" class="review-card your-review">
        <strong>You</strong>
        <p>Rating: {{ userReview.rating }} ★</p>
        <p>{{ userReview.comment }}</p>
      </div>

      <div v-for="review in reviews" :key="review.id" class="review-card">
        <strong>{{ review.user.username }}</strong>
        <p>Rating: {{ review.rating }} ★</p>
        <p class="review-date">{{ new Date(review.created_at).toLocaleDateString() }}</p>
        <p>{{ review.comment }}</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  padding: 20px;
}

.product-section {
  display: flex;
  gap: 30px;
}

.product-image {
  width: 400px;
  height: 400px;
  object-fit: cover;
  border-radius: 10px;
}

.product-details {
  flex: 1;
}

button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  border-radius: 5px;
}

button:hover {
  background-color: #0056b3;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: #333;
  color: white;
  padding: 30px;
  border-radius: 10px;
  width: 400px;
}

.modal-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.star-rating span {
  font-size: 24px;
  cursor: pointer;
}

.star-rating span:hover {
  color: gold;
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
</style>
