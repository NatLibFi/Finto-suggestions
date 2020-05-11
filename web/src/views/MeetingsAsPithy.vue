<template>
  <div class="meetings">
    <navigation />
    <meetings-as-pithy />
  </div>
</template>

<script>
import Navigation from '../components/navigation/Navigation';
import MeetingsAsPithy from '../components/meetings/MeetingsAsPithy';

export default {
  components: {
    Navigation,
    MeetingsAsPithy
  }
};
</script>
