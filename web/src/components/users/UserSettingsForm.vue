<template>
  <div class="form-container">

    <!-- User text block -->
    <!-- <span> Onko käyttäjä autentikoitu: {{ isAuthenticated }} </span> -->
    <span> UserNameInitials (imports) {{ userNameInitials }} </span>
    <!-- <span> userRoleToString  (imports) {{ userRoleToString }} </span> -->
    <span> userId (imports) {{ userId }} </span>
    <span> User  (imports) {{ user }} </span>
    <!-- <span> authenticatedUserGetters  (imports) {{ authenticatedUserGetters }} </span>
    <span> mapAuthenticatedUserGetters  (imports) {{ mapAuthenticatedUserGetters }} </span> -->


    <!-- <span> Onko käyttäjä autentikoitu: {{ isAuthenticated }} </span> -->
    <h5>Muokkaa asetuksiasi</h5>
    <div class="setting-inputs">
      <div>
        <p>Nimi:</p>
        <input v-model="userName" type="text" />
      </div>
      <div>
        <p>Nimike/titteli:</p>
        <input v-model="userTitle" @input="$v.$touch()" type="text" />
      </div>
      <div>
        <p>Organisaatio:</p>
        <input v-model="userOrg" @input="$v.$touch()" type="text" />
      </div>
      <div>
        <p>Profiilikuvan url-osoite:</p>
        <input v-model="userImageUrl" @input="$v.$touch()" type="url" />
      </div>
    </div>

    <div @click.stop="submitForm" :class="[$v.$invalid ? 'disabled' : '', 'button']">
      <span class="save">
        Tallenna muutokset
      </span>
    </div>
    <transition name="fade">
      <p v-if="hasSucceeded" class="success-message">Muutokset tallennettu.</p>
      <p v-if="hasFailed" class="failure-message">Muutoksia ei saatu tallennettua.</p>
    </transition>
  </div>
</template>

<script>
import { userActions, userGetters } from '../../store/modules/user/userConsts';
import { mapUserActions, mapUserGetters } from '../../store/modules/user/userModule';
// eslint-disable-next-line
import { authenticatedUserGetters, authenticatedUserActions } from '../../store/modules/authenticatedUser/authenticatedUserConsts.js';
// eslint-disable-next-line
import { mapAuthenticatedUserGetters, mapAuthenticatedUserActions } from '../../store/modules/authenticatedUser/authenticatedUserModule.js';

import { required, minLength } from 'vuelidate/lib/validators';

export default {
  data() {
    return {
      userName: '',
      userTitle: '',
      userOrg: '',
      userImageUrl: '',
      hasSucceeded: false,
      hasFailed: false
    };
  },
  validations: {
    userName: {
      required,
      minLength: minLength(1)
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
  async created() {
    await this.getUserIdFromStorage();
    await this.getAuthenticatedUser(this.userId);
    this.userName = this.user.name;
    if (this.user.title) {
      this.userTitle = this.user.title;
    }
    if (this.user.organization) {
      this.userOrg = this.user.organization;
    }
    if (this.user.imageUrl) {
      this.userImageUrl = this.user.imageUrl;
    }
  },
  methods: {
    ...mapAuthenticatedUserActions({
      getUserIdFromStorage: authenticatedUserActions.GET_USER_ID_FROM_STORAGE
    }),
    ...mapUserActions({
      getAuthenticatedUser: userActions.GET_AUTHENTICATED_USER,
      patchUser: userActions.PATCH_USER
    }),
    async updateUser() {
      const params = {
        userId: this.userId,
        data: {
          name: this.$sanitize(this.userName),
          title: this.$sanitize(this.userTitle),
          organization: this.$sanitize(this.userOrg),
          imageUrl: this.$sanitize(this.userImageUrl)
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
      await this.updateShowingUserData();
    },
    async submitForm() {
      if (!this.$v.$invalid) {
        await this.updateUser();
      }
    },
    async updateShowingUserData() {
      await this.getAuthenticatedUser(this.userId);
    }
  },
  mounted: function() {
    document.addEventListener('keydown', e => {
      if (e.keyCode == 13) {
        this.submitForm();
      }
    });
  }
};
</script>

<style scoped>
.form-container {
  padding: 10px 0 20px;
}

h5 {
  margin: 6px 0 20px;
}

.setting-inputs div {
  margin: 6px 0 14px;
  width: 50%;
  display: inline-block;
}

.setting-inputs div p {
  height: 100%;
  margin: 0 0 2px 0;
  font-size: 13.5px;
  font-weight: 500;
}

.setting-inputs div input {
  padding: 7px 6px;
  width: 20vw;
}

.button {
  display: inline-block;
  margin: 10px 20px 0 0;
  padding: 6px 12px;
  font-weight: 600;
  font-size: 13px;
  background-color: #06a798;
  border: 3px solid #06a798;
  border-radius: 2px;
}

.button:hover {
  background-color: #44bdb2;
  border: 3px solid #44bdb2;
  cursor: pointer;
  cursor: hand;
}

.button .save {
  color: #ffffff;
  transition: background-color, 0.1s;
  transition: border, 0.1s;
}

.disabled,
.disabled:hover {
  background-color: #dddddd;
  border: none;
  -webkit-user-select: none; /* Safari */
  -moz-user-select: none; /* Firefox */
  -ms-user-select: none; /* IE10+/Edge */
  user-select: none; /* Standard */
  cursor: default;
}

.success-message,
.failure-message {
  color: #44bdb2;
  display: inline-block;
  margin: 10px 0 0;
}

.failure-message {
  color: red;
}

@media (max-width: 700px) {
  .setting-inputs div {
    margin: 6px 0 14px;
    width: 100%;
    display: block;
  }

  .setting-inputs div input {
    padding: 7px 6px;
    width: 42vw;
  }
}

@media (max-width: 500px) {
  .setting-inputs div input {
    width: 50vw;
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>
