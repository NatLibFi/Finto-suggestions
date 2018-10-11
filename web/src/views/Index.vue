<template>
  <div>
    <navigation></navigation>
    <Suggestions />
  </div>
</template>

<script>
import Navigation from '../components/navigation/Navigation'
import Suggestions from '../components/suggestion/Suggestions';

export default {
  components: {
    Navigation,
    Suggestions
  }
};
</script>
