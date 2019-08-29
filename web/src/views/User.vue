<template>
  <div>
    <navigation />
    <user :userId="userId" :page="page" />
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
