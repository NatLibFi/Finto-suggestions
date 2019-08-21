<template>
  <div>
    <navigation />
    <meeting-suggestion-list :meetingId="meetingId" :page="page" />
  </div>
</template>

<script>
import Navigation from '../components/navigation/Navigation';
import MeetingSuggestionList from '../components/meetings/MeetingSuggestionList';

export default {
  components: {
    Navigation,
    MeetingSuggestionList
  },
  props: {
    meetingId: {
      type: [String, Number],
      required: true
    },
    page: {
      type: [String, Number],
      required: true,
      default: 1
    }
  }
};
</script>
