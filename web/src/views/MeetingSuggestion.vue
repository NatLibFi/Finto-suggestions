<template>
  <div>
    <navigation />
    <suggestion :suggestionId="suggestionId" :meetingId="meetingId" />
  </div>
</template>

<script>
import Navigation from '../components/navigation/Navigation';
import MeetingStatus from '../components/meetings/MeetingStatus';
import Suggestion from '../components/suggestion/Suggestion';

export default {
  components: {
    Navigation,
    MeetingStatus,
    Suggestion
  },
  props: {
    suggestionId: {
      type: [String, Number],
      required: true
    },
    meetingId: {
      type: [String, Number],
      required: true
    }
  }
};
</script>
