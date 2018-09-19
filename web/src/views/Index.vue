<template>
  <div class="container">
    <!-- <img src="../assets/logo.png"> -->
    <SuggestionSearch />
    <Suggestions />
  </div>
</template>

<script>
import SuggestionSearch from '../components/suggestion/SuggestionSearch';
import Suggestions from '../components/suggestion/Suggestions';

export default {
  components: {
    SuggestionSearch,
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
