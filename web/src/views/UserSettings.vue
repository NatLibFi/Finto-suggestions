<template>
<div>
  <navigation />
  <user-settings />
</div>
</template>

<script>
import Navigation from '../components/navigation/Navigation';
import UserSettings from '../components/users/UserSettings';

export default {
  components: {
    Navigation,
    UserSettings
  }
};
</script>
