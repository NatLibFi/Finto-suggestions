<template>
  <div>
    <navigation></navigation>
    <suggestion-list :meetingId="null" :userId="null" :page="page" />
  </div>
</template>

<script>
import Navigation from '../components/navigation/Navigation';
import SuggestionList from '../components/suggestion/SuggestionList';

export default {
  components: {
    Navigation,
    SuggestionList
  },
  props: {
    page: {
      type: [String, Number],
      required: false
    }
  }
};
</script>
