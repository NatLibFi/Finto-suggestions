<template>
  <div class="assign-user">
    <a @click="openSearch">
      Lisää käsittelijä
    </a>
    <div class="dropdown-content" v-if="searchOpen" v-on-clickaway="closeSearch">
      <div class="dropdown-header">Kutsu käyttäjä ehdotukseen</div>
      <div class="dropdown-filter">
        <input type="text" class="dropdown-filter-input" v-model="searchQuery" />
      </div>
      <div class="dropdown-options">
        <div
          v-for="user in filteredUsers"
          :key="user.id"
          @click="assignUserToSuggestion({ suggestionId: suggestion.id, userId: user.id })"
          class="user-item">
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
import { userNameInitials } from '../../utils/userHelpers';
import { suggestionActions } from '../../store/modules/suggestion/suggestionConsts';
import { mapSuggestionActions } from '../../store/modules/suggestion/suggestionModule';
import {
  mapUserActions,
  mapUserGetters,
  mapUserMutations
} from '../../store/modules/user/userModule';
import { userActions, userGetters, userMutations } from '../../store/modules/user/userConsts';
import { directive as onClickaway } from 'vue-clickaway';

export default {
  directives: { onClickaway: onClickaway },
  props: {
    suggestion: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      searchOpen: false,
      searchQuery: '',
      userNameInitials,
      filteredUsers: []
    };
  },
  computed: {
    ...mapUserGetters({ users: userGetters.GET_USERS })
  },
  async created() {
    // If "admin" in user.roles:
    await this.getUsers();
    this.filteredUsers = this.users;
  },
  mounted() {
    document.body.addEventListener('keyup', e => {
      if (e.keyCode === 27) {
        this.closeSearch();
      }
    });
  },
  methods: {
    ...mapSuggestionActions({
      assignUserToSuggestion: suggestionActions.ASSIGN_SUGGESTION_TO_USER
    }),
    ...mapUserActions({ getUsers: userActions.GET_USERS }),
    ...mapUserMutations({ setUsers: userMutations.SET_USERS }),
    toggleSearch() {
      this.searchOpen = !this.searchOpen;
    },
    filterResults() {
      this.getUsers();
      if (this.searchQuery.length >= 1) {
        const filteredUsers = this.users.filter(user =>
          user.name.toLowerCase().includes(this.searchQuery.toLowerCase())
        );
        this.setUsers(filteredUsers);
      }
    },
    openSearch() {
      this.searchOpen = true;
    },
    closeSearch() {
      this.searchOpen = false;
    }
  },
  watch: {
    searchQuery() {
      this.filterResults();
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
  -webkit-user-select: none; /* Safari */
  -moz-user-select: none; /* Firefox */
  -ms-user-select: none; /* IE10+/Edge */
  user-select: none; /* Standard */
}
.assign-user a:hover {
  cursor: pointer;
  cursor: hand;
}
.dropdown-content {
  text-align: center;
  position: absolute;
  top: 22px;
  left: -30%;
  width: 200px;
  height: auto;
  background: #ffffff;
  border: 1px solid #f5f5f5;
  box-sizing: border-box;
  border-radius: 1px;
  z-index: 10;
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
  border: 1px solid #e1e1e1;
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
  height: 42px;
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

@media (max-width: 700px) {
  .dropdown-content {
    left: -25%;
  }
}
</style>
