<template>
<div class="container">
  <suggestion-header
    :openSuggestionCount="openCount ? openCount : 0"
    :resolvedSuggestionCount="resolvedCount ? resolvedCount : 0"
    @sortSuggestionListBy="sortSuggestionList"
    class="header" />
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
import { filterType, suggestionType } from '../../utils/suggestionMappings';

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
      filters: suggestionGetters.GET_FILTERS,
      paginated_items: suggestionGetters.GET_PAGINATION_SUGGESTIONS
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
      getSortedSuggestions: suggestionActions.GET_SORTED_SUGGESTIONS
    }),
    ...mapSuggestionMutations({
      setPaginatedSuggestions: suggestionMutations.SET_PAGINATION_SUGGESTIONS,
      setFilteredSuggestions: suggestionMutations.SET_SUGGESTIONS
    }),
    sortSuggestionList(selectedSorting) {
      if (selectedSorting && selectedSorting !== '') {
        console.log('sorting', selectedSorting);
        this.getSortedSuggestions(selectedSorting);
      } else {
        this.getSuggestions();
      }
    },
    getPaginationStaringIndex(pageNumber) {
      return pageNumber > 1 ? (this.paginationMaxCount * pageNumber) - this.paginationMaxCount : 0;
    },
    getPaginationEndingIndex(pageNumber) {
      const endIndex = (this.paginationMaxCount * pageNumber)
      return endIndex > this.items.length ? this.items.length : endIndex;
    },
    paginationPageChanged(pageNumber = 1) {
      const index = this.getPaginationStaringIndex(pageNumber);
      const endindex = this.getPaginationEndingIndex(pageNumber);
      const items = this.items;
      this.setPaginatedSuggestions(items.slice(index, endindex));
    },
    calcultePageCountForPagination() {
      const pageCount = Math.ceil(this.items.length / this.paginationMaxCount);
      return pageCount;
    }
  },
  watch: {
    async filters() {
      if (this.filters.length > 0) {
        let items = this.items;
        this.filters.forEach(filter => {
          switch(filter.type) {
            case filterType.STATUS:
              items = items.filter(i => i.status === filter.value);
              break;
            case filterType.TAG:
              break;
            case filterType.TYPE:
              items = items.filter(i => i.suggestion_type === filter.value);
              break;
            case filterType.MEETING:
              items = items.filter(i => i.meeting_id === filter.value);
              break;
            case filterType.SEARCH:
              items = items.filter(i => i.preferred_label && i.preferred_label.fi.startsWith(filter.value));
              break;
          }
        });
        this.setFilteredSuggestions(items);
      } else {
        await this.getSuggestions();
      }
      this.paginationPageChanged();
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.container {
  margin-bottom: 40px;
}

ul {
  list-style: none;
}

.list {
  text-align: left;
  background-color: #ffffff;
  border: 2px solid #f5f5f5;
  border-bottom: none;
  width: 60vw;
  margin: 20px 20vw 0;
  padding-left: 0; /* reset inital padding for ul tags */
}

.item {
  margin: 10px 0 10px 0;
  border-bottom: 2px solid #f5f5f5;
}

@media (max-width: 700px) {
  .list {
    width: 80vw;
    margin: 0 10vw 20px;
  }
}
</style>
