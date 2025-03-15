<template>
  <div class="login-container">
    <h2>Customer Login</h2>
    <form @submit.prevent="login">
      <input type="email" v-model="email" placeholder="Email" required />
      <input type="password" v-model="password" placeholder="Password" required />
      <button type="submit">Log In</button>
      <p v-if="error" class="error">{{ error }}</p>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      email: '',
      password: '',
      error: ''
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post("http://127.0.0.1:8000/user/customer/login/", {
          email: this.email,
          password: this.password
        });
        alert("Login Successful!");
        console.log(response.data);
        // Store token in localStorage or Vuex for authentication
        localStorage.setItem("token", response.data.token);
        this.$router.push(`/customer/profile/${response.data.username}`);
      } catch (err) {
        this.error = "Invalid email or password";
      }
    }
  }
};
</script>

<style scoped>
/* Main container */
.login-container {
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