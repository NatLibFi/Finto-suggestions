<template>
  <ul class="suggestionList">
  <suggestion-item
    class="suggestionItem"
    v-for="item in this.items"
    v-bind:key="item.orderNumber"
    :orderNumber=item.orderNumber
    :title=item.title
    :created=item.created
    :tags=item.tags />
  </ul>
</template>

<script>
// import {
//   suggestionActions,
//   suggestionGetters,
//   mapSuggestionActions,
//   mapSuggestionGetters } from '../../store/modules/suggestion'
import SuggestionItem from "./SuggestionItem";
import api from "../../api/index.js";

export default {
  name: "SuggestionList",
  components: {
    SuggestionItem
  },
  data() {
    return {
      items: []
    };
  },
  created: {
    async getSuggestions() {
      this.items = await api.suggestions.getSuggestions();
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
ul {
  list-style: none;
}

.suggestionList {
  align-items: flex-start;
  text-align: start;
}

.suggestionItem {
  margin: 10px 0 10px 0;
  border-top: 2px solid #b1bfd6;
  border-bottom: 2px solid #b1bfd6;
}
</style>
