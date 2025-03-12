<template>
  <div class="home">
    <h1>Welcome to Our E-Commerce Platform</h1>
    <p>Choose an option to continue:</p>

    <div class="buttons">
      <router-link to="/signup">
        <button>Sign Up</button>
      </router-link>
      <router-link to="/login">
        <button>Login</button>
      </router-link>
    </div>
  </div>
</template>

<style scoped>
.home {
  text-align: center;
  margin-top: 50px;
}
.buttons {
  margin-top: 20px;
}
button {
  margin: 10px;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
}
</style>
