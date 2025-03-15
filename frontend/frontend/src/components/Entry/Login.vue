<template>
  <div class="login">
    <h2>Log In as:</h2>
    <router-link to="/customer/login">
      <button>Customer</button>
    </router-link>
    <router-link to="/seller/login">
      <button>Seller</button>
    </router-link>
    <router-link to="/delivery/login">
      <button>Delivery Partner</button>
    </router-link>
  </div>
</template>

<style scoped>
.login {
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
