<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
export default {
  created() {
    // eslint-disable-next-line
    $cookies.config('10d');
    // eslint-disable-next-line
    $cookies.set('logged_user_id', process.env.VUE_APP_USER_ID); //TODO: remove this when login and logout is working
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
