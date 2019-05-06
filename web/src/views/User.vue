<template>
  <div>
    <navigation />
    <user :userId="userId" />
  </div>
</template>

<script>
import Navigation from '../components/navigation/Navigation';
import User from '../components/users/User';

export default {
  components: {
    Navigation,
    User
  },
  props: {
    userId: {
      userId: [String, Number],
      required: true
    }
  }
};
</script>
