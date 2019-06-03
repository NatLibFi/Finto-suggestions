<template>
  <div>
    <suggestion-search :filters="filters" :searchWord="searchWord" />
    <div class="list-container">
      <ul class="list">
        <transition-group name="fade">
          <suggestion-item
            class="item"
            v-for="item in items"
            :key="item.id"
            :suggestion="item"
            :meetingId="meetingId"
          />
        </transition-group>
      </ul>
      <suggestion-list-pagination
        :pageCount="pageCount"
        :pageCountLoading="pageCountLoading"
        :page="page"
        :filters="$route.query.filters"
        :searchWord="$route.query.search"
        @pageChanged="updateSuggestionList"
      />
    </div>
  </div>
</template>

<script>
import SuggestionSearch from './SuggestionSearch';
import SuggestionItem from './SuggestionItem';
import SuggestionListPagination from './SuggestionListPagination';

import {
  suggestionGetters,
  suggestionActions
} from '../../store/modules/suggestion/suggestionConsts.js';

import {
  mapSuggestionGetters,
  mapSuggestionActions
} from '../../store/modules/suggestion/suggestionModule.js';

import { offsetByPagination } from '../../utils/suggestionHelpers.js';

export default {
  components: {
    SuggestionSearch,
    SuggestionItem,
    SuggestionListPagination
  },
  props: {
    // TODO: use meetingId to filter suggestions under this meeting for Meeting's Suggestion list
    meetingId: {
      type: [String, Number],
      default: null
    },
    page: {
      type: [String, Number],
      default: 1
    }
  },
  data() {
    return {
      filters: this.$route.query.filters ? this.$route.query.filters : '',
      searchWord: this.$route.query.search ? this.$route.query.search : '',
      offsetByPagination,
      pageCount: 400,
      pageCountLoading: false
    };
  },
  computed: {
    ...mapSuggestionGetters({
      items: suggestionGetters.GET_SUGGESTIONS,
      itemCount: suggestionGetters.GET_SUGGESTIONS_COUNT,
      sortKey: suggestionGetters.GET_SUGGESTIONS_SELECTED_SORT
    })
  },
  async created() {
    this.pageCountLoading = true;
    await this.getSuggestionsSelectedSortKey();
    this.fetchSuggestions();
    await this.getSuggestionsCount({
      filters: this.filters,
      searchWord: this.searchWord
    });
    this.pageCount = Math.ceil(this.itemCount / 15);
    if (this.pageCount < this.page) {
      this.goToFirstPage();
    }
    this.pageCountLoading = false;
  },
  methods: {
    ...mapSuggestionActions({
      getSuggestions: suggestionActions.GET_SUGGESTIONS,
      getSuggestionsCount: suggestionActions.GET_SUGGESTIONS_COUNT,
      getSuggestionsSelectedSortKey: suggestionActions.GET_SUGGESTIONS_SELECTED_SORT
    }),
    fetchSuggestions() {
      this.getSuggestions({
        offset: offsetByPagination(this.page),
        sortValue: this.sortKey,
        filters: this.filters,
        searchWord: this.searchWord
      });
    },
    async updateSuggestionList() {
      this.pageCountLoading = true;
      this.fetchSuggestions();
      await this.getSuggestionsCount({
        filters: this.filters,
        searchWord: this.searchWord
      })
      this.pageCount = Math.ceil(this.itemCount / 15);
      if (this.pageCount < this.page) {
        this.goToFirstPage();
      }
      this.pageCountLoading = false;
    },
    goToFirstPage() {
      this.$router.push({
        name: 'suggestions',
        params: {
          page: 1
        },
        query: {
          filters: this.filters,
          search: this.searchWord
        }
      });
    }
  },
  watch:{
    $route(to, from) {
      this.filters = this.$route.query.filters ? this.$route.query.filters : '';
      this.searchWord = this.$route.query.search ? this.$route.query.search : '';
      this.updateSuggestionList();
    }
  }
};
</script>

<style scoped>
.list-container {
  margin-bottom: 40px;
}

ul {
  list-style: none;
  min-height: 760px;
}

.list {
  text-align: left;
  background-color: #ffffff;
  border: 2px solid #f5f5f5;
  border-bottom: none;
  border-top: none;
  width: 60vw;
  margin: 0 20vw;
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
