<template>
  <div class="assign-user">
    <a @click="openSearch">
      Lisää käsittelijä
    </a>
    <div class="dropdown-content" id="users-list" v-if="searchOpen" v-on-clickaway="closeSearch">
      <div class="dropdown-header">Kutsu käyttäjä ehdotukseen</div>
      <div class="dropdown-filter">
        <input type="text" class="dropdown-filter-input" v-model="searchQuery" @keydown="filterResults"/>
      </div>
      <div class="dropdown-options">
        <div class="user-item" v-for="user in users" :key="user.id" v-on:click="assignUserToSuggestion({ suggestionId: suggestion.id, userId: user.id })">
          <div v-if="user.name && user.name.length > 0">
            <div  class="user-image">{{ userNameInitials(user.name) }}</div>
            <div class="user-name">{{ user.name }}</div>
          </div>
          <div v-if="user.name && user.name.length === 0">
            <div  class="user-image">{{ user.id }}</div>
            <div class="user-name">Käyttäjä {{ user.id }}</div>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SvgIcon from '../icons/SvgIcon';
import IconAddPerson from '../icons/IconAddPerson';
import { userNameInitials } from '../../utils/nameHelpers';
import { suggestionActions } from '../../store/modules/suggestion/suggestionConsts';
import { mapSuggestionActions } from '../../store/modules/suggestion/suggestionModule';
import { mapUserActions, mapUserGetters } from '../../store/modules/user/userModule';
import { userActions, userGetters } from '../../store/modules/user/userConsts';
import { directive as onClickaway } from 'vue-clickaway';

export default {
  components: {SvgIcon, IconAddPerson},
  directives: {onClickaway: onClickaway},
  props: {
    suggestion: {
      type: Object,
      required: true
    }
  },
  computed: {
    ...mapUserGetters({ users: userGetters.GET_USERS })
  },
  methods: {
    openSearch() {
      this.searchOpen = true;
    },
    closeSearch() {
      this.searchOpen = false;
    },
    filterResults() {
      this.users = this.userCache;
      if (this.searchQuery.length === 1) {
        return this.users = this.userCache
      };
      this.users = this.userCache.filter(item => item.name.toLowerCase().match(this.searchQuery.toLowerCase()));
    },
    ...mapSuggestionActions({ assignUserToSuggestion: suggestionActions.ASSIGN_SUGGESTION_TO_USER }),
    ...mapUserActions({ getUsers: userActions.GET_USERS }),

  },
  async created() {
    // If "admin" in user.roles:
    await this.getUsers();
    this.userCache = this.users;
  },
  data() {
    return {
      userCache: [],
      searchOpen: false,
      searchQuery: '',
      userNameInitials
    }
  }
  };
</script>

<style scoped>
    .assign-user {
      position: relative;
      display: inline-block;
    }
    .assign-user a {
      font-size: 14px;
    }
    .assign-user a:hover {
      cursor: pointer;
      cursor: hand;
    }
    .dropdown-content {
      text-align: center;
      position: absolute;
      right: 0;
      width: 200px;
      height: auto;
      background: #FFFFFF;
      border: 1px solid #f5f5f5;
      box-sizing: border-box;
      box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
      border-radius: 1px;
    }
    .dropdown-header {
      font-style: normal;
      font-weight: bold;
      line-height: normal;
      padding: 9px 0 8px 0;
      border-bottom: 1px solid #f5f5f5;
      font-size: 12px;
      color: #444444;
    }
    .dropdown-filter {
      border-bottom: 1px solid #f5f5f5;
      padding: 10px;
    }
    input.dropdown-filter-input {
      width: 180px;
      height: 26px;
      left: 10px;
      top: 44px;
      border: 1px solid #E1E1E1;
      box-sizing: border-box;
      border-radius: 1px;
    }
    .dropdown-options {
      max-height: 180px;
      overflow-x: scroll;
    }
    .user-item {
      text-align: left;
      position: relative;
      height: 40px;
      padding: 0 10px;
    }
    .user-item:hover {
      cursor: pointer;
      background-color: #f3fbfa;
    }
    .user-image {
      position: absolute;
      top: 22%;
      height: 25px;
      width: 25px;
      display: inline-block;
      border-radius: 35px;
      line-height: 27px;
      text-align: center;
      background-color: #804af2;
      color: #ffffff;
      font-size: 10px;
      font-weight: 800;
    }
    .user-name {
      position: absolute;
      top: 22%;
      margin-left: 40px;
      padding-top: 2px;
      display: inline-block;
      font-style: normal;
      font-weight: bold;
      line-height: 20px;
      font-size: 13px;
      color: #333333;
    }
</style>