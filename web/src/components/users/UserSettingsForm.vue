<template>
  <div class="form-container">
    <h5>Muokkaa asetuksiasi</h5>
    <div class="setting-inputs">
      <!-- TODO: Finish patching functionality (store + api) -->
      <!-- TODO: Then remove disabled input states  -->
      <div>
        <p>Nimi:</p>
        <input disabled :value="$v.userName.$model" type="text">
      </div>
      <div>
        <p>Nimike/titteli: {{ userTitle }}</p>
        <input disabled v-model.trim.lazy="$v.userTitle" @input="$v.$touch()" type="text">
      </div>
      <div>
        <p>Organisaatio: {{ userOrg }}</p>
        <input disabled v-model.trim.lazy="$v.userOrg" @input="$v.$touch()" type="text">
      </div>
      <div>
        <p>Profiilikuvan url-osoite: {{ userImageUrl }}</p>
        <input disabled v-model.trim.lazy="$v.userImageUrl" @input="$v.$touch()" type="url">
      </div>
    </div>

    <!--<div @click.stop="submitForm" :class="[$v.$invalid ? '' : 'disabled', 'button']">
      <span class="save">
        Tallenna muutokset
      </span>
    </div>-->
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
      userTitle: '',
      userOrg: '',
      userImageUrl: ''
    };
  },
  validations: {
    userName: {
      required,
      minLength: minLength(1)
    }
  },
  computed: {
    ...mapAuthenticatedUserGetters({
      userId: authenticatedUserGetters.GET_USER_ID,
      isAuthenticated: authenticatedUserGetters.GET_IS_AUTHENTICATED,
      userName: authenticatedUserGetters.GET_USER_NAME
    }),
    ...mapUserGetters({
      user: userGetters.GET_USER
    })
  },
  async created() {
    this.getUserIdFromStorage();
    await this.getUser(this.userId);
  },
  methods: {
    ...mapAuthenticatedUserActions({
      getUserIdFromStorage: authenticatedUserActions.GET_USER_ID_FROM_STORAGE,
      getUserName: authenticatedUserActions.GET_USER_NAME
    }),
    ...mapUserActions({
      getUser: userActions.GET_USER,
      patchUser: userActions.PATCH_USER
    }),
    async updateUser() {
      const params = {
        name: this.$sanitize(this.userName),
        title: this.$sanitize(this.userTitle),
        organization: this.$sanitize(this.userOrg),
        imageUrl: this.$sanitize(this.userImageUrl)
      };
      await this.patchUser(this.userId, params);
    },
    submitForm() {
      if (!this.$v.$invalid) {
        this.updateUser();
      }
    }
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
  margin: 10px 0 0;
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
</style>
