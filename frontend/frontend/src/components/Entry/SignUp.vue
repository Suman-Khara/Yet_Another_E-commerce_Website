<template>
  <div class="signup">
    <h2>Sign Up as:</h2>
    <router-link to="/customer/signup">
      <button>Customer</button>
    </router-link>
    <router-link to="/seller/signup">
      <button>Seller</button>
    </router-link>
    <router-link to="/delivery/signup">
      <button>Delivery Partner</button>
    </router-link>
  </div>
</template>

<style scoped>
.signup {
  text-align: center;
  margin-top: 50px;
}
button {
  margin: 10px;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
}
</style>
