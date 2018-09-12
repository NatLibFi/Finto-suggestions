<template>
<div>
  <suggestion-header
    :openSuggestionCount="openSuggestionCount"
    :resolvedSuggestionCount="resolvedSuggestionCount"
    @fetchOpenSuggestionCount="getOpenSuggestionCount"
    @fetchResolvedSuggestionCount="getResolvedSuggestionCount"
    @sortSuggestionListBy="sortSuggestionList"
  />
  <ul class="list">
    <suggestion-item
      class="item"
      v-for="item in items"
      :key="item.id"
      :orderNumber=item.id
      :title=item.description
      :created=item.created
      :status=item.status
      :suggestionType=item.suggestion_type
      :tags=item.tags />
  </ul>
</div>
</template>

<script>
// import {
//   suggestionActions,
//   suggestionGetters,
//   mapSuggestionActions,
//   mapSuggestionGetters } from '../../store/modules/suggestion'
import SuggestionHeader from "./SuggestionHeader";
import SuggestionItem from "./SuggestionItem";
import api from "../../api/index.js";

export default {
  components: {
    SuggestionHeader,
    SuggestionItem
  },
  data: () => ({
    items: [],
    openSuggestionCount: 0,
    resolvedSuggestionCount: 0
  }),
  async created() {
    this.getSuggestions();
  },
  methods: {
    async getSuggestions() {
      const response = await api.suggestions.getSuggestions();
      this.items = response.data;
    },
    async getOpenSuggestionCount() {
      const newSuggestions = await api.suggestions.getAllNewSuggestions();
      this.openSuggestionCount = newSuggestions.items;
    },
    async getResolvedSuggestionCount() {
      const resolvedSuggestions = await api.suggestions.getAllResolvedSuggestions();
      this.resolvedSuggestionCount = resolvedSuggestions.items;
    },
    async sortSuggestionList(sortValue) {
      if(sortValue !== '') {
        const response = await api.suggestions.getSortedSuggestions(sortValue);
        this.items = response.data;
        return;
      }

      this.getSuggestions();
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
ul {
  list-style: none;
}

.list {
  align-items: flex-start;
  text-align: start;
}

.item {
  margin: 10px 0 10px 0;
  border-top: 2px solid #b1bfd6;
  border-bottom: 2px solid #b1bfd6;
}
</style>
