<template>
  <div class="login-dialog">
    <h3 v-if="!showForgottenPasswordForm">Kirjaudu sisään</h3>
    <!-- TODO: uncomment this when google oauth2 is ready -->
    <!-- <p>Voit kirjautua sisään Github- ja Google-tunnuksilla</p> -->
    <div v-if="!showForgottenPasswordForm" class="login-services">
      <!-- Next div for GitHub -->
      <!-- <div @click="login('github')" class="login-service-button"> -->
        <!-- <svg-icon icon-name="github"><icon-github /></svg-icon> -->
        <!-- <span class="normal">Kirjaudu GitHub-tunnuksilla</span> -->
        <!-- <span class="mobile">GitHub-tunnukset</span> -->
      <!-- </div> -->
      <!-- TODO: uncomment this when google oauth2 is ready -->
      <!-- <div @click="login('google')" class="login-service-button">
        <svg-icon icon-name="google"><icon-google /></svg-icon>
        <span>Kirjaudu Google-tunnuksilla</span>
      </div> -->
    </div>
    <div class="login-own-credentials">
      <h4
        v-if="!showOwnCredentialLogin && !showForgottenPasswordForm"
        @click="showOwnCredentialInputs()"
      >
        Kirjaudu sisään omilla tunnuksilla
      </h4>
      <div v-if="showOwnCredentialLogin">
        <h5>Kirjaudu omilla tunnuksillasi</h5>
        <div class="login-input">
          <span>Sähköposti</span>
          <input type="text" v-model="email" />
        </div>
        <div class="login-input">
          <span>Salasana</span>
          <input type="password" v-model="password" />
        </div>
        <transition name="fade">
          <p v-if="showLocalLoginError" class="error">Väärä sähköposti tai salasana.</p>
        </transition>
        <div
          @click="login('local')"
          :class="[!$v.email.$invalid && !$v.password.$invalid ? '' : 'disabled', 'login-submit']"
        >
          <span>Kirjaudu sisään</span>
        </div>
      </div>
      <div
        class="login-forgot-password"
        @click="showResetPasswordInputs()"
        v-if="!showForgottenPasswordForm"
      >
        <span>Unohditko salasanasi?</span>
      </div>
      <div class="forgot-password-input" v-if="showForgottenPasswordForm">
        <h4>Tilaa uusi salasana</h4>
        <div class="login-input">
          <span>Sähköposti</span>
          <input type="text" v-model="resetEmail" />
        </div>
        <div
          @click="resetPassword()"
          :class="[!$v.resetEmail.$invalid ? '' : 'disabled', 'login-submit']"
        >
          <span>Tilaa uusi salasana</span>
        </div>
        <transition name="fade">
          <p v-if="showResetPasswordSuccess" class="success">Uusi salasana lähetetty.</p>
        </transition>
      </div>
    </div>
  </div>
</template>

<script>
import SvgIcon from '../icons/SvgIcon';
import IconGithub from '../icons/IconGithub';
import IconGoogle from '../icons/IconGoogle';
import router from '../../router/index';
import { required, minLength, email } from 'vuelidate/lib/validators';
// Mika 250919
import { userActions, userGetters } from '../../store/modules/user/userConsts';
import { mapUserActions, mapUserGetters } from '../../store/modules/user/userModule';
// eslint-disable-next-line
import { authenticatedUserGetters, authenticatedUserActions } from '../../store/modules/authenticatedUser/authenticatedUserConsts.js';
// eslint-disable-next-line
import { mapAuthenticatedUserGetters, mapAuthenticatedUserActions } from '../../store/modules/authenticatedUser/authenticatedUserModule.js';
// Mika 250919




export default {
  components: {
    SvgIcon,
    IconGithub,
    IconGoogle
  },
  props: {
    showResetPasswordForm: {
      type: Boolean,
      default: false
    },
    showLocalLoginError: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      baseUrl: process.env.BASE_URL,
      showOwnCredentialLogin: false,
      email: '',
      password: '',
      showForgottenPasswordForm: false,
      showResetPasswordSuccess: false,
      resetEmail: '',
      hasFailedLogin: false,
      userName: '',
      userTitle: '',
      userOrg: '',
      userRole: '',
      hasSucceeded: false,
      hasFailed: false
    };
  },
  validations: {
    email: {
      required,
      minLength: minLength(3),
      email
    },
    password: {
      required,
      minLength: minLength(6)
    },
    resetEmail: {
      required,
      minLength: minLength(3),
      email
    }
  },
  computed: {
    ...mapUserGetters({
      user: userGetters.GET_AUTHENTICATED_USER
    }),
    ...mapAuthenticatedUserGetters({
      userId: authenticatedUserGetters.GET_USER_ID,
      isAuthenticated: authenticatedUserGetters.GET_IS_AUTHENTICATED
    })
  },
  ...mapUserActions({
    getAuthenticatedUser: userActions.GET_AUTHENTICATED_USER,
    patchUser: userActions.PATCH_USER
  }),


  created() {
    if (this.showResetPasswordForm) {
      this.showResetPasswordInputs();
    }
  },
  methods: {
    login(service) {
      const loginData = service === 'local' ? this.gatherLoginData() : null;
      const data = { service, loginData };
      if (!this.$v.email.$invalid && !this.$v.password.$invalid && service === 'local') {
        this.$emit('login', data);
        this.getUserBasics();
        this.updateUser();
        // this.goToSettingsPage();
      } else {
        this.$emit('login', data);
      }
    },


    async updateUser() {
      const params = {
        userId: this.userId,
        data: {
          name: this.$sanitize(this.userName),
          title: this.$sanitize(this.userTitle),
          organization: this.$sanitize(this.userOrg),
          imageUrl: this.$sanitize(this.userImageUrl),
          role: this.$sanitize(this.userRole)
        }
      };
      await this.patchUser(params)
        .then(() => {
          this.hasSucceeded = true;
          setTimeout(() => {
            this.hasSucceeded = false;
          }, 2000);
        })
        .catch(() => {
          this.hasFailed = true;
          setTimeout(() => {
            this.hasFailed = false;
          }, 3000);
        });
      // await this.updateShowingUserData();
    },

    getUserBasics() {
      this.userName = this.user.name;
      if (this.user.title) {
        this.userTitle = this.user.title;
      }
      if (this.user.organization) {
        this.userOrg = this.user.organization;
      }
      if (this.user.role) {
        this.userRole = this.user.role;
      }
    },

    gatherLoginData() {
      return { email: this.email, password: this.password };
    },
    showOwnCredentialInputs() {
      this.showOwnCredentialLogin = true;
      this.showForgottenPasswordForm = false;
    },
    showResetPasswordInputs() {
      this.showOwnCredentialLogin = false;
      this.showForgottenPasswordForm = true;
    },
    resetPassword() {
      if (!this.$v.resetEmail.$invalid) {
        this.$emit('resetPassword', this.resetEmail);
        this.showResetPasswordSuccess = true;
      }
    },
    goToSettingsPage() {
      router.push('/settings');
    }
  },
  mounted: function() {
    document.addEventListener('keydown', e => {
      if (e.keyCode == 13) {
        if (this.showForgottenPasswordForm) {
          this.resetPassword();
        } else {
          this.login('local');
        }
      }
    });
  }
};
</script>

<style scoped>
.login-dialog {
  padding: 20px;
  overflow: none;
}

.login-services {
  margin-top: 25px;
  border-bottom: 1px solid #eeeeee;
  padding-bottom: 20px;
}

.login-service-button {
  margin: 10px 15%;
  padding: 22px 0;
  border: 2px solid #eeeeee;
  border-radius: 2px;
  font-size: 13px;
  font-weight: 600;
  position: relative;
  transition: all 0.1s;
}

.login-service-button:hover {
  border: 2px solid #a7e7e1;
  cursor: pointer;
  cursor: hand;
}

.login-service-button svg {
  position: absolute;
  left: 15px;
  top: 49%;
  transform: perspective(1px) translateY(calc(-50% - 0.5px));
  display: inline-block;
}

.login-service-button span {
  position: absolute;
  right: 20px;
  top: 50%;
  transform: perspective(1px) translateY(calc(-50% - 0.5px));
}

.login-service-button span.mobile {
  display: none;
}

.login-own-credentials {
  padding-top: 10px;
}

.login-own-credentials h4 {
  color: #06a798;
  transition: color 0.1s;
}

.login-own-credentials h4:hover {
  color: #21baac;
  cursor: pointer;
  cursor: hand;
}

.login-input {
  margin: 10px 15%;
}

.login-input span {
  display: block;
  text-align: left;
  font-weight: 600;
  font-size: 13px;
  margin-bottom: 2px;
}

.login-input input {
  width: 100%;
  padding: 10px 0;
  border: 2px solid #eeeeee;
  border-radius: 1px;
  font-weight: 600;
  font-size: 13px;
  box-sizing: border-box;
}

.login-input [type='text'],
.login-input [type='password'] {
  padding: 11px 8px;
}

.login-submit {
  margin: 18px 15% 10px;
  padding: 12px 0 11px;
  background-color: #06a798;
  border: 2px solid #06a798;
  border-radius: 1px;
  color: #ffffff;
  font-weight: 600;
  font-size: 13px;
  cursor: pointer;
  cursor: hand;
  transition: all 0.1s;
  -webkit-user-select: none; /* Safari */
  -moz-user-select: none; /* Firefox */
  -ms-user-select: none; /* IE10+/Edge */
  user-select: none; /* Standard */
}

.login-submit:hover {
  background-color: #21baac;
  border-color: #21baac;
}

.login-forgot-password {
  margin: 20px 0 10px;
}

.login-forgot-password span {
  font-weight: 600;
  color: #06a798;
  cursor: pointer;
  cursor: hand;
  transition: all 0.1s;
}

.login-forgot-password span:hover {
  color: #21baac;
}

.forgot-password-input h4,
.forgot-password-input h4:hover {
  color: initial;
}

.disabled,
.disabled:hover {
  background-color: #dddddd;
  border-color: #dddddd;
  cursor: default;
}

.error {
  color: red;
  font-size: 12px;
}

.success {
  color: #44bdb2;
  font-size: 12px;
}

@media (max-width: 750px) {
  .login-service-button {
    margin: 10px 6%;
  }

  .login-service-button span {
    left: 50px;
  }

  .login-input,
  .login-submit {
    margin: 10px 6%;
  }
}

@media (max-width: 420px) {
  .login-service-button span.normal {
    display: none;
  }
  .login-service-button span.mobile {
    display: initial;
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 10.5s;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>
