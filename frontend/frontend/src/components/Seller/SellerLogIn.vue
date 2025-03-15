<template>
  <div class="login-container">
    <h2>Seller Login</h2>
    <form @submit.prevent="login">
      <input type="email" v-model="store_email" placeholder="Store Email" required />
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
      store_email: '',
      password: '',
      error: ''
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post("http://127.0.0.1:8000/user/seller/login/", {
          store_email: this.store_email,
          password: this.password
        });

        alert("Login Successful!");
        console.log(response.data);

        // Store token and store_name in localStorage
        localStorage.setItem("token", response.data.token);
        localStorage.setItem("store_name", response.data.store_name);  // 🔹 Add this line

        this.$router.push(`/seller/profile/${response.data.store_name}`);
      } catch (err) {
        this.error = "Invalid store email or password";
      }
    }
  }
};
</script>

<style scoped>
/* Main container */
.login-container {
  width: 100%;
  max-width: 600px;
  margin: 5vh auto;
  padding: 3rem;
  background: rgb(35, 35, 35);
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0,255,170,255);
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* Form layout */
form {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* Input fields */
input {
  width: 100%;
  padding: 12px;
  border: 1px solid #666;
  border-radius: 8px;
  background: #222;
  color: #fff;
  font-size: 1rem;
}
</style>