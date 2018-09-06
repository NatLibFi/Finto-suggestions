<template>
  <li class="suggestionItem">
        <span>
            <p class="title">
                {{title}} {{ formatTags() }}
            </p>
            <p class="label">
                #{{orderNumber}} Lähetetty {{ buildLabel() }}
            </p>
        </span>
  </li>
</template>

<script>
import { differenceInDays, parse } from "date-fns";

export default {
  name: "SuggestionItem",
  props: {
    orderNumber: Number,
    title: String,
    created: String,
    suggestionType: String,
    tags: Array
  },
  methods: {
    getDayDifference() {
      return differenceInDays(parse(new Date()), parse(this.created));
    },
    buildLabel() {
      const whenSended = this.getDayDifference();
      return whenSended > 0 ? `${whenSended} päivää sitten` : "tänään";
    },
    formatTags() {
      let tagListing = this.suggestionType;
      console.log(this.suggestionType);

      if (this.tags.length > 0) {
        this.tags.forEach(tag => {
          tagListing += `${tag},`;
        });
        return tagListing.slice(0, -1); //removed last ,-mark from string
      }

      return tagListing;
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
