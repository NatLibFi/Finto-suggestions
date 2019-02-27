<template>
  <div class="user">
    <div class="profile-container">
      <div class="user-name-initials">{{ userNameInitials }}</div>
      <div v-if="user || userId" class="profile">
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
    </div>

    <div class="setting-container">
      <user-settings-form />
    </div>
  </div>
</template>

<script>
import UserSettingsForm from './UserSettingsForm';
import { userNameInitials } from '../../utils/userHelpers.js';
import { userRoleToString } from '../../utils/userMappings.js';

import { userActions, userGetters } from '../../store/modules/user/userConsts';
import { mapUserActions, mapUserGetters } from '../../store/modules/user/userModule';
// eslint-disable-next-line
import { authenticatedUserGetters, authenticatedUserActions } from '../../store/modules/authenticatedUser/authenticatedUserConsts.js';
// eslint-disable-next-line
import { mapAuthenticatedUserGetters, mapAuthenticatedUserActions } from '../../store/modules/authenticatedUser/authenticatedUserModule.js';

export default {
  components: {
    UserSettingsForm
  },
  data() {
    return {
      userRoleToString,
      userNameInitials: '',
      isTouched: false
    };
  },
  computed: {
    ...mapAuthenticatedUserGetters({
      userId: authenticatedUserGetters.GET_USER_ID,
      isAuthenticated: authenticatedUserGetters.GET_IS_AUTHENTICATED,
      name: authenticatedUserGetters.GET_USER_NAME
    }),
    ...mapUserGetters({
      user: userGetters.GET_USER
    })
  },
  async created() {
    this.getUserIdFromStorage();
    await this.getUser(this.userId);
    await this.fetchUserNameAndInitials();
  },
  methods: {
    ...mapAuthenticatedUserActions({
      getUserIdFromStorage: authenticatedUserActions.GET_USER_ID_FROM_STORAGE,
      getUserName: authenticatedUserActions.GET_USER_NAME
    }),
    ...mapUserActions({
      getUser: userActions.GET_USER
    }),
    fetchUserNameAndInitials() {
      if (this.user) {
        this.userNameInitials = userNameInitials(this.user.name);
      }
    }
  }
};
</script>

<style scoped>
.profile-container {
  position: relative;
  background-color: #ffffff;
  border: 2px solid #f5f5f5;
  text-align: left;
  margin: 20px 20vw 0;
  padding: 10px 40px;
  height: 80px;
  overflow: hidden;
}

.setting-container {
  position: relative;
  background-color: #ffffff;
  border: 2px solid #f5f5f5;
  text-align: left;
  padding: 10px 40px;
  margin: 6px 20vw 0;
  height: 100%;
  overflow: hidden;
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

@media (max-width: 700px) {
  .profile-container,
  .setting-container {
    height: initial;
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

  .setting-container {
    padding-top: 6px;
    margin-top: 10px;
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
