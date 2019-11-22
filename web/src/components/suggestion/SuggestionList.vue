<template>
  <div>
    <suggestion-search
      v-if="!isUserPage"
      :meetingId="meetingId"
      :filters="filters"
      :searchWord="searchWord"
      :sort="sort"
    />
    <suggestion-list-header
      v-if="!isUserPage"
      :meetingId="meetingId"
      :filters="filters"
      :searchWord="searchWord"
      :sort="sort"
    />
    <div>


    </div>

<!-- Area 51
    <div class="list-container">
      <suggestions-filtered-by-archived
      :filters="filters"
      :searchWord="searchWord"
      
      
      />
    </div> -->


    <div class="list-container">
      <ul class="list">
        <transition-group name="fade">
          <suggestion-item
            class="suggestion"
            v-for="suggestion in suggestions"
            :key="suggestion.id"
            :suggestion="suggestion"
            :meetingId="meetingId"
          />
        </transition-group>
      </ul>
      <suggestion-list-pagination
        :pageCount="pageCount"
        :pageCountLoading="pageCountLoading"
        :userId="userId"
        :isUserPage="isUserPage"
        :meetingId="meetingId"
        :page="page"
        :filters="filters"
        :searchWord="searchWord"
        :sort="sort"
        @pageChanged="updateSuggestionList"
      />
    </div>
  </div>
</template>

<script>
import SuggestionSearch from './SuggestionSearch';
import SuggestionListHeader from './SuggestionListHeader';
import SuggestionItem from './SuggestionItem';
import SuggestionListPagination from './SuggestionListPagination';
// import SuggestionsFilteredByArchived from './SuggestionsFilteredByArchived';

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
    SuggestionListHeader,
    SuggestionItem,
    SuggestionListPagination,
    // SuggestionsFilteredByArchived,
  },
  props: {
    userId: {
      type: [String, Number],
      default: null
    },
    isUserPage: Boolean,
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
      aFilters: 'status:ARCHIVED',
      searchWord: this.$route.query.search ? this.$route.query.search : '',
      sort: this.$route.query.sort ? this.$route.query.sort : '',
      searchWordForRemoteUse: String,
      offsetByPagination,
      pageCount: 400,
      pageCountLoading: false,
      aCount: 0,
      suggestionsAsArray: []
    };
  },
  computed: {
    ...mapSuggestionGetters({
      suggestions: suggestionGetters.GET_SUGGESTIONS,
      suggestionCount: suggestionGetters.GET_SUGGESTIONS_COUNT,
      // archivedSuggestionCount: suggestionGetters.GET_ARCHIVED_SUGGESTIONS_COUNT
    }),
    
  },
  beforeUpdate() {
    // this.getArchivedSuggestionsCount();
  },
  async created() {
    this.pageCountLoading = true;
    await this.fetchSuggestions();
    this.pageCount = Math.ceil(this.suggestionCount / 25);

    // this.aCount = this.$router.archivedSuggestionCount.name('archivedCounts');


    if (this.pageCount < this.page) {
      this.goToFirstPage();
    }
    this.pageCountLoading = false;
  
  },
  

  methods: {
    ...mapSuggestionActions({
      getSuggestions: suggestionActions.GET_SUGGESTIONS,
      getSuggestionsByUserId: suggestionActions.GET_SUGGESTIONS_BY_USER_ID,
      getSuggestionsCount: suggestionActions.GET_SUGGESTIONS_COUNT,
      // getArchivedSuggestionsCount: suggestionActions.GET_ARCHIVED_SUGGESTIONS_COUNT
    }),
    test: function() {
      this.searchWordForRemoteUse = this.searchWord; 
    },
    async fetchSuggestions() {
      if (this.userId) {
        this.getSuggestionsByUserId({
          userId: this.userId,
          offset: offsetByPagination(this.page)
        });

        await this.getSuggestionsCount({
          filters: 'user_id:' + this.userId,
          searchWord: ''
        });

      } else {
        this.getSuggestions({
          offset: offsetByPagination(this.page),
          sort: this.sort,
          filters: this.filters,
          searchWord: this.searchWord
        });
        // this.aFilters = this.suggestions.filter(obj => obj.status === 'ARCHIVED').length;

        await this.getSuggestionsCount({
          filters: this.filters,
          searchWord: this.searchWord
        });

      }
    },
    async updateSuggestionList() {



      this.pageCountLoading = true;
      await this.fetchSuggestions();
      this.pageCount = Math.ceil(this.suggestionCount / 25);
      // Toimi molemmilla
      // this.aCount = this.archivedSuggestionCount.length;
      // this.aCount = this.archivedSuggestionCount.length;
      if (this.pageCount < this.page) {
        this.goToFirstPage();
      }
      this.pageCountLoading = false;
    },
    goToFirstPage() {
      if (this.meetingId) {
        this.$router.push({
          name: 'meeting-suggestion-list',
          params: {
            meetingId: this.meetingId,
            page: 1
          },
          query: {
            filters: this.filters,
            search: this.searchWord,
            sort: this.sort
          }
        });
      } else if (this.userId) {
        this.$router.push({
          name: 'user',
          params: {
            userId: this.userId,
            page: 1
          }
        });
      } else if (this.suggestions.length > 0) {
        this.$router.push({
          name: 'suggestions',
          params: {
            page: 1
          },
          query: {
            filters: this.filters,
            search: this.searchWord,
            sort: this.sort
          }
        });
      } else if (this.suggestions.length === 0 && !this.$route.query) {
        this.$router.push({
          name: 'index'
        });
      }
    }
  },
  watch: {
    $route() {
      this.filters = this.$route.query.filters ? this.$route.query.filters : '';
      this.aFilters = 'status:ARCHIVED';
      this.searchWord = this.$route.query.search ? this.$route.query.search : '';
      this.sort = this.$route.query.sort ? this.$route.query.sort : '';
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

.suggestion {
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
