<template>
  <div>
    <navigation />
    <meeting-list />
  </div>
</template>

<script>
import Navigation from '../components/navigation/Navigation';
import MeetingList from '../components/meetings/MeetingList';

export default {
  components: {
    Navigation,
    MeetingList
  }
};
</script>
