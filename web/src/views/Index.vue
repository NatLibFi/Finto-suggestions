<template>
  <div class="container">
    <!-- <img src="../assets/logo.png"> -->
    <Suggestions />
  </div>
</template>

<script>
import Suggestions from '../components/suggestion/Suggestions';

export default {
  components: {
    Suggestions
  }
};
</script>

<style>
.container {
  display: flex;
  flex-flow: row wrap;
  flex-direction: column;
  justify-content: space-around;
}
</style>
