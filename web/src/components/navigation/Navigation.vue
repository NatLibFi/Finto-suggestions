<template>
  <div class="navigation">
    <div class="nav-content">
      <div class="nav-title">
        <img @click="returnToHome" src="../assets/finto-logo.svg" alt="" />
        <span @click="returnToHome">Finto – Käsite-ehdotukset</span>
      </div>
      <div class="refresh-button">
        <p>
          [
          <a href="javascript:location.reload(true)">Refresh</a>
          ]
        </p>
      </div>
      <transition name="fade">
        <div v-if="isAuthenticated && user.name" class="nav-menu" @click="showDropdown = true">
          <transition name="fade">
            <div v-if="user.imageUrl" class="user-bubble-image">
              <img :src="user.imageUrl" alt="userInitials" />
            </div>
          </transition>
          <div v-if="!user.imageUrl" class="user-bubble">
            <transition name="fade">
              <span v-if="userInitials" unselectable="on">{{ userInitials }}</span>
            </transition>
          </div>
          <div class="nav-menu-user">
            <p v-if="user.name && user.name.length > 0">{{ user.name }}</p>
            <p v-if="user.name && user.name.length === 0">Käyttäjä {{ userId }}</p>
          </div>
          <svg-icon icon-name="triangle"><icon-triangle /></svg-icon>
        </div>
      </transition>
      <transition name="fade">
        <div v-if="!isAuthenticated" class="nav-login-buttons">
          <div @click="showLoginDialog = !showLoginDialog">Kirjaudu sisään</div>
          <div @click="showSignupDialog = !showSignupDialog">Luo tunnus</div>
        </div>
      </transition>
      <transition name="fade">
        <!-- Mobile menu shown below screen width of 700px -->
        <div
          v-if="isAuthenticated && user.name"
          class="nav-menu-mobile"
          @click="showMobileDropdown = true"
        >
          <svg-icon icon-name="more"><icon-more /></svg-icon>
        </div>
      </transition>
      <transition name="fade">
        <div v-if="!isAuthenticated" class="nav-login-buttons-mobile">
          <div @click="showLoginDialog = !showLoginDialog">Kirjaudu sisään</div>
          <div @click="showSignupDialog = !showSignupDialog">Luo tunnus</div>
        </div>
      </transition>
    </div>

    <div v-if="showDropdown" v-on-clickaway="closeDropdown" class="nav-menu-dropdown dropdown">
      <div @click="goToProfile">Profiili</div>
      <div @click="goToSettings">Asetukset</div>
      <div @click="logOut">Kirjaudu ulos</div>
    </div>

    <div
      v-if="showMobileDropdown"
      v-on-clickaway="closeMobileDropdown"
      class="nav-mobile-dropdown dropdown"
    >
      <div class="nav-mobile-dropdown-header">
        <transition name="fade">
          <div v-if="user.imageUrl" class="user-bubble-image">
            <img :src="user.imageUrl" alt="userInitials" />
          </div>
        </transition>
        <div v-if="!user.imageUrl" class="user-bubble">
          <span unselectable="on">{{ userInitials }}</span>
        </div>
        <div class="nav-dropdown-user">
          <p v-if="user.name && user.name.length > 0">{{ user.name }}</p>
          <p v-if="user.name && user.name.length === 0">Käyttäjä {{ userId }}</p>
        </div>
      </div>
      <div class="nav-mobile-dropdown-content">
        <div @click="goToProfile">Profiili</div>
        <div @click="goToSettings">Asetukset</div>
        <div @click="logOut">Kirjaudu ulos</div>
      </div>
    </div>

    <div v-if="showLoginDialog">
      <centered-dialog @close="closeDialog">
        <the-login
          :showResetPasswordForm="showResetPasswordForm"
          :showLocalLoginError="showLocalLoginError"
          @login="login"
          @resetPassword="resetPassword"
        />
      </centered-dialog>
    </div>
    <div v-if="showSignupDialog">
      <centered-dialog @close="closeDialog">
        <the-signup @signup="signup" />
      </centered-dialog>
    </div>
    <div v-if="showSignupConfirmation">
      <centered-dialog @close="closeDialog">
        <the-signup-confirmation
          :signupSucceeded="signupSucceeded"
          :errorMessage="signupError"
          @openResetPasswordForm="openResetPasswordForm"
        />
      </centered-dialog>
    </div>
  </div>
</template>

<script>
import CenteredDialog from '../common/CenteredDialog';
import TheLogin from '../auth/TheLogin';
import TheSignup from '../auth/TheSignup';
import TheSignupConfirmation from '../auth/TheSignupConfirmation';
import SvgIcon from '../icons/SvgIcon';
import IconMore from '../icons/IconMore';
import IconTriangle from '../icons/IconTriangle';
import { directive as onClickaway } from 'vue-clickaway';
import router from '../../router/index';
import { userGetters, userActions } from '../../store/modules/user/userConsts';
import { mapUserGetters, mapUserActions } from '../../store/modules/user/userModule';
// eslint-disable-next-line
import { mapAuthenticatedUserGetters, mapAuthenticatedUserActions } from '../../store/modules/authenticatedUser/authenticatedUserModule';
// eslint-disable-next-line
import { authenticatedUserGetters, authenticatedUserActions, storeKeyNames, authenticatedUserMutations } from '../../store/modules/authenticatedUser/authenticatedUserConsts';

import { userNameInitials } from '../../utils/userHelpers.js';

//The following two lines are for testing purposes at the moment
// eslint-disable-next-line no-unused-vars
import { mapMeetingGetters, mapMeetingActions } from '../../store/modules/meeting/meetingModule.js';
// eslint-disable-next-line no-unused-vars
import { meetingGetters, meetingActions } from '../../store/modules/meeting/meetingConsts.js';

export default {
  components: {
    CenteredDialog,
    TheLogin,
    TheSignup,
    TheSignupConfirmation,
    SvgIcon,
    IconMore,
    IconTriangle
  },
  directives: {
    onClickaway: onClickaway
  },
  data() {
    return {
      userInitials: '',
      userNameInitials: '',
      loginProvider: '',
      registerData: null,
      showDropdown: false,
      showMobileDropdown: false,
      showLoginDialog: false,
      showSignupDialog: false,
      showSignupConfirmation: false,
      signupSucceeded: true,
      signupError: '',
      showResetPasswordForm: false,
      showLocalLoginError: false
    };
  },
  computed: {
    ...mapAuthenticatedUserGetters({
      isAuthenticated: authenticatedUserGetters.GET_IS_AUTHENTICATED,
      userId: authenticatedUserGetters.GET_USER_ID,
      // can be shown if login did not succeed:
      error: authenticatedUserGetters.GET_AUTHENTICATE_ERROR
    }),
    ...mapUserGetters({
      user: userGetters.GET_AUTHENTICATED_USER
    }),
    ...mapMeetingGetters({
      selectedSort: meetingGetters.GET_MEETINGS_SELECTED_SORT
    })
  },
  async created() {
    await this.validateAuthentication();
    if (this.isAuthenticated) {
      await this.refreshToken();
      await this.getUserIdFromStorage();
      await this.handleUserFetch();
      await this.handleUserInitialsFetch();
    }
  },
  methods: {
    ...mapAuthenticatedUserActions({
      validateAuthentication: authenticatedUserActions.VALIDATE_AUTHENTICATION,
      revokeAuthentication: authenticatedUserActions.REVOKE_AUTHENTICATION,
      authenticateLocalUser: authenticatedUserActions.AUTHENTICATE_LOCAL_USER,
      getUserIdFromStorage: authenticatedUserActions.GET_USER_ID_FROM_STORAGE,
      refreshToken: authenticatedUserActions.REFRESH_AUTHORIZATION_TOKEN
    }),
    ...mapUserActions({
      resetPasswordByEmail: userActions.RESET_PASSWORD,
      registerLocalUser: userActions.CREATE_USER,
      getAuthenticatedUser: userActions.GET_AUTHENTICATED_USER
    }),
    async returnToHome() {
      this.$router.push('/');
    },
    closeDropdown() {
      this.showDropdown = false;
    },
    closeMobileDropdown() {
      this.showMobileDropdown = false;
    },
    closeDialog() {
      this.showLoginDialog = false;
      this.showSignupDialog = false;
      this.showSignupConfirmation = false;
      this.showLocalLoginError = false;
    },
    async login(data) {
      if (data) {
        if (data.service !== '' && data.service !== 'local') {
          await this.oAuth2Authenticate(data.service);
        } else {
          await this.authenticateLocalUser(data.loginData)
            .then(() => {
              if (this.userId) {
                this.getAuthenticatedUser(this.userId);
                this.showLoginDialog = false;
              }
            })
            .catch(() => {
              this.showLocalLoginError = true;
            });
          if (window.localStorage) {
            if (!localStorage.getItem('loadedOnce')) {
              localStorage['loadedOnce'] = true;
              // window.location.reload();
            } else localStorage.removeItem('firstLoad');
          }
        }
      }
      window.location.reload();
    },
    async signup(data) {
      if (data && data.service !== 'local') {
        await this.oAuth2Authenticate(data.service);
      } else {
        const createdUserResponse = await this.registerLocalUser(data.userdata);
        this.signupSucceeded = createdUserResponse.success;
        this.signupError = createdUserResponse.error;
      }
      this.showSignupDialog = false;
      this.showSignupConfirmation = true;
    },
    goToProfile: function() {
      this.$router.push({
        name: 'user',
        params: {
          userId: this.userId,
          page: 1
        }
      });
      this.showDropdown = false;
      this.showMobileDropdown = false;
    },
    goToSettings: function() {
      this.$router.push({
        name: 'settings',
        params: {
          userId: this.userId
        }
      });
      this.showDropdown = false;
      this.showMobileDropdown = false;
    },
    logOut() {
      alert('NOTE! You must close all Finto-suggestion tabs');
      console.log('Router: ' + router.history.current.name);
      this.revokeAuthentication();
      this.closeDropdown();
      this.closeMobileDropdown();
      localStorage.removeItem('userIdTemp');
      sessionStorage.removeItem('userId');
      location.reload();
    },
    async oAuth2Authenticate() {
      this.$router.push('/github');
    },
    async handleUserFetch() {
      if (parseInt(this.userId, 10) > 0) {
        this.getAuthenticatedUser(this.userId);
        this.handleUserInitialsFetch();
      }
    },
    handleUserInitialsFetch() {
      this.userNameInitials = userNameInitials(this.user.name);
    },
    async resetPassword(email) {
      await this.resetPasswordByEmail(email)
        .then(() => {})
        .catch(() => {
          console.log('Resetting failed.');
        });
    },
    openResetPasswordForm() {
      this.showSignupConfirmation = false;
      this.showResetPasswordForm = true;
      this.showLoginDialog = true;
    }
  },
  mounted: function() {
    document.addEventListener('keydown', e => {
      if (e.keyCode === 27) {
        this.closeDropdown();
        this.closeMobileDropdown();
      }
    });
  }
};
</script>

<style scoped>
.navigation {
  width: 100%;
  overflow: hidden;
  border-bottom: 2px solid #f5f5f5;
  background-color: #ffffff;
  -webkit-user-select: none; /* Safari */
  -moz-user-select: none; /* Firefox */
  -ms-user-select: none; /* IE10+/Edge */
  user-select: none; /* Standard */
}

.nav-content {
  position: relative;
  height: 60px;
}

.nav-title {
  position: absolute;
  top: 50%;
  left: 40px;
  transform: perspective(1px) translateY(calc(-50% - 0.5px));
  height: 60px;
  line-height: 60px;
  width: 45%;
}

.refresh-button {
  position: absolute;
  top: 25%;
  right: 20%;
  transform: perspective(1px) translateX(calc(-50% - 10.5px));
  transform: perspective(1px) translateY(calc(-50% - 0.5px));
  height: 60px;
  line-height: 60px;
  width: 45%;
}

.refresh-button a {
  text-decoration: none;
}

.nav-title img {
  position: absolute;
  top: 51%;
  left: 0;
  transform: perspective(1px) translateY(calc(-50% - 0.5px));
}

.nav-title img:hover,
.nav-title span:hover {
  opacity: 0.9;
  cursor: pointer;
  cursor: hand;
}

.nav-title span {
  display: inline-block;
  position: absolute;
  top: 56%;
  left: 90px;
  transform: perspective(1px) translateY(calc(-50% - 0.5px));
  font-weight: 600;
}

.nav-login-buttons,
.nav-login-buttons-mobile {
  position: absolute;
  top: 50%;
  right: 40px;
  transform: perspective(1px) translateY(calc(-47% - 0.5px));
  height: 60px;
  line-height: 60px;
  width: 45%;
  font-size: 14px;
  font-weight: 600;
  color: #06a798;
  text-align: right;
  cursor: pointer;
  cursor: hand;
}

.nav-login-buttons-mobile {
  display: none;
}

.nav-login-buttons div,
.nav-login-buttons-mobile div {
  display: inline-block;
}

.nav-login-buttons div:last-of-type,
.nav-login-buttons-mobile div:last-of-type {
  margin-left: 20px;
}

.nav-menu {
  position: absolute;
  right: 0;
  padding: 0 40px 0 20px;
  top: 52%;
  height: 100%;
  transform: perspective(1px) translateY(calc(-50% - 0.5px));
  color: #1ea195;
  font-weight: 600;
  font-size: 15px;
  cursor: pointer;
  cursor: hand;
}

.nav-menu .user-bubble,
.nav-menu .user-bubble-image {
  position: relative;
  top: 50%;
  transform: perspective(1px) translateY(calc(-50% - 0.5px));
  overflow: hidden;
}

.nav-menu .user-bubble-image img {
  height: 35px;
  width: 35px;
  background-color: #eeeeee;
}

.nav-menu .nav-menu-user {
  display: inline;
  vertical-align: middle;
}

.nav-menu .nav-menu-user p {
  display: inline;
  margin: 0 0 0 14px;
}

.nav-menu svg {
  margin: 0 0 -13px 10px;
}

.nav-menu-mobile {
  display: none;
  position: absolute;
  right: 0;
  padding-right: 40px;
  top: 50%;
  transform: perspective(1px) translateY(calc(-50% - 0.5px));
  height: 100%;
}

.nav-menu-mobile svg {
  position: relative;
  top: 55%;
  transform: perspective(1px) translateY(calc(-50% - 0.5px));
  display: inline-block;
  margin: 0 0 -8px 10px;
  background-size: 24px 24px;
}

.nav-menu-dropdown {
  position: absolute;
  z-index: 2;
  top: 55px;
  right: 40px;
  width: 200px;
  box-sizing: border-box;
  -moz-box-sizing: border-box;
  -webkit-box-sizing: border-box;
  overflow: hidden;
}

.nav-menu-dropdown div {
  padding: 16px 20px;
  border-bottom: 1px solid #f5f5f5;
  box-sizing: border-box;
  -moz-box-sizing: border-box;
  -webkit-box-sizing: border-box;
}

.nav-menu-dropdown div:last-of-type {
  border-bottom: none;
}

.nav-menu-dropdown div:hover {
  background-color: #f3fbfa;
  cursor: pointer;
  cursor: hand;
}

.nav-mobile-dropdown {
  display: none;
  position: absolute;
  z-index: 2;
  top: 50px;
  right: 1px;
  width: 300px;
}

.nav-mobile-dropdown-header {
  padding: 20px;
  padding-top: 24px;
  border-bottom: 1px solid #f5f5f5;
  position: relative;
  height: 60px;
}

.nav-mobile-dropdown-header .user-bubble,
.nav-mobile-dropdown-header .user-bubble-image {
  height: 50px;
  width: 50px;
  line-height: 50px;
  font-size: 16px;
  position: absolute;
  top: 50%;
  transform: perspective(1px) translateY(calc(-50% - 0.5px));
}

.nav-mobile-dropdown-header .user-bubble-image img {
  height: 50px;
  width: 50px;
  border-radius: 50px;
}

.nav-mobile-dropdown-header .nav-dropdown-user {
  display: inline-block;
  margin-left: 30px;
  font-size: 16px;
  line-height: 16px;
  position: absolute;
  left: 60px;
  top: 50%;
  transform: perspective(1px) translateY(calc(-50% - 0.5px));
}

.nav-mobile-dropdown-content div {
  padding: 16px 20px;
  border-bottom: 1px solid #f5f5f5;
}

.nav-mobile-dropdown-content div:last-of-type {
  padding: 16px 20px;
  border-bottom: 1px solid #f5f5f5;
}

.nav-mobile-dropdown-content div:hover {
  background-color: #f3fbfa;
  cursor: pointer;
  cursor: hand;
}

@media (max-width: 700px) {
  .nav-title {
    left: 20px;
  }

  .nav-title span {
    display: none;
  }

  .nav-login-buttons {
    display: none;
  }

  .nav-login-buttons-mobile {
    display: initial;
  }

  .nav-login-buttons-mobile div {
    font-size: 11px;
  }

  .nav-login-buttons div:last-of-type,
  .nav-login-buttons-mobile div:last-of-type {
    margin-left: 8px;
  }

  .nav-menu {
    display: none;
  }

  .nav-menu-mobile {
    display: initial;
    padding-right: 20px;
  }

  .nav-menu-dropdown {
    display: none;
  }

  .nav-mobile-dropdown {
    display: initial;
  }
}

.dropdown {
  font-size: 15px;
  font-weight: 600;
  color: #555555;
  text-align: left;
  background-color: #ffffff;
  border: 1px solid #e1e1e1;
  border-radius: 2px;
}

.user-bubble,
.user-bubble-image {
  display: inline-block;
  height: 35px;
  width: 35px;
  border-radius: 35px;
  line-height: 36px;
  text-align: center;
  background-color: #dddddd;
  color: #ffffff;
  font-size: 13px;
  font-weight: 800;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.4s;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}

.disabled {
  color: #ccc;
  cursor: default !important;
}
</style>
