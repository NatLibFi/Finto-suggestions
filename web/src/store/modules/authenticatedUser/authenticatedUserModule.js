import Vue from 'vue';
import { mapGetters, mapActions } from 'vuex';
import VueAxios from 'vue-axios';
import VueAuthenticate from 'vue-authenticate';
import axios from 'axios';
import addDays from 'date-fns/add_days';
import VueCookies from 'vue-cookies';

import {
  namespace,
  storeStateNames,
  storeKeyNames,
  authenticatedUserGetters,
  authenticatedUserActions,
  authenticatedUserMutations
} from './authenticatedUserConsts';

import api from '../../../api';

Vue.use(VueAxios, axios);
Vue.use(VueCookies);

const vueAuth = VueAuthenticate.factory(Vue.prototype.$http, {
  baseUrl: `${process.env.VUE_APP_BASE_DOMAIN}/api`,
  storageType: 'cookieStorage',
  cookieStorage: {
    expires: addDays(new Date(), 14),
    secure: process.env.NODE_ENV === 'production' ? true : false
  },
  providers: {
    github: {
      clientId: `${process.env.VUE_APP_GITHUB_CLIENT_ID}`,
      redirectUri: `${process.env.VUE_APP_BASE_DOMAIN}/api/auth/github`,
      state: '0',
      optionalUrlParams: ['scope', 'state'],
      popupOptions: null
    },
    google: {
      clientId: '',
      redirectUri: `${process.env.VUE_APP_BASE_DOMAIN}/api/auth/google`
    }
  }
});

export const mapAuthenticatedUserGetters = getters => mapGetters(namespace, getters);
export const mapAuthenticatedUserActions = actions => mapActions(namespace, actions);

export default {
  namespaced: true,
  state: {
    [storeStateNames.IS_AUTHENTICATED]: false,
    [storeStateNames.USER_ID]: 0,
    [storeStateNames.NAME]: ''
  },
  getters: {
    [authenticatedUserGetters.GET_AUTHENTICATE]: state => state[storeStateNames.IS_AUTHENTICATED],
    [authenticatedUserGetters.GET_USER_ID]: state => state[storeStateNames.USER_ID],
    [authenticatedUserGetters.GET_USER_NAME]: state => state[storeStateNames.NAME]
  },
  mutations: {
    [authenticatedUserMutations.SET_AUTHENTICATE](state, authenticatedData) {
      Vue.set(state, storeStateNames.IS_AUTHENTICATED, authenticatedData.authenticated);
      Vue.set(state, storeStateNames.USER_ID, authenticatedData.user_id);
      Vue.set(sessionStorage, storeKeyNames.USER_ID, authenticatedData.user_id);
    },
    [authenticatedUserMutations.SET_USER_NAME](state, name) {
      Vue.set(state, storeStateNames.NAME, name);
    }
  },
  actions: {
    async [authenticatedUserActions.AUTHENTICATE]({ commit }, payload) {
      await vueAuth
        .authenticate(payload.providerName)
        .then(response => {
          if (response && response.status === 200) {
            commit(authenticatedUserMutations.SET_AUTHENTICATE, {
              authenticated: true,
              user_id: response.data.user_id
            });
          } else {
            commit(authenticatedUserMutations.SET_AUTHENTICATE, {
              authenticated: false,
              user_id: 0
            });
          }
        })
        .catch(err => {
          console.log(err);
          commit(authenticatedUserMutations.SET_AUTHENTICATE, false);
        });
    },
    [authenticatedUserActions.VALIDATE_AUTHENTICATION]({ commit, dispatch }) {
      // eslint-disable-next-line no-undef
      const token = $cookies.get(storeKeyNames.ACCESS_TOKEN);
      // eslint-disable-next-line no-unused-vars
      const userId =
        this.state.user[storeStateNames.USER_ID] || sessionStorage.getItem(storeKeyNames.USER_ID);
      //TODO: needs to validate token from backend and also check that token has correct userid
      if (token && token.length > 0 && parseInt(userId) > 0) {
        commit(authenticatedUserMutations.SET_AUTHENTICATE, {
          authenticated: true,
          user_id: userId
        });
      } else {
        dispatch(authenticatedUserActions.REVOKE_AUTHENTICATION);
      }
    },
    async [authenticatedUserActions.REVOKE_AUTHENTICATION]({ commit }) {
      // eslint-disable-next-line no-undef
      const token = $cookies.get(storeKeyNames.ACCESS_TOKEN);
      const userId =
        this.state.user[storeStateNames.USER_ID] || sessionStorage.getItem(storeKeyNames.USER_ID);

      if (token && token.length > 0 && parseInt(userId) > 0) {
        const payload = { user_id: userId };
        try {
          await api.user.revokeAuthentication(payload);
        } catch (err) {
          console.log(err);
        }
      }

      // eslint-disable-next-line no-undef
      $cookies.remove(storeKeyNames.ACCESS_TOKEN);
      // eslint-disable-next-line no-undef
      $cookies.remove(storeKeyNames.REFRESH_TOKEN);
      commit(authenticatedUserMutations.SET_AUTHENTICATE, {
        authenticated: false,
        user_id: 0
      });
    },
    async [authenticatedUserActions.GET_USER_NAME]({ commit }, userId) {
      const response = await api.user.getUser(userId);
      if (response && response.code === 200) {
        commit(authenticatedUserMutations.SET_USER_NAME, response.data.name);
      }
    },
    async [authenticatedUserActions.AUTHENTICATE_LOCAL_USER]({ commit }, authenticateData) {
      const response = await api.user.authenticateLocalUser(authenticateData);

      if (response && response.code === 200) {
        commit(authenticatedUserMutations.SET_AUTHENTICATE, {
          authenticated: true,
          user_id: response.data.user_id
        });

        // eslint-disable-next-line no-undef
        $cookies.set(storeKeyNames.ACCESS_TOKEN, response.access_token);
        // eslint-disable-next-line no-undef
        $cookies.set(storeKeyNames.REFRESH_TOKEN, response.refresh_token);
      } else {
        commit(authenticatedUserMutations.SET_AUTHENTICATE, false);
      }
    },
    [authenticatedUserActions.GET_USER_ID_FROM_STORAGE]({ commit }) {
      const userId = sessionStorage.getItem(storeKeyNames.USER_ID);
      if (userId && userId > 0) {
        commit(authenticatedUserMutations.SET_USER_ID, userId);
      }
    }
  }
};
