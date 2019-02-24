<template>
  <div class="user">
    <div class="profile-container">
      <div class="user-name-initials">{{ userNameInitials }}</div>
      <div class="profile">
        <p class="profile-user" v-if="!user.name">
          Käyttäjä {{ userId }}<span v-if="user.role">, {{ userRoleToString[user.role] }}</span>
        </p>
        <p class="profile-user" v-if="user.name">
          {{ user.name }}<span v-if="user.role">, {{ userRoleToString[user.role] }}</span>
        </p>
        <p v-if="user.title || user.organization" class="profile-role">
          <span v-if="user.title">{{ user.title }}, </span>
          <span v-if="user.organization">{{ user.organization }}</span>
        </p>
      </div>
      <!--<div v-if="isAuthenticated && loggedInUserId === userId" class="settings">
        <div @click="showDropdown = true">
          <svg-icon icon-name="more"><icon-more/></svg-icon>
        </div>
        <div v-if="showDropdown" v-on-clickaway="closeDropdown" class="dropdown">
          <div @click="goToSettings">Muokkaa profiiliasi</div>
        </div>
      </div>-->
    </div>

    <div v-if="paginated_items && paginated_items.length > 0" class="user-suggestions">
      <suggestion-header
        :openSuggestionCount="openCount || 0"
        :resolvedSuggestionCount="resolvedCount || 0"
        :userPage="true"
        class="header" />
      <ul class="list">
        <transition-group name="fade">
          <suggestion-item
            class="item"
            v-for="item in paginated_items"
            :key="item.id"
            :suggestion="item"
            />
        </transition-group>
      </ul>
      <suggestion-list-pagination
        v-if="calculatePageCountForPagination() > 1"
        :pageCount="calculatePageCountForPagination()"
        @paginationPageChanged="paginationPageChanged"
      />
    </div>

    <div
      v-if="paginated_items && paginated_items.length === 0"
      class="no-user-suggestions-container">
        <p>Käyttäjälle ei ole asetettu käsitteitä.</p>
    </div>
  </div>
</template>

<script>
import SuggestionListHeader from '../suggestion/SuggestionListHeader';
import SuggestionItem from '../suggestion/SuggestionItem';
import SuggestionListPagination from '../suggestion/SuggestionListPagination';
import { calculateOpenAndResolvedSuggestionCounts } from '../../utils/suggestionHelpers';

import { userActions, userGetters } from '../../store/modules/user/userConsts';
import { mapUserActions, mapUserGetters } from '../../store/modules/user/userModule';
import { userNameInitials } from '../../utils/userHelpers.js';
import { userRoleToString } from '../../utils/userMappings.js';
// eslint-disable-next-line
import { authenticatedUserGetters } from '../../store/modules/authenticatedUser/authenticatedUserConsts.js';
// eslint-disable-next-line
import { mapAuthenticatedUserGetters } from '../../store/modules/authenticatedUser/authenticatedUserModule.js';

import {
  suggestionGetters,
  suggestionActions
} from '../../store/modules/suggestion/suggestionConsts.js';

import {
  mapSuggestionActions,
  mapSuggestionGetters
} from '../../store/modules/suggestion/suggestionModule.js';

import { filterType } from '../../utils/suggestionHelpers';

import SvgIcon from '../icons/SvgIcon';
import IconMore from '../icons/IconMore';
import { directive as onClickaway } from 'vue-clickaway';

export default {
  components: {
    SuggestionListHeader,
    SuggestionItem,
    SuggestionListPagination,
    SvgIcon,
    IconMore
  },
  directives: {
    onClickaway: onClickaway
  },
  props: {
    userId: [String, Number]
  },
  data() {
    return {
      userRoleToString,
      userNameInitials: '',
      paginationMaxCount: 10,
      openCount: 0,
      resolvedCount: 0,
      paginated_items: [],
      showDropdown: false
    };
  },
  computed: {
    ...mapAuthenticatedUserGetters({
      loggedInUserId: authenticatedUserGetters.GET_USER_ID,
      isAuthenticated: authenticatedUserGetters.GET_IS_AUTHENTICATED
    }),
    ...mapUserGetters({
      user: userGetters.GET_USER
    }),
    ...mapSuggestionGetters({
      items: suggestionGetters.GET_SUGGESTIONS,
      filters: suggestionGetters.GET_FILTERS,
      suggestionsSelectedSort: suggestionGetters.GET_SUGGESTIONS_SELECTED_SORT
    })
  },
  async created() {
    await this.getUser(this.userId);
    this.fetchUserNameAndInitials();
    await this.getSuggestionsByUserId(parseInt(this.userId));
    await this.handleSuggestionFetching();
    await this.getSuggestionsSelectedSortKey();
  },
  methods: {
    ...mapUserActions({
      getUser: userActions.GET_USER
    }),
    ...mapSuggestionActions({
      getSuggestionsByUserId: suggestionActions.GET_SUGGESTIONS_BY_USER_ID,
      getSortedSuggestionsByUserId: suggestionActions.GET_SORTED_SUGGESTIONS_BY_USER_ID,
      getSuggestionsSelectedSortKey: suggestionActions.GET_SUGGESTIONS_SELECTED_SORT
    }),
    fetchUserNameAndInitials() {
      if (this.user) {
        this.userNameInitials = userNameInitials(this.user.name);
      }
    },
    async handleSuggestionFetching() {
      await this.fetchAndSortAllSuggestions();
      await this.paginationPageChanged();
    },
    async fetchAndSortAllSuggestions() {
      await this.getSuggestionsSelectedSortKey();
      // TODO: Ensure that the sortValue is taken into account
      if (this.suggestionsSelectedSort && this.suggestionsSelectedSort !== '') {
        await this.getSortedSuggestionsByUserId({
          userId: parseInt(this.userId),
          sortValue: this.suggestionsSelectedSort
        });
      } else {
        await this.getSuggestionsByUserId(parseInt(this.userId));
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
      // eslint-disable-next-line
      this.paginated_items = paginatedItems && paginatedItems.length > 0 ? paginatedItems.slice(start, end) : []
      this.calculateOpenAndResolvedSuggestionCounts(items);
      this.calculatePageCountForPagination(items)
    },
    calculatePageCountForPagination() {
      return Math.ceil(this.items.length / this.paginationMaxCount);
    },
    calculateOpenAndResolvedSuggestionCounts(items = null) {
      const counts = items === null
        ? calculateOpenAndResolvedSuggestionCounts(this.items)
        : calculateOpenAndResolvedSuggestionCounts(items);
      this.openCount = counts && counts.openCount ? counts.openCount : 0;
      this.resolvedCount = counts && counts.resolvedCount ? counts.resolvedCount : 0;
    },
    closeDropdown() {
      this.showDropdown = false;
    },
    goToSettings: function() {
      this.$router.push({
        name: 'settings'
      });
      this.showDropdown = false;
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
          }
        });
        await this.paginationPageChanged(1, items);
      } else {
        await this.handleSuggestionFetching();
      }
    },
    async suggestionsSelectedSort() {
      await this.handleSuggestionFetching();
    }
  },
  mounted: function() {
    document.addEventListener('keydown', e => {
      if (e.keyCode === 27) {
        this.closeDropdown();
      }
    });
  }
};
</script>


<style scoped>
.profile-container {
  position: relative;
  background-color: #ffffff;
  border: 2px solid #f5f5f5;
  text-align: left;
  padding: 10px 40px;
  height: 80px;
  overflow: hidden;
  margin: 20px 20vw 0;
}

.user-name-initials {
  position: absolute;
  top: 50%;
  left: initial;
  transform: perspective(1px) translateY(-50%);
  display: inline-block;
  height: 50px;
  width: 50px;
  border-radius: 50px;
  line-height: 52px;
  text-align: center;
  background-color: #804af2;
  color: #ffffff;
  font-size: 17px;
  font-weight: 800;
  margin-right: 20px;
  -webkit-user-select: none; /* Safari */
  -moz-user-select: none; /* Firefox */
  -ms-user-select: none; /* IE10+/Edge */
  user-select: none; /* Standard */
}

.profile {
  position: absolute;
  top: 50%;
  left: 120px;
  transform: perspective(1px) translateY(-50%);
}

.profile-user {
  margin: 0;
  font-weight: 600;
  font-size: 14px;
}

.profile-role {
  margin: 0;
  margin-top: 4px;
  font-size: 13px;
}

.settings {
  position: absolute;
  top: 20px;
  right: 30px;
}

.dropdown {
  position: absolute;
  top: 20px;
  right: 0;
  width: 160px;
  font-size: 13px;
  font-weight: 600;
  color: #555555;
  text-align: center;
  background-color: #ffffff;
  border: 1px solid #e1e1e1;
  border-radius: 2px;
  -webkit-box-shadow: 6px 8px 17px -6px rgba(80, 80, 80, 0.35);
  -moz-box-shadow: 6px 8px 17px -6px rgba(80, 80, 80, 0.35);
  box-shadow: 6px 8px 17px -6px rgba(80, 80, 80, 0.35);
}

.dropdown div {
  padding: 10px 16px;
}

.dropdown div:hover {
  background-color: #f3fbfa;
  cursor: pointer;
  cursor: hand;
}

.user-suggestions {
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

.no-user-suggestions-container {
  position: relative;
  margin: 20px 20vw 0;
  padding: 10px 40px;
  font-weight: normal;
  text-align: left;
  background-color: #ffffff;
  border: 2px solid #f5f5f5;
  height: 36px;
}

.no-user-suggestions-container p {
  margin: 0;
  line-height: 100%;
  position: absolute;
  top: 50%;
  transform: perspective(1px) translateY(-50%);
}

@media (max-width: 700px) {
  .profile-container {
    height: 100%;
    padding: 20px 20px;
    margin: 20px 10vw 0;
  }

  .user-name-initials {
    display: block;
    position: initial;
    transform: initial;
    margin: 0 auto;
  }

  .profile {
    display: block;
    position: initial;
    transform: initial;
    text-align: center;
    padding: 20px 10px 10px;
  }

  .list {
    width: 80vw;
    margin: 0 10vw 20px;
  }

  .no-user-suggestions-container {
    margin: 20px 10vw 0;
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
