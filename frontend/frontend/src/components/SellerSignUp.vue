<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const router = useRouter();  // Initialize Vue Router

const store_name = ref('');
const store_email = ref('');
const store_address = ref('');
const phone_number = ref('');
const password = ref('');
const confirmPassword = ref('');
const message = ref('');

const submitForm = async () => {
  if (password.value !== confirmPassword.value) {
    message.value = "Passwords do not match!";
    return;
  }

  try {
    const response = await axios.post('http://127.0.0.1:8000/user/signup/seller', {
      store_name: store_name.value,
      store_email: store_email.value,
      store_address: store_address.value,
      phone_number: phone_number.value,
      password: password.value
    });

    message.value = response.data.message;
    router.push('/login/seller');
  } catch (error) {
    console.error("Signup Error:", error.response);  // Log error details in console
    message.value = `Error: ${error.response?.data?.detail || error.response?.data || "Something went wrong"}`;
  }
};
</script>

<template>
  <div class="signup-container">
    <h2>Seller Sign Up</h2>
    <form @submit.prevent="submitForm">
      <input v-model="store_name" type="text" placeholder="Store Name" required />
      <input v-model="store_email" type="email" placeholder="Store Email" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <input v-model="confirmPassword" type="password" placeholder="Confirm Password" required />
      <input v-model="phone_number" type="text" placeholder="Phone Number" required />
      <textarea v-model="store_address" placeholder="Store Address" required></textarea>
      <button type="submit">Sign Up</button>
    </form>
    <p v-if="message">{{ message }}</p>
  </div>
</template>

<style scoped>
/* Main container */
.signup-container {
  width: 100%; /* Responsive width */
  max-width: 600px; /* Prevents stretching too wide */
  margin: 5vh auto; /* Centers the form with space on all sides */
  padding: 3rem; /* Spacing inside the container */
  background: rgb(35, 35, 35); /* Slightly greyish background */
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 255, 170, 255); /* Faint white shadow */
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* Form layout */
form {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 1rem; /* Equal spacing between elements */
}

/* Input fields & Textarea */
input, textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #666;
  border-radius: 8px;
  background: #222;
  color: #fff;
  font-size: 1rem;
}
</style>