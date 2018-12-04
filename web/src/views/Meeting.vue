<template>
  <div>
    <navigation />
    <meeting :meetingId="meetingId" />
  </div>
</template>

<script>
import Navigation from '../components/navigation/Navigation';
import Meeting from '../components/meetings/Meeting';

export default {
  components: {
    Navigation,
    Meeting
  },
  props: {
    meetingId: {
      type: [String, Number],
      required: true
    }
  }
};
</script>
