<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
export default {
  created() {
    $cookies.config('10d');
    $cookies.set('access_token', process.env.ACCESS_TOKEN);
  }
};
</script>


<style>
body {
  margin: 0;
  background-color: #f9f9f9;
}

a {
  color: #06a798;
}

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
