<template>
  <div class="home_page">
    <!--
    <a href="/history">History Link</a> <!-- sends new request to server 
    <nuxt-link to="/history">History Page</nuxt-link> <!-- remains in the same SPA
    <button @click="onLoadHistory">Load History</button>
    -->
    <button @click="onLogin">Login</button>
  </div>
</template>

<script>
export default {
  methods: {
    onLogin() {
      this.$router.push("/about")
    },
    onLoadHistory() {
      this.$router.push("/history")
    }
  }
}
</script>

<style scoped>
.home_page {
    display: flex;
    justify-content: center;
    align-items: center;
}
</style>
