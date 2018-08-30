<template>
  <li class="suggestionItem">
        <span>
            <p class="title">
                {{title}} {{tags}}
            </p>
            <p class="label">
                #{{orderNumber}} Lähetetty {{ getDayDifference() }} päivää sitten
            </p>
        </span>
  </li>
</template>

<script>

import { differenceInDays, parse } from 'date-fns'

export default {
  name: "SuggestionElement",
  props: {
      orderNumber: Number,
      title: String,
      created: String,
      tags: Array
  },
  methods: {
      getDayDifference() {
          return differenceInDays(parse(new Date()), parse(this.created))
      }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    .suggestionItem {
        flex-basis: auto;
        width: 100%;
        height: 100%;
        margin-left: 3%;
    }

    .suggestionItem p {
        margin: 0;
    }

    .title {
        font-weight: bold;
    }

    .label {
        font-size: smaller;
    }
</style>
