<template>
  <div class="assign-user">
    <button v-on:click="toggleSearch">
        <svg-icon icon-name='add-person'><icon-add-person /></svg-icon>
    </button>
    <div class="dropdown-content" id="users-list" v-show="searchOpen" v-on:mouseleave="searchOpen = false">
      <div class="dropdown-header">Kutsu käyttäjä ehdotukseen</div>
      <hr class="line"/>
      <input type="text" class="dropdown-filter" v-model="searchQuery" v-on:keydown="filterResults"/>
      <hr class="line"/>
      <div class="dropdown-users">
        <div class="user-item" v-for="user in users" :key="user.id" v-on:click="assignUserToSuggestion({ suggestionId: suggestion.id, userId: user.id })">
          <div class="user-image">{{ userNameInitials(user.name) }}</div>
          <div class="user-name">{{ user.name }}</div>
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

export default {
  components: {SvgIcon, IconAddPerson},
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
    toggleSearch() {
      this.searchOpen = !this.searchOpen
    },
    filterResults() {
      this.users = this.userCache;
      if (this.searchQuery.length === 1) return this.users = this.userCache;
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
  data () {
    return {
      userCache: [],
      searchOpen: false,
      searchQuery: '',
      userNameInitials
    }
  }
}
</script>

<style scoped>
    .assign-user {
        position: relative;
        display: inline-block;
    }
    .assign-user button {
        background-color: rgba(0,0,0,0);
        border-width: 0;
    }
    .dropdown-content {
        text-align: center;
        position: absolute;
        right: 0;
        width: 200px;
        height: auto;
        background: #FFFFFF;
        border: 2px solid #E1E1E1;
        box-sizing: border-box;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
        border-radius: 1px;
    }
    .dropdown-header {
        font-style: normal;
        font-weight: bold;
        line-height: normal;
        font-size: 14px;
        padding: 5px;
        color: #444444;
    }
    input.dropdown-filter {
        width: 180px;
        height: 26px;
        left: 10px;
        top: 44px;
        border: 1px solid #E1E1E1;
        box-sizing: border-box;
        border-radius: 1px;

    }
    .user-item {
        text-align: left;
        position: relative;
        height: 30px;
    }
    .user-item:hover {
        cursor: pointer;
        background-color: #f3f3f3 ;
    }
    .user-image {
        position: absolute;
        display: inline-block;
        height: 25px;
        width: 25px;
        border-radius: 35px;
        line-height: 25px;
        text-align: center;
        background-color: #804af2;
        color: #ffffff;
        font-size: 8px;
        font-weight: 800;
    }
    .user-name {
        margin-left: 40px;
        display: inline-block;
        font-style: normal;
        font-weight: bold;
        line-height: normal;
        font-size: 14px;
        color: #333333;
    }
    hr.line {
        border: 1px solid #F5F5F5;
    }
</style>