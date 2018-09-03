<template>
  <ul class="suggestionList">
  <suggestion-item
    class="suggestionItem"
    v-for="item in items"
    v-bind:key="item.id"
    :orderNumber=item.id
    :title=item.description
    :created=item.created
    :tags=[] />
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
  data: () => ({
    items: []
  }),
  async created() {
    const response = await api.suggestions.getSuggestions();
    this.items = response.data;
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
