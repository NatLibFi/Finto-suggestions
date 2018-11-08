<template>
  <div>
    <navigation />
    <suggestion :suggestionId="suggestionId" />
  </div>
</template>

<script>
import Navigation from '../components/navigation/Navigation';
import Suggestion from '../components/suggestion/Suggestion';

export default {
  components: {
    Navigation,
    Suggestion
  },
  props: {
    suggestionId: {
      type: [String, Number],
      required: true
    }
  }
};
</script>
