import Vue from 'vue';
import { mapGetters, mapActions } from 'vuex';
import VueAxios from 'vue-axios';
import VueAuthenticate from 'vue-authenticate';
import axios from 'axios';

import { namespace, storeStateNames, authGetters, authMutations, authActions } from './authConsts';

Vue.use(VueAxios, axios);

const vueAuth = VueAuthenticate.factory(Vue.prototype.$http, {
  baseUrl: process.env.VUE_APP_APPURL,
  providers: {
    github: {
      clientId: `${process.env.VUE_APP_GITHUB_CLIENT_ID}`,
      redirectUri: `${process.env.VUE_APP_APPURL}/api/auth`
    },
    google: {
      clientId: '',
      redirectUri: `${process.env.VUE_APP_APPURL}/api/auth`
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
    [authGetters.GET_IS_USER_AUTHENTICATED]: state => state[storeStateNames.IS_AUTHENTICATED]
  },
  mutations: {
    [authMutations.SET_USER_AUTHENTICATED](state, payload) {
      Vue.set(state, storeStateNames.IS_AUTHENTICATED, payload.isAuthenticated);
    }
  },
  actions: {
    async [authActions.AUTHENTICATE]({ commit }, payload) {
      vueAuth
        .authenticate(payload.providerName)
        .then(response => {
          console.log(response);
          commit(authMutations.SET_USER_AUTHENTICATED, {
            isAuthenticated: vueAuth.isAuthenticated()
          });
        })
        .catch(err => {
          console.log(err);
        });
    }
  }
};
