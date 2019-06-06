<template>
  <div class="meetings">
    <navigation />
    <meetings />
    <meeting-list />
  </div>
</template>

<script>
import Navigation from '../components/navigation/Navigation';
import Meetings from '../components/meetings/Meetings';
import MeetingList from '../components/meetings/MeetingList';

export default {
  components: {
    Navigation,
    Meetings,
    MeetingList
  }
};
</script>
