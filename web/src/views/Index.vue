<template>
  <div>
    <navigation></navigation>
  <div class="container">
    <!-- <img src="../assets/logo.png"> -->
    <SuggestionSearch />
    <Suggestions />
  </div>
</template>

<script>
import Navigation from '../components/navigation/Navigation';
import SuggestionSearch from '../components/suggestion/SuggestionSearch';
import Suggestions from '../components/suggestion/Suggestions';

export default {
  components: {
    Navigation,
    SuggestionSearch,
    Suggestions
  }
};
</script>
