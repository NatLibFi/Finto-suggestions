<template>
<div>
  <navigation />
  <user-settings :userId="userId"/>
</div>
</template>

<script>
import Navigation from '../components/navigation/Navigation';
import UserSettings from '../components/users/UserSettings';

export default {
  components: {
    Navigation,
    UserSettings
  },
  props: {
    userId: [String, Number]
  }
};
</script>
