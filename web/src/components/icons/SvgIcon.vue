<template>
  <svg
    :width="width"
    :height="height"
    viewBox="0 0 24 24"
    :aria-labelledby="iconName"
    role="presentation"
    stroke="currentColor">
    <title :id="iconName" lang="en">{{iconName}} icon</title>
    <g :fill="iconColor">
        <slot />
    </g>
  </svg>
</template>


<script>
export default {
  props: {
    iconName: {
      type: String,
      default: ''
    },
    width: {
      type: [Number, String],
      default: 24
    },
    height: {
      type: [Number, String],
      default: 24
    },
    iconColor: {
      type: String,
      default: 'currentColor'
    }
  }
};
</script>

<style scoped>
svg:hover {
  cursor: pointer;
  cursor: hand;
}
</style>
