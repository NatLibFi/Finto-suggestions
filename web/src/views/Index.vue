<template>
  <div>
    <navigation></navigation>
    <suggestion-list></suggestion-list>
  </div>
</template>

<script>
import Navigation from '../components/navigation/Navigation';
import SuggestionList from '../components/suggestion/SuggestionList';

export default {
  components: {
    Navigation,
    SuggestionList
  }
};
</script>
