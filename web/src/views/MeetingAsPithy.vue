<template>
  <div class="meetings">
    <navigation />
    <meeting-as-pithy />
  </div>
</template>

<script>
import Navigation from '../components/navigation/Navigation';
import MeetingAsPithy from '../components/meetings/MeetingAsPithy';

export default {
  components: {
    Navigation,
    MeetingAsPithy
  }
};
</script>
