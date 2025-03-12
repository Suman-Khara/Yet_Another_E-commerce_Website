<template>
  <div class="login">
    <h2>Log In as:</h2>
    <router-link to="/login/customer">
      <button>Customer</button>
    </router-link>
    <router-link to="/login/seller">
      <button>Seller</button>
    </router-link>
    <router-link to="/login/delivery">
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
