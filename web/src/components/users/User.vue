<template>
  <div class="user">

      <!-- User text block -->
      <!-- <span> Onko käyttäjä autentikoitu: {{ isAuthenticated }} </span> -->
      <!-- <span> UserNameInitials (imports) {{ userNameInitials }} </span> -->
      <!-- <span> userRoleToString  (imports) {{ userRoleToString }} </span> -->
      <!-- <span> userId (imports) {{ userId }} </span> -->
      <!-- <span> User  (imports) {{ user }} </span> -->
      <!-- <span> authenticatedUserGetters  (imports) {{ authenticatedUserGetters }} </span>
      <span> mapAuthenticatedUserGetters  (imports) {{ mapAuthenticatedUserGetters }} </span> -->


    <div class="profile-container">
      <transition name="fade">
        <div v-if="user.imageUrl" class="profile-image">
          <img :src="user.imageUrl" :alt="userNameInitials" />
        </div>
        <div v-if="!user.imageUrl" class="user-name-initials">
          <span v-if="userNameInitials">{{ userNameInitials }}</span>
        </div>
      </transition>
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
      <div v-if="isAuthenticated && loggedInUserId === userId" class="settings">
        <div @click="showDropdown = true">
          <svg-icon icon-name="more"><icon-more /></svg-icon>
        </div>
        <div v-if="showDropdown" v-on-clickaway="closeDropdown" class="dropdown">
          <div @click="goToSettings">Muokkaa profiilia</div>
        </div>
      </div>
    </div>

    <suggestion-list-header :userPage="true" class="header" />
    <suggestion-list :userId="userId" :page="page" :isUserPage="true" />
  </div>
</template>

<script>
import SuggestionListHeader from '../suggestion/SuggestionListHeader';
import SuggestionItem from '../suggestion/SuggestionItem';
import SuggestionList from '../suggestion/SuggestionList';

import { userGetters, userActions } from '../../store/modules/user/userConsts';
import { mapUserGetters, mapUserActions } from '../../store/modules/user/userModule';
import { userNameInitials } from '../../utils/userHelpers.js';
import { userRoleToString } from '../../utils/userMappings.js';
// eslint-disable-next-line
import { authenticatedUserGetters } from '../../store/modules/authenticatedUser/authenticatedUserConsts.js';
// eslint-disable-next-line
import { mapAuthenticatedUserGetters } from '../../store/modules/authenticatedUser/authenticatedUserModule.js';

import SvgIcon from '../icons/SvgIcon';
import IconMore from '../icons/IconMore';
import { directive as onClickaway } from 'vue-clickaway';

export default {
  components: {
    SuggestionListHeader,
    SuggestionList,
    SuggestionItem,
    SvgIcon,
    IconMore
  },
  directives: {
    onClickaway: onClickaway
  },
  props: {
    userId: {
      type: [String, Number],
      required: true
    },
    page: {
      type: [String, Number],
      required: true,
      default: 1
    }
  },
  data() {
    return {
      filters: this.$route.query.filters ? this.$route.query.filters : '',
      searchWord: this.$route.query.search ? this.$route.query.search : '',
      sort: this.$route.query.sort ? this.$route.query.sort : '',
      userRoleToString,
      userNameInitials: '',
      showDropdown: false
    };
  },
  computed: {
    ...mapAuthenticatedUserGetters({
      loggedInUserId: authenticatedUserGetters.GET_USER_ID,
      isAuthenticated: authenticatedUserGetters.GET_IS_AUTHENTICATED
    }),
    ...mapUserGetters({
      user: userGetters.GET_AUTHENTICATED_USER
    })
  },
  created() {
    this.fetchUserNameAndInitials();
  },
  methods: {
    fetchUserNameAndInitials() {
      if (this.user) {
        this.userNameInitials = userNameInitials(this.user.name);
      }
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
  transform: perspective(1px) translateY(calc(-50% - 0.5px));
  display: inline-block;
  height: 50px;
  width: 50px;
  border-radius: 50px;
  line-height: 52px;
  text-align: center;
  background-color: #dddddd;
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
  transform: perspective(1px) translateY(calc(-50% - 0.5px));
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

.profile-image {
  position: absolute;
  height: 50px;
  width: 50px;
  top: 50%;
  left: initial;
  transform: perspective(1px) translateY(calc(-50% - 0.5px));
  display: inline-block;
  border-radius: 50px;
  margin-right: 20px;
  text-align: center;
}

.profile-image img {
  height: 50px;
  width: 50px;
  background-color: #eeeeee;
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
}

.dropdown:hover {
  background-color: #f3fbfa;
  cursor: pointer;
  cursor: hand;
}

.dropdown div {
  padding: 10px 16px;
}

.user-suggestions {
  margin-bottom: 40px;
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
  transform: perspective(1px) translateY(calc(-50% - 0.5px));
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

  .no-user-suggestions-container {
    margin: 20px 10vw 0;
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
