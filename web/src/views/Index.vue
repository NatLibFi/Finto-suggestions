<template>
  <div>
    <navigation></navigation>
    <suggestion-search />
    <suggestion-list />
    <suggestion-list-pagination />
  </div>
</template>

<script>
import Navigation from '../components/navigation/Navigation';
import SuggestionSearch from '../components/suggestion/SuggestionSearch';
import SuggestionList from '../components/suggestion/SuggestionList';
import SuggestionListPagination from '../components/suggestion/SuggestionListPagination';

export default {
  components: {
    Navigation,
    SuggestionSearch,
    SuggestionList,
    SuggestionListPagination
  }
};
</script>
