<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const router = useRouter();  // Initialize Vue Router

const username = ref('');
const email = ref('');
const password = ref('');
const confirmPassword = ref('');
const phone_number = ref('');
const address = ref('');
const message = ref('');

const submitForm = async () => {
  if (password.value !== confirmPassword.value) {
    message.value = "Passwords do not match!";
    return;
  }

  try {
    const response = await axios.post('http://127.0.0.1:8000/user/signup/customer', {
      username: username.value,
      email: email.value,
      password: password.value,
      phone_number: phone_number.value,
      address: address.value
    });

    message.value = response.data.message;
    router.push('/login/customer');
  } catch (error) {
    console.error("Signup Error:", error.response);  // Log error details in console
    message.value = `Error: ${error.response?.data?.detail || error.response?.data || "Something went wrong"}`;
  }
};
</script>

<template>
  <div class="signup-container">
    <h2>Customer Sign Up</h2>
    <form @submit.prevent="submitForm">
      <input v-model="username" type="text" placeholder="Username" required />
      <input v-model="email" type="email" placeholder="Email" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <input v-model="confirmPassword" type="password" placeholder="Confirm Password" required />
      <input v-model="phone_number" type="text" placeholder="Phone Number" required />
      <textarea v-model="address" placeholder="Address" required></textarea>
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
  box-shadow: 0 4px 15px rgba(0,255,170,255); /* Faint white shadow */
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