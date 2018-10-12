<template>
<div>
  <suggestion-header
    :openSuggestionCount="openCount"
    :resolvedSuggestionCount="resolvedCount"
    @sortSuggestionListBy="sortSuggestionList"
  />
  <ul class="list">
    <suggestion-item
      class="item"
      v-for="item in items"
      :key="item.id"
      :orderNumber="item.id"
      :title="item.preferred_label.fi"
      :created="item.created"
      :status="item.status"
      :suggestionType="item.suggestion_type"
      :tags="item.tags" />
  </ul>
</div>
</template>

<script>
import SuggestionHeader from './SuggestionHeader';
import SuggestionItem from './SuggestionItem';

import {
  suggestionGetters,
  suggestionActions
} from '../../store/modules/suggestionConsts.js';

import {
  mapSuggestionActions,
  mapSuggestionGetters
} from '../../store/modules/suggestion.js';

export default {
  components: {
    SuggestionHeader,
    SuggestionItem
  },
  computed: {
    ...mapSuggestionGetters({
      items: suggestionGetters.GET_SUGGESTIONS,
      openCount: suggestionGetters.GET_OPEN_SUGGESTIONS_COUNT,
      resolvedCount: suggestionGetters.GET_RESOLVED_SUGGESTIONS_COUNT
    })
  },
  created() {
    this.getSuggestions();
    this.getOpenSuggestionCount();
    this.getResolvedSuggestionCount();
  },
  methods: {
    ...mapSuggestionActions({
      getSuggestions: suggestionActions.GET_SUGGESTIONS,
      getOpenSuggestionCount: suggestionActions.GET_OPEN_SUGGESTIONS,
      getResolvedSuggestionCount: suggestionActions.GET_RESOLVED_SUGGESTIONS,
      getSortedSuggestions: suggestionActions.GET_SORTED_SUGGESTIONS
    }),
    async sortSuggestionList(sortValue) {
      console.log(sortValue);
      if (sortValue !== '') {
        this.getSortedSuggestions(sortValue);
      } else {
        this.getSuggestions();
      }
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
  text-align: left;
  background-color: #ffffff;
  border: 2px solid #f5f5f5;
  width: 60vw;
  margin: 20px 20vw;
  padding-left: 0; /* reset inital padding for ul tags */
}

.item {
  margin: 10px 0 10px 0;
  border-bottom: 2px solid #f5f5f5;
}

@media (max-width: 700px) {
  .list {
    width: 80vw;
    margin: 20px 10vw;
  }
}
</style>