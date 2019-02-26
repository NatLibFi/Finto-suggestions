<template>
<div class="list-container">
  <suggestion-list-header
    :openSuggestionCount="openCount || 0"
    :resolvedSuggestionCount="resolvedCount || 0"
    :meetingSort="meetingSort"
    class="header" />
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
  suggestionActions
} from '../../store/modules/suggestion/suggestionConsts.js';

import {
  mapSuggestionGetters,
  mapSuggestionActions
} from '../../store/modules/suggestion/suggestionModule.js';

import SuggestionListPagination from './SuggestionListPagination';
import { filterType, calculateOpenAndResolvedSuggestionCounts } from '../../utils/suggestionHelpers';
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
      meetingSuggestionsSelectedSort: suggestionGetters.GET_MEETING_SUGGESTIONS_SELECTED_SORT
    })
  },
  async created() {
    this.meetingSort = this.meetingId && parseInt(this.meetingId) > 0 ? true : false;
    await this.getSuggestionsSelectedSortKey();
    await this.getMeetingsSuggestionsSelectedSortKey();
    await this.handleSuggestionFetching();

    if(this.filters.length > 0) {
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
      getMeetingsSuggestionsSelectedSortKey: suggestionActions.GET_MEETING_SUGGESTIONS_SELECTED_SORT,
      getSuggestionsBySearchWord: suggestionActions.GET_SUGGESTIONS_BY_SEARCH_WORD
    }),
    async handleSuggestionFetching() {
      if (this.meetingId && parseInt(this.meetingId) > 0) {
        await this.fetchAndSortMeetingSuggestions();
      } else {
        await this.fetchAndSortAllSuggestions();
      }
      await this.paginationPageChanged();
    },
    async fetchAndSortAllSuggestions() {
      await this.getSuggestionsSelectedSortKey();
      if (this.suggestionsSelectedSort && this.suggestionsSelectedSort !== '') {
        await this.getSortedSuggestions(this.suggestionsSelectedSort);
      } else {
        await this.getSortedSuggestions(sortingKeys.NEWEST_FIRST);
      }
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
        ? endIndex > this.items.length ? this.items.length : endIndex
        : endIndex > items.length ? items.length : endIndex
    },
    async paginationPageChanged(pageNumber = 1, items = null) {
      const start = this.getPaginationStaringIndex(pageNumber);
      const end = this.getPaginationEndingIndex(pageNumber, items);
      const paginatedItems = items ? items : this.items;
      this.paginated_items =
        paginatedItems && paginatedItems.length > 0 ? paginatedItems.slice(start, end) : [];
      this.calculateOpenAndResolvedSuggestionCounts(items);
      this.calculatePageCountForPagination(items);
    },
    calculatePageCountForPagination(items = null) {
      this.paginationPageCount = items === null
        ? Math.ceil(this.items.length / this.paginationMaxCount)
        : Math.ceil(items.length / this.paginationMaxCount);
    },
    calculateOpenAndResolvedSuggestionCounts(items = null) {
      const counts = items === null
        ? calculateOpenAndResolvedSuggestionCounts(this.items)
        : calculateOpenAndResolvedSuggestionCounts(items);
      this.openCount = counts && counts.openCount ? counts.openCount : 0;
      this.resolvedCount = counts && counts.resolvedCount ? counts.resolvedCount : 0;
    },
    async filterSuggestions() {
     if (this.filters && this.filters.length > 0) {
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
              this.getSuggestionsBySearchWord(filter.value)
              items = this.items;
              break;
          }
        });
        await this.paginationPageChanged(1, items);
      } else {
        await this.handleSuggestionFetching();
      }
    }
  },
  watch: {
    async filters() {
      this.filterSuggestions();
    },
    async suggestionsSelectedSort() {
      await this.handleSuggestionFetching();
    },
    async meetingSuggestionsSelectedSort() {
      await this.handleSuggestionFetching();
    },
    async items() {
       await this.paginationPageChanged(1, this.items);
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
.fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0.75;
}
</style>
