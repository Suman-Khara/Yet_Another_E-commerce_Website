<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
  <header>
    <img src="/favicon.ico" alt="Logo" class="favicon" />
    <h1>Assignment 2 E-Commerce Website</h1>
  </header>

  <main>
    <RouterView />
  </main>
</template>

<style scoped>
header {
  background-color: rgb(0, 255, 170);
  text-align: center;
  padding: 0.5rem;
  color: black;
  font-size: 1.2rem;
  font-weight: bold;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  position: fixed;
  width: 100%;
  top: 0;
  left: 0;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
}

.favicon {
  width: 24px;
  height: 24px;
  margin-right: 10px;
}

main {
  padding: 5rem 2rem 2rem; /* Add padding to avoid overlap with the fixed header */
}
</style>
