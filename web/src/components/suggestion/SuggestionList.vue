<template>
<div class="container">
  <suggestion-header
    :openSuggestionCount="openCount"
    :resolvedSuggestionCount="resolvedCount"
    @sortSuggestionListBy="sortSuggestionList" />
  <ul class="list">
    <suggestion-item
      class="item"
      v-for="item in paginated_items"
      :key="item.id"
      :orderNumber="item.id"
      :title="item.preferred_label.fi"
      :created="item.created"
      :status="item.status"
      :suggestionType="item.suggestion_type"
      :tags="item.tags" />
  </ul>
  <suggestion-list-pagination
    :pageCount="calcultePageCountForPagination()"
    @paginationPageChanged="paginationPageChanged"
  />
</div>
</template>

<script>
import SuggestionHeader from './SuggestionHeader';
import SuggestionItem from './SuggestionItem';

import {
  suggestionGetters,
  suggestionActions,
  suggestionMutations
} from '../../store/modules/suggestion/suggestionConsts.js';

import {
  mapSuggestionActions,
  mapSuggestionGetters,
  mapSuggestionMutations
} from '../../store/modules/suggestion/suggestionModule.js';

import SuggestionListPagination from './SuggestionListPagination';

export default {
  components: {
    SuggestionHeader,
    SuggestionItem,
    SuggestionListPagination
  },
  data: () => ({
    paginationMaxCount: 10
  }),
  computed: {
    ...mapSuggestionGetters({
      items: suggestionGetters.GET_SUGGESTIONS,
      openCount: suggestionGetters.GET_OPEN_SUGGESTIONS_COUNT,
      resolvedCount: suggestionGetters.GET_RESOLVED_SUGGESTIONS_COUNT,
      searchQuery: suggestionGetters.GET_SEARCH_QUERY,
      paginated_items: suggestionGetters.GET_PAGINATION_SUGGESTIONS,
    })
  },
  async created() {
    await this.getSuggestions();
    await this.getOpenSuggestionCount();
    await this.getResolvedSuggestionCount();
    this.paginationPageChanged();
  },
  methods: {
    ...mapSuggestionActions({
      getSuggestions: suggestionActions.GET_SUGGESTIONS,
      getOpenSuggestionCount: suggestionActions.GET_OPEN_SUGGESTIONS,
      getResolvedSuggestionCount: suggestionActions.GET_RESOLVED_SUGGESTIONS,
      getSortedSuggestions: suggestionActions.GET_SORTED_SUGGESTIONS,
      searchSuggestions: suggestionActions.GET_SEARCHED_SUGGESTIONS
    }),
    ...mapSuggestionMutations({
      setPaginatedSuggestions: suggestionMutations.SET_PAGINATION_SUGGESTIONS
    }),
    async sortSuggestionList(selectedSorting) {
      if (selectedSorting && selectedSorting !== '') {
        this.getSortedSuggestions(selectedSorting);
      } else {
        this.getSuggestions();
      }
    },
    getPaginationStaringIndex(pageNumber) {
      console.log(pageNumber);
      return pageNumber > 1 ? (this.paginationMaxCount * pageNumber) - this.paginationMaxCount : 0;
    },
    getPaginationEndingIndex(pageNumber) {
      const endIndex = (this.paginationMaxCount * pageNumber) -1
      return endIndex > this.items.length ? this.items.length : endIndex;
    },
    paginationPageChanged(pageNumber = 1) {
      const index = this.getPaginationStaringIndex(pageNumber);
      const endindex = this.getPaginationEndingIndex(pageNumber);
      const items = this.items.slice(index, endindex);
      console.log(items);
      this.setPaginatedSuggestions(items);
    },
    calcultePageCountForPagination() {
      const pageCount = Math.ceil(this.items.length / this.paginationMaxCount);
      console.log('pagecount calculated: ' + pageCount);
      return pageCount;
    }
  },
  watch: {
    searchQuery() {
      if (this.searchQuery !== '') {
        this.searchSuggestions(this.searchQuery);
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
