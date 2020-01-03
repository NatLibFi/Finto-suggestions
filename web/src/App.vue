<template>
<!-- <div v-if="$auth.ready()" id="app"> -->
  <div id="app">
    <router-view />
  </div>
</template>

<script>
export default {};

// function ready() {
//   alert('DOM is ready');
// }

// document.addEventListener("DOMContentLoaded", ready);
</script>

<style>
body {
  margin: 0;
  background-color: #f9f9f9;
}

a {
  color: #06a798;
}

a:hover {
  color: #21baac;
}

#app {
  font-family: 'Fira Sans', 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
