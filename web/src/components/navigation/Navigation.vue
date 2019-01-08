<template>
  <div class="navigation">

    <div class="nav-content">
      <div class="nav-title">
        <img @click="returnToHome" src="./finto-logo.svg" alt="">
        <span @click="returnToHome">Finto – Käsite-ehdotukset</span>
      </div>

      <transition name="fade">
        <div v-if="isAuthenticated" class="nav-menu" @click="showDropdown = true">
          <div class="user-bubble">
            <span unselectable="on">{{ userInitials }}</span>
          </div>
          <div class="nav-menu-user">
            <p v-if="name && name.length > 0">{{ name }}</p>
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
        <div v-if="isAuthenticated" class="nav-menu-mobile" @click="showMobileDropdown = true">
          <svg-icon icon-name="more"><icon-more/></svg-icon>
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
      <div class="disabled">Profiili</div>
      <div class="disabled">Asetukset</div>
      <div @click="logOut">Kirjaudu ulos</div>
    </div>

    <div
      v-if="showMobileDropdown"
      v-on-clickaway="closeMobileDropdown"
      class="nav-mobile-dropdown dropdown">
      <div class="nav-mobile-dropdown-header">
        <div class="user-bubble">
          <span unselectable="on">{{ userInitials }}</span>
        </div>
        <div class="nav-dropdown-user">
          <p>{{ userName }}</p>
        </div>
      </div>
      <div class="nav-mobile-dropdown-content">
        <div class="disabled">Profiili</div>
        <div class="disabled">Asetukset</div>
        <div @click="logOut">Kirjaudu ulos</div>
      </div>
    </div>

    <div v-if="showLoginDialog">
      <centered-dialog @close="closeDialog">
        <the-login @login="login"/>
      </centered-dialog>
    </div>
    <div v-if="showSignupDialog">
      <centered-dialog @close="closeDialog">
        <the-signup @signup="signup"/>
      </centered-dialog>
    </div>
    <div v-if="showSignupConfirmation">
      <centered-dialog @close="closeDialog">
        <the-signup-confirmation/>
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

import { mapAuthenticatedUserGetters, mapAuthenticatedUserActions } from '../../store/modules/authenticatedUser/authenticatedUserModule.js';
import { authenticatedUserGetters, authenticatedUserActions } from '../../store/modules/authenticatedUser/authenticatedUserConsts.js';

import api from '../../api/index.js';
import { userNameInitials } from '../../utils/nameHelpers.js';

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
  data: () => ({
    userInitials: '',
    loginProvider: '',
    registerData: null,
    showDropdown: false,
    showMobileDropdown: false,
    showLoginDialog: false,
    showSignupDialog: false,
    showSignupConfirmation: false
  }),
  created() {
    this.validateAuthentication();
    this.getUserIdFromStorage();

    this.handleUserFetch();
    this.handleUserInitialsFetch();
  },
  computed: {
    ...mapAuthenticatedUserGetters({
      isAuthenticated: authenticatedUserGetters.GET_AUTHENTICATION,
      userId: authenticatedUserGetters.GET_USER_ID,
      name: authenticatedUserGetters.GET_USER_NAME
    })
  },
  methods: {
    ...mapAuthenticatedUserActions({
      authenticateGithubUser: authenticatedUserActions.AUTHENTICATE,
      validateAuthentication: authenticatedUserActions.VALIDATE_AUTHENTICATION,
      revokeAuthentication: authenticatedUserActions.REVOKE_AUTHENTICATION,
      getUserName: authenticatedUserActions.GET_USER_NAME,
      authenticateLocalUser: authenticatedUserActions.AUTHENTICATE_LOCAL_USER,
      getUserIdFromStorage: authenticatedUserActions.GET_USER_ID_FROM_STORAGE
    }),
    returnToHome() {
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
    },
    async login(data) {
      if (data) {
        if (data.service !== '' && data.service !== 'local') {
          await this.oAuth2Authenticate(data.service);
        } else {
          await this.authenticateLocalUser(data.loginData);
        }
      }
      this.handleUserFetch();
      this.showLoginDialog = false;
    },
    async signup(data) {
      if (data && data.service !== 'local') {
        await this.oAuth2Authenticate(data.service);
      } else {
        await this.registerLocalUser(data.userdata);
      }
      this.showSignupDialog = false;
      this.showSignupConfirmation = true;
    },
    logOut() {
      this.revokeAuthentication();
      this.closeDropdown();
      this.closeMobileDropdown();
    },
    async oAuth2Authenticate(provider) {
      await this.authenticateGithubUser({ providerName: provider });
    },
    async registerLocalUser(userdata) {
      await api.user.registerLocalUser(userdata);
    },
    handleUserFetch() {
      if(parseInt(this.userId) > 0){
        this.getUserName(parseInt(this.userId));
      }
    },
    handleUserInitialsFetch() {
      this.userInitials = userNameInitials(this.name);
    }
  },
  watch: {
    name() {
      this.handleUserInitialsFetch();
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
  transform: perspective(1px) translateY(-50%);
  height: 60px;
  line-height: 60px;
  width: 45%;
}

.nav-title img {
  position: absolute;
  top: 51%;
  left: 0;
  transform: perspective(1px) translateY(-50%);
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
  transform: perspective(1px) translateY(-50%);
  font-weight: 600;
}

.nav-login-buttons,
.nav-login-buttons-mobile {
  position: absolute;
  top: 50%;
  right: 40px;
  transform: perspective(1px) translateY(-47%);
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
  transform: perspective(1px) translateY(-50%);
  color: #1ea195;
  font-weight: 600;
  font-size: 15px;
  cursor: pointer;
  cursor: hand;
}

.nav-menu .user-bubble {
  position: relative;
  top: 50%;
  transform: perspective(1px) translateY(-50%);
  overflow: hidden;
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
  transform: perspective(1px) translateY(-50%);
  height: 100%;
}

.nav-menu-mobile svg {
  position: relative;
  top: 55%;
  transform: perspective(1px) translateY(-50%);
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
}

.nav-menu-dropdown div {
  padding: 16px 20px;
  border-bottom: 1px solid #f5f5f5;
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
}

.nav-mobile-dropdown-header .user-bubble {
  height: 50px;
  width: 50px;
  line-height: 50px;
  font-size: 16px;
}

.nav-mobile-dropdown-header .nav-dropdown-user {
  display: inline-block;
  margin-left: 30px;
  font-size: 16px;
  line-height: 16px;
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
  -webkit-box-shadow: 6px 8px 17px -6px rgba(80, 80, 80, 0.35);
  -moz-box-shadow: 6px 8px 17px -6px rgba(80, 80, 80, 0.35);
  box-shadow: 6px 8px 17px -6px rgba(80, 80, 80, 0.35);
}

.user-bubble {
  display: inline-block;
  height: 35px;
  width: 35px;
  border-radius: 35px;
  line-height: 35px;
  text-align: center;
  background-color: #804af2;
  color: #ffffff;
  font-size: 14px;
  font-weight: 800;
}

.disabled {
  color: #ccc;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.4s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
</style>
