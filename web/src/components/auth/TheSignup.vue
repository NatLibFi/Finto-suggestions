<template>
  <!-- Using 'login' as a catch-all term for signups and logins -->
  <div class="login-dialog">
    <h3>Luo tunnus</h3>
    <p>Voit luoda tilin Github- ja Google-tunnuksilla</p>
    <div class="login-services">
      <div @click="signup('github')" class="login-service-button">
        <svg-icon icon-name="github"><icon-github /></svg-icon>
        <span>Luo tili GitHub-tunnuksilla</span>
      </div>
      <!-- TODO: enable this when google login/signup works -->
      <!-- <div @click="signup('google')" class="login-service-button">
        <svg-icon icon-name="google"><icon-google /></svg-icon>
        <span>Luo tili Google-tunnuksilla</span>
      </div> -->
    </div>
    <div class="login-own-credentials">
      <h4
        v-if="!showOwnCredentialSignup"
        @click="showOwnCredentialSignup = !showOwnCredentialSignup"
      >
        Luo tili omilla tunnuksilla
      </h4>
      <div v-if="showOwnCredentialSignup" class="login-inputs">
        <div class="login-input">
          <span>Nimi</span>
          <input type="text" v-model="name" />
        </div>
        <div class="login-input">
          <span>Sähköposti</span>
          <input type="text" v-model="email" />
        </div>
        <div class="login-input">
          <span>Salasana</span>
          <input type="password" v-model="password" />
          <span>Syötä salasana toisen kerran</span>
          <input type="password" v-model="password2" />
          <p class="hint">Salasanan tulee olla 6 merkkiä tai pitempi.</p>
        </div>
        <div
          v-if="password === password2"
          @click="signup('local')"
          :class="[!$v.$invalid ? '' : 'disabled', 'login-submit']"
        >
          <!-- <div @click="signup('local')" :class="[!$v.$invalid ? '' :
            'disabled', 'login-submit']"> -->
          <span>Luo tili</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SvgIcon from '../icons/SvgIcon';
import IconGithub from '../icons/IconGithub';
import IconGoogle from '../icons/IconGoogle';

import { required, minLength, email } from 'vuelidate/lib/validators';

export default {
  components: {
    SvgIcon,
    IconGithub,
    IconGoogle
  },
  data: () => ({
    showOwnCredentialSignup: false,
    name: '',
    email: '',
    password: '',
    password2: ''
  }),
  validations: {
    name: {
      required
    },
    email: {
      required,
      minLength: minLength(3),
      email
    },
    password: {
      required,
      minLength: minLength(5)
    }
  },
  methods: {
    gatherLocalSignupData() {
      return { name: this.name, email: this.email, password: this.password };
    },
    signup(service) {
      const userdata = service === 'local' ? this.gatherLocalSignupData() : null;
      let data = { service, userdata };
      if (service === 'local') {
        if (!this.$v.$invalid) {
          this.$emit('signup', data);
        }
      } else {
        this.$emit('signup', data);
      }
    }
  },
  mounted: function() {
    document.addEventListener('keydown', e => {
      if (e.keyCode == 13 && this.showOwnCredentialSignup) {
        this.signup('local');
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
  left: 20px;
  top: 50%;
  transform: perspective(1px) translateY(calc(-50% - 0.5px));
  display: inline-block;
}

.login-service-button span {
  position: absolute;
  right: 22px;
  top: 50%;
  transform: perspective(1px) translateY(calc(-50% - 0.5px));
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

.disabled,
.disabled:hover {
  background-color: #dddddd;
  border-color: #dddddd;
  cursor: default;
}

.hint {
  color: #444444;
  font-size: 12px;
  margin-top: 5px;
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
</style>
