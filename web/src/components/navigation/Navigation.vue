<template>
  <div class="navigation">

    <div class="nav-content">
      <div class="nav-title">
        <img @click="returnToHome" src="./finto-logo.svg" alt="">
        <span>Finto – Käsite-ehdotukset</span>
      </div>
      <div v-if="isAuthenticated" class="nav-menu" @click="showDropdown = true">
        <div class="user-bubble">
          <span unselectable="on">{{ userInitials }}</span>
        </div>
        <div class="nav-menu-user">
          <p>{{ userName }}</p>
        </div>
        <svg-icon icon-name="triangle"><icon-triangle /></svg-icon>
      </div>
      <div v-if="!isAuthenticated" class="nav-login-buttons">
        <div @click="showLoginDialog = !showLoginDialog">Kirjaudu sisään</div>
        <div @click="showSignupDialog = !showSignupDialog">Luo tunnus</div>
      </div>
      <!-- Mobile menu shown below screen width of 700px -->
      <div v-if="isAuthenticated" class="nav-menu-mobile" @click="showMobileDropdown = true">
        <svg-icon icon-name="more"><icon-more/></svg-icon>
      </div>
      <div v-if="!isAuthenticated" class="nav-login-buttons-mobile">
        <div @click="showLoginDialog = !showLoginDialog">Kirjaudu sisään</div>
        <div @click="showSignupDialog = !showSignupDialog">Luo tunnus</div>
      </div>
    </div>

    <div v-if="showDropdown" v-on-clickaway="closeDropdown" class="nav-menu-dropdown dropdown">
      <div>Profiili</div>
      <div>Asetukset</div>
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
        <div>Profiili</div>
        <div>Asetukset</div>
        <div @click="logOut">Kirjaudu ulos</div>
      </div>
    </div>

    <div v-if="showLoginDialog">
      <centered-dialog @close="closeDialog">
        <the-login @login="login($event)"/>
      </centered-dialog>
    </div>
    <div v-if="showSignupDialog">
      <centered-dialog @close="closeDialog">
        <the-signup @signup="signup($event)"/>
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

import { mapAuthGetters, mapAuthActions } from '../../store/modules/auth/authModule.js';
import { authGetters, authActions } from '../../store/modules/auth/authConsts.js';

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
    userInitials: 'MP',
    userName: 'Miki Pernu',
    showDropdown: false,
    showMobileDropdown: false,
    showLoginDialog: false,
    showSignupDialog: false,
    showSignupConfirmation: false
  }),
  computed: {
    ...mapAuthGetters({ isAuthenticated: authGetters.GET_IS_USER_AUTHENTICATED })
  },
  methods: {
    ...mapAuthActions({ authenticate: authActions.AUTHENTICATE }),
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
    // TODO: connect these with the authentication service, remove console.logs
    login(service) {
      this.showLoginDialog = false;
      console.log(service);
      this.authenticate({ providerName: service, user: {}, requestOptions: {} });
    },
    signup(service) {
      console.log(service);
      this.authenticate({ providerName: service, user: {}, requestOptions: {} });
      this.showSignupDialog = false;
      this.showSignupConfirmation = true;
    },
    logOut() {
      this.closeDropdown();
      this.closeMobileDropdown();
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
div.navigation {
  width: 100%;
  overflow: hidden;
  border-bottom: 2px solid #f5f5f5;
  background-color: #ffffff;
  -webkit-user-select: none; /* Safari */
  -moz-user-select: none; /* Firefox */
  -ms-user-select: none; /* IE10+/Edge */
  user-select: none; /* Standard */
}

div.nav-content {
  position: relative;
  height: 60px;
}

div.nav-title {
  position: absolute;
  top: 50%;
  left: 40px;
  transform: perspective(1px) translateY(-50%);
  height: 60px;
  line-height: 60px;
  width: 45%;
}

div.nav-title img {
  position: absolute;
  top: 51%;
  left: 0;
  transform: perspective(1px) translateY(-50%);
  cursor: pointer;
  cursor: hand;
}

div.nav-title img:hover {
  opacity: 0.9;
}

div.nav-title span {
  display: inline-block;
  position: absolute;
  top: 56%;
  left: 90px;
  transform: perspective(1px) translateY(-50%);
  font-weight: 600;
}

div.nav-login-buttons,
div.nav-login-buttons-mobile {
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

div.nav-login-buttons-mobile {
  display: none;
}

div.nav-login-buttons div,
div.nav-login-buttons-mobile div {
  display: inline-block;
}

div.nav-login-buttons div:last-of-type,
div.nav-login-buttons-mobile div:last-of-type {
  margin-left: 20px;
}

div.nav-menu {
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

div.nav-menu .user-bubble {
  position: relative;
  top: 50%;
  transform: perspective(1px) translateY(-50%);
  overflow: hidden;
}

div.nav-menu .nav-menu-user {
  display: inline;
  vertical-align: middle;
}

div.nav-menu .nav-menu-user p {
  display: inline;
  margin: 0 0 0 14px;
}

div.nav-menu svg {
  margin: 0 0 -13px 10px;
}

div.nav-menu-mobile {
  display: none;
  position: absolute;
  right: 0;
  padding-right: 40px;
  top: 50%;
  transform: perspective(1px) translateY(-50%);
  height: 100%;
}

div.nav-menu-mobile svg {
  position: relative;
  top: 55%;
  transform: perspective(1px) translateY(-50%);
  display: inline-block;
  margin: 0 0 -8px 10px;
  background-size: 24px 24px;
}

div.nav-menu-dropdown {
  position: absolute;
  z-index: 2;
  top: 55px;
  right: 40px;
  width: 200px;
}

div.nav-menu-dropdown div {
  padding: 16px 20px;
  border-bottom: 1px solid #f5f5f5;
}

div.nav-menu-dropdown div:last-of-type {
  border-bottom: none;
}

div.nav-menu-dropdown div:hover {
  background-color: #f3fbfa;
  cursor: pointer;
  cursor: hand;
}

div.nav-mobile-dropdown {
  display: none;
  position: absolute;
  z-index: 2;
  top: 50px;
  right: 1px;
  width: 300px;
}

div.nav-mobile-dropdown-header {
  padding: 20px;
  padding-top: 24px;
  border-bottom: 1px solid #f5f5f5;
}

div.nav-mobile-dropdown-header .user-bubble {
  height: 50px;
  width: 50px;
  line-height: 50px;
  font-size: 16px;
}

div.nav-mobile-dropdown-header .nav-dropdown-user {
  display: inline-block;
  margin-left: 30px;
  font-size: 16px;
  line-height: 16px;
}

div.nav-mobile-dropdown-content div {
  padding: 16px 20px;
  border-bottom: 1px solid #f5f5f5;
}

div.nav-mobile-dropdown-content div:last-of-type {
  padding: 16px 20px;
  border-bottom: 1px solid #f5f5f5;
}

div.nav-mobile-dropdown-content div:hover {
  background-color: #f3fbfa;
  cursor: pointer;
  cursor: hand;
}

@media (max-width: 700px) {
  div.nav-title {
    left: 20px;
  }

  div.nav-title span {
    display: none;
  }

  div.nav-login-buttons {
    display: none;
  }

  div.nav-login-buttons-mobile {
    display: initial;
  }

  div.nav-login-buttons-mobile div {
    font-size: 11px;
  }

  div.nav-login-buttons div:last-of-type,
  div.nav-login-buttons-mobile div:last-of-type {
    margin-left: 8px;
  }

  div.nav-menu {
    display: none;
  }

  div.nav-menu-mobile {
    display: initial;
    padding-right: 20px;
  }

  div.nav-menu-dropdown {
    display: none;
  }

  div.nav-mobile-dropdown {
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
</style>
