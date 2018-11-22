import Vue from 'vue';
import { mapGetters, mapActions } from 'vuex';
import VueAxios from 'vue-axios';
import VueAuthenticate from 'vue-authenticate';
import axios from 'axios';

import { namespace, storeStateNames, authGetters, authActions } from './authConsts';

Vue.use(VueAxios, axios);

const vueAuth = VueAuthenticate.factory(Vue.prototype.$http, {
  baseUrl: 'http://localhost:8080/api',
  state: '0',
  providers: {
    github: {
      clientId: `${process.env.VUE_APP_GITHUB_CLIENT_ID}`,
      redirectUri: `http://localhost:8080/api/auth/github`,
      state: '0',
      optionalUrlParams: ['scope', 'state']
    },
    google: {
      clientId: '',
      redirectUri: `${process.env.VUE_APP_APPURL}/api/auth/google`
    }
  }
});

export const mapAuthGetters = getters => mapGetters(namespace, getters);
export const mapAuthActions = actions => mapActions(namespace, actions);

export default {
  namespaced: true,
  state: {
    [storeStateNames.IS_AUTHENTICATED]: false
  },
  getters: {
    [authGetters.GET_IS_USER_AUTHENTICATED]: () => {
      const token = localStorage.getItem('vue-authenticate.vueauth_token');
      return token && token.length > 0 ? true : false;
    }
  },
  mutations: {},
  actions: {
    async [authActions.AUTHENTICATE]({ commit }, payload) {
      await vueAuth.authenticate(payload.providerName);
    }
  }
};
