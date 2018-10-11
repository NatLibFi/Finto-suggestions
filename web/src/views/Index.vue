<template>
  <div class="container">
    <!-- <img src="../assets/logo.png"> -->
    <SuggestionSearch />
  <div>
    <navigation></navigation>
    <Suggestions />
  </div>
</template>

<script>
import SuggestionSearch from '../components/suggestion/SuggestionSearch';
import Navigation from '../components/navigation/Navigation';
import Suggestions from '../components/suggestion/Suggestions';

export default {
  components: {
    SuggestionSearch,
    Navigation,
    Suggestions
  }
};
</script>
