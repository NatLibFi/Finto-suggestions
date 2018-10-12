<template>
<div>
  <suggestion-header
    :openSuggestionCount="openCount"
    :resolvedSuggestionCount="resolvedCount"
    @sortSuggestionListBy="sortSuggestionList" />
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
import SuggestionHeader from './SuggestionHeader';
import SuggestionItem from './SuggestionItem';

import {
  suggestionGetters,
  suggestionActions
} from '../../store/modules/suggestion/suggestionConsts.js';

import {
  mapSuggestionActions,
  mapSuggestionGetters
} from '../../store/modules/suggestion/suggestionModule.js';

export default {
  components: {
    SuggestionHeader,
    SuggestionItem
  },
  computed: {
    ...mapSuggestionGetters({
      items: suggestionGetters.GET_SUGGESTIONS,
      openCount: suggestionGetters.GET_OPEN_SUGGESTIONS_COUNT,
      resolvedCount: suggestionGetters.GET_RESOLVED_SUGGESTIONS_COUNT,
      searchQuery: suggestionGetters.GET_SEARCH_QUERY,
      filters: suggestionGetters.GET_FILTERS
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
      getSortedSuggestions: suggestionActions.GET_SORTED_SUGGESTIONS,
      searchSuggestions: suggestionActions.GET_SEARCHED_SUGGESTIONS,
      getFilteredSuggestions: suggestionActions.GET_FILTERED_SUGGESTIONS
    }),
    async sortSuggestionList(selectedSorting) {
      if (selectedSorting && selectedSorting !== '') {
        this.getSortedSuggestions(selectedSorting);
      } else {
        this.getSuggestions();
      }
    }
  },
  watch: {
    searchQuery() {
      if (this.searchQuery !== '') {
        this.searchSuggestions(this.searchQuery);
      } else {
        this.getSuggestions();
      }
    },
    filters() {
      if(this.searchQuery.length <= 0) {
        if (this.filters.length > 0) {
          this.getFilteredSuggestions(this.filters);
        } else {
          this.getSuggestions();
        }
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
  align-items: flex-start;
  text-align: start;
}

.item {
  margin: 10px 0 10px 0;
  border-top: 2px solid #b1bfd6;
  border-bottom: 2px solid #b1bfd6;
}
</style>
