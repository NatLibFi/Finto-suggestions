<template>
<div class="list-container">
  <suggestion-header
    :openSuggestionCount="openCount || 0"
    :resolvedSuggestionCount="resolvedCount || 0"
    class="header" />
  <ul class="list">
    <suggestion-item
      class="item"
      v-for="item in paginated_items"
      :key="item.id"
      :suggestion="item"
      />
  </ul>
  <suggestion-list-pagination
    v-if="calculatePageCountForPagination() > 1"
    :pageCount="calculatePageCountForPagination()"
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
import { filterType, suggestionType, suggestionStateStatus } from '../../utils/suggestionMappings';

export default {
  components: {
    SuggestionHeader,
    SuggestionItem,
    SuggestionListPagination
  },
  props: {
    // TODO: use meetingId to filter suggestions under this meeting for Meeting's Suggestion list
    meetingId: {
      type: [String, Number, null],
      default: null
    }
  },
  data: () => ({
    paginationMaxCount: 10,
    openCount: 0,
    resolvedCount: 0
  }),
  computed: {
    ...mapSuggestionGetters({
      items: suggestionGetters.GET_SUGGESTIONS,
      filters: suggestionGetters.GET_FILTERS,
      paginated_items: suggestionGetters.GET_PAGINATION_SUGGESTIONS,
      selectedSort: suggestionGetters.GET_SELECTED_SORT
    })
  },
  async created() {
    await this.getSelectedSortKey();
    await this.handleSuggestionFetching();
  },
  methods: {
    ...mapSuggestionActions({
      getSuggestions: suggestionActions.GET_SUGGESTIONS,
      getSortedSuggestions: suggestionActions.GET_SORTED_SUGGESTIONS,
      getSelectedSortKey: suggestionActions.GET_SELECTED_SORT_KEY,
      getSuggestionsByMeetingId: suggestionActions.GET_SUGGESTIONS_BY_MEETING_ID,
      getSortedSuggestionsByMeetingId: suggestionActions.GET_SORTED_SUGGESTIONS_BY_MEETING_ID
    }),
    ...mapSuggestionMutations({
      setPaginatedSuggestions: suggestionMutations.SET_PAGINATION_SUGGESTIONS
    }),
    async handleSuggestionFetching() {
      if(this.meetingId && this.meetingId > 0) {
        await this.fetchAndSortMeetingSuggestions();
      } else {
        await this.fetchAndSortAllSuggestions();
      }
      await this.paginationPageChanged();
    },
    async fetchAndSortAllSuggestions() {
      if (this.selectedSort && this.selectedSort !== '') {
        await this.getSortedSuggestions(this.selectedSort);
      } else {
        await this.getSuggestions();
      }
    },
    async fetchAndSortMeetingSuggestions() {
      if (this.selectedSort && this.selectedSort !== '') {
        await this.getSortedSuggestionsByMeetingId({ meetingId: this.meetingId, sortValue: this.selectedSort });
      } else {
        await this.getSuggestionsByMeetingId(parseInt(this.meetingId));
      }
    },
    getPaginationStaringIndex(pageNumber) {
      return pageNumber > 1 ? this.paginationMaxCount * pageNumber - this.paginationMaxCount : 0;
    },
    getPaginationEndingIndex(pageNumber) {
      const endIndex = this.paginationMaxCount * pageNumber;
      return endIndex > this.items.length ? this.items.length : endIndex;
    },
    async paginationPageChanged(pageNumber = 1, items = null) {
      const start = this.getPaginationStaringIndex(pageNumber);
      const end = this.getPaginationEndingIndex(pageNumber);
      const paginatedItems = items ? items : this.items;
      this.setPaginatedSuggestions(
        paginatedItems && paginatedItems.length > 0 ? paginatedItems.slice(start, end) : []
      );
      this.calculateOpenAndResolvedSuggestionCounts();
    },
    calculatePageCountForPagination() {
      return Math.ceil(this.items.length / this.paginationMaxCount);
    },
    calculateOpenAndResolvedSuggestionCounts() {
      this.openCount = this.items.filter(i => i.status === null).length;
      this.resolvedCount = this.items.filter(i => i.status !== null).length;
    }
  },
  watch: {
    async filters() {
      if (this.filters.length > 0) {
        let items = this.items;
        this.filters.forEach(filter => {
          switch (filter.type) {
            case filterType.STATUS:
              items = items.filter(i => i.status === filter.value);
              break;
            case filterType.TAG:
              items = items.filter(i => {
                let hasFilterTag = i.tags.findIndex(tag => {
                  return tag.label == filter.value;
                });
                return hasFilterTag != -1;
              });
              break;
            case filterType.TYPE:
              items = items.filter(i => i.suggestion_type === filter.value);
              break;
            case filterType.MEETING:
              items = items.filter(i => i.meeting_id === filter.value);
              break;
            case filterType.SEARCH:
              items = items.filter(
                i => i.preferred_label && i.preferred_label.fi.startsWith(filter.value)
              );
              break;
          }
        });
        await this.paginationPageChanged(1, items);
      } else {
        await this.handleSuggestionFetching();
      }
    },
    async selectedSort() {
      await this.handleSuggestionFetching();
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.list-container {
  margin-bottom: 40px;
}

ul {
  list-style: none;
}

.list {
  text-align: left;
  background-color: #ffffff;
  border: 2px solid #f5f5f5;
  border-top: none;
  width: 60vw;
  margin: 0 20vw 20px;
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
