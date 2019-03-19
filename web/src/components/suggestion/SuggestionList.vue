<template>
<div class="list-container">
  <suggestion-list-header
    :openSuggestionCount="openCount || 0"
    :resolvedSuggestionCount="resolvedCount || 0"
    :meetingSort="meetingSort"
    class="header"
    @showOpenSuggestions="fetchOpenSuggestions"
    @showResolvedSuggestions="fetchResolvedSuggestions"
    @showAllSuggestions="handleSuggestionFetching"
  />
  <ul class="list">
    <transition-group name="fade">
      <suggestion-item
        class="item"
        v-for="item in paginated_items"
        :key="item.id"
        :suggestion="item"
        :meetingId="meetingId"
        />
    </transition-group>
  </ul>
  <suggestion-list-pagination
    :pageCount="paginationPageCount"
    @paginationPageChanged="paginationPageChanged"
  />
</div>
</template>

<script>
import SuggestionListHeader from './SuggestionListHeader';
import SuggestionItem from './SuggestionItem';

import {
  suggestionGetters,
  suggestionActions,
  suggestionMutations
} from '../../store/modules/suggestion/suggestionConsts.js';

import {
  mapSuggestionGetters,
  mapSuggestionActions,
  mapSuggestionMutations
} from '../../store/modules/suggestion/suggestionModule.js';

import SuggestionListPagination from './SuggestionListPagination';
import {
  filterType,
  calculateOpenAndResolvedSuggestionCounts
} from '../../utils/suggestionHelpers';
import { sortingKeys } from '../../utils/sortingHelper.js';

export default {
  components: {
    SuggestionListHeader,
    SuggestionItem,
    SuggestionListPagination
  },
  props: {
    // TODO: use meetingId to filter suggestions under this meeting for Meeting's Suggestion list
    meetingId: {
      type: [String, Number],
      default: null
    }
  },
  data() {
    return {
      paginationMaxCount: 10,
      paginationPageCount: 0,
      openCount: 0,
      resolvedCount: 0,
      paginated_items: [],
      meetingSort: false
    };
  },
  computed: {
    ...mapSuggestionGetters({
      items: suggestionGetters.GET_SUGGESTIONS,
      filters: suggestionGetters.GET_FILTERS,
      suggestionsSelectedSort: suggestionGetters.GET_SUGGESTIONS_SELECTED_SORT,
      meetingSuggestionsSelectedSort: suggestionGetters.GET_MEETING_SUGGESTIONS_SELECTED_SORT,
      filtered_items: suggestionGetters.GET_FILTERED_ITEMS
    })
  },
  async created() {
    this.meetingSort = this.meetingId && parseInt(this.meetingId) > 0 ? true : false;
    await this.getSuggestionsSelectedSortKey();
    await this.getMeetingsSuggestionsSelectedSortKey();
    await this.handleSuggestionFetching();
    this.getSelectedFilters();

    if (this.filters.length > 0) {
      this.filterSuggestions();
    }
  },
  methods: {
    ...mapSuggestionActions({
      getSuggestions: suggestionActions.GET_SUGGESTIONS,
      getSortedSuggestions: suggestionActions.GET_SORTED_SUGGESTIONS,
      getSuggestionsSelectedSortKey: suggestionActions.GET_SUGGESTIONS_SELECTED_SORT,
      getSuggestionsByMeetingId: suggestionActions.GET_SUGGESTIONS_BY_MEETING_ID,
      getSortedSuggestionsByMeetingId: suggestionActions.GET_SORTED_SUGGESTIONS_BY_MEETING_ID,
      getMeetingsSuggestionsSelectedSortKey:
        suggestionActions.GET_MEETING_SUGGESTIONS_SELECTED_SORT,
      getSuggestionsBySearchWord: suggestionActions.GET_SUGGESTIONS_BY_SEARCH_WORD,
      getSelectedFilters: suggestionActions.GET_SELECTED_FILTERS,
      setSelectedFilters: suggestionActions.SET_SELECTED_FILTERS,
      getOpenSuggestions: suggestionActions.GET_OPEN_SUGGESTIONS,
      getResolvedSuggestions: suggestionActions.GET_RESOLVED_SUGGESTIONS
    }),
    ...mapSuggestionMutations({
      setFilteredItems: suggestionMutations.SET_FILTERED_ITEMS
    }),
    async handleSuggestionFetching() {
      if (this.meetingId && parseInt(this.meetingId) > 0) {
        // notice: clearing all the filters when entering meeting suggestion list
        if (this.filters.length > 0) {
          await this.setSelectedFilters([]);
        }
        await this.fetchAndSortMeetingSuggestions();
      } else {
        await this.fetchAndSortAllSuggestions();
      }
    },
    async fetchAndSortAllSuggestions() {
      await this.getSuggestionsSelectedSortKey();
      if (this.suggestionsSelectedSort && this.suggestionsSelectedSort !== '') {
        await this.getSortedSuggestions(this.suggestionsSelectedSort);
        if (this.filters.length > 0) {
          await this.filterSuggestions();
        }
      } else {
        await this.getSortedSuggestions(sortingKeys.NEWEST_FIRST);
      }
      await this.paginationPageChanged();
    },
    async fetchAndSortMeetingSuggestions() {
      await this.getMeetingsSuggestionsSelectedSortKey();
      if (this.meetingSuggestionsSelectedSort && this.meetingSuggestionsSelectedSort !== '') {
        await this.getSortedSuggestionsByMeetingId({
          meetingId: this.meetingId,
          sortValue: this.meetingSuggestionsSelectedSort
        });
      } else {
        await this.getSuggestionsByMeetingId(parseInt(this.meetingId));
      }
      this.paginationPageChanged();
    },
    getPaginationStaringIndex(pageNumber) {
      return pageNumber > 1 ? this.paginationMaxCount * pageNumber - this.paginationMaxCount : 0;
    },
    getPaginationEndingIndex(pageNumber, items) {
      const endIndex = this.paginationMaxCount * pageNumber;
      return items === null
        ? endIndex > this.items.length
          ? this.items.length
          : endIndex
        : endIndex > items.length
          ? items.length
          : endIndex;
    },
    async paginationPageChanged(pageNumber = 1, items = null, refreshSuggestionsCount = true) {
      const start = this.getPaginationStaringIndex(pageNumber);
      const end = this.getPaginationEndingIndex(pageNumber, items);

      let paginatedItems;
      if (items) {
        paginatedItems = items;
        if (this.filters.length > 0) {
          await this.setFilteredItems(items);
        }
      } else if (!items && this.filters.length > 0) {
        paginatedItems = this.filtered_items;
      } else {
        paginatedItems = this.items;
      }

      this.paginated_items =
        paginatedItems && paginatedItems.length > 0 ? paginatedItems.slice(start, end) : [];

      if (refreshSuggestionsCount) {
        this.calculateOpenAndResolvedSuggestionCounts(paginatedItems);
      }

      this.calculatePageCountForPagination(paginatedItems);
    },
    calculatePageCountForPagination(items = null) {
      this.paginationPageCount =
        items === null
          ? Math.ceil(this.items.length / this.paginationMaxCount)
          : Math.ceil(items.length / this.paginationMaxCount);
    },
    calculateOpenAndResolvedSuggestionCounts(items = null) {
      const counts =
        items === null
          ? calculateOpenAndResolvedSuggestionCounts(this.items)
          : calculateOpenAndResolvedSuggestionCounts(items);
      this.openCount = counts && counts.openCount ? counts.openCount : 0;
      this.resolvedCount = counts && counts.resolvedCount ? counts.resolvedCount : 0;
    },
    async filterSuggestions() {
      if (this.filters && this.filters.length > 0) {
        const searchFilter = this.filters.find(f => f.type === filterType.SEARCH);
        let items;
        if (searchFilter) {
          await this.getSuggestionsBySearchWord(searchFilter.value);
          items = this.items;
          if (this.filters.length > 1) {
            items = this.handleTheResultFiltering(this.items, this.filters);
          }
        } else {
          items = this.handleTheResultFiltering(this.items, this.filters);
        }
        await this.paginationPageChanged(1, items);
      } else {
        await this.handleSuggestionFetching();
      }
    },
    handleTheResultFiltering(items, filters) {
      filters.forEach(filter => {
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
        }
      });
      return items;
    },
    async fetchOpenSuggestions() {
      await this.getOpenSuggestions();
      await this.paginationPageChanged(1, this.items, false);
    },
    async fetchResolvedSuggestions() {
      await this.getResolvedSuggestions();
      await this.paginationPageChanged(1, this.items, false);
    }
  },
  watch: {
    async filters() {
      if(this.filters.length > 0) {
        this.filterSuggestions();
      } else {
        this.handleSuggestionFetching();
      }
    },
    async suggestionsSelectedSort() {
      await this.handleSuggestionFetching();
    },
    async meetingSuggestionsSelectedSort() {
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

.fade-enter-active,
.fade-leave-active {
  transition: opacity 3s;
}
.fade-enter,
.fade-leave-to {
  opacity: 0.75;
}
</style>
