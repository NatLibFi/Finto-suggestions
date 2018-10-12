<template>
  <div>
    <navigation></navigation>
    <SuggestionSearch />
    <suggestion-list></suggestion-list>
  </div>
</template>

<script>
import Navigation from '../components/navigation/Navigation';
import SuggestionSearch from '../components/suggestion/SuggestionSearch';
import SuggestionList from '../components/suggestion/SuggestionList';

export default {
  components: {
    Navigation,
    SuggestionSearch,
    SuggestionList
  }
};
</script>
