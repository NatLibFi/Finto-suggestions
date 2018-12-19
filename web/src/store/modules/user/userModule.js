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
  userGetters,
  userActions,
  userMutations
} from './userConsts';

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

export const mapUserGetters = getters => mapGetters(namespace, getters);
export const mapUserActions = actions => mapActions(namespace, actions);

export default {
  namespaced: true,
  state: {
    [storeStateNames.IS_AUTHENTICATED]: false,
    [storeStateNames.USER_ID]: 0,
    [storeStateNames.NAME]: ''
    [storeStateNames.USER]: ''
  },
  getters: {
    [userGetters.GET_AUTHENTICATE]: state => state[storeStateNames.IS_AUTHENTICATED],
    [userGetters.GET_USER_ID]: state => state[storeStateNames.USER_ID],
    [userGetters.GET_USER_NAME]: state => state[storeStateNames.NAME]
    [userGetters.GET_USER]: state => state[storeStateNames.USER],
    [userGetters.GET_USERS]: state => state[storeStateNames.USERS],
  },
  mutations: {
    [userMutations.SET_AUTHENTICATE](state, authenticate) {
      Vue.set(state, storeStateNames.IS_AUTHENTICATED, authenticate);
    },
    [userMutations.SET_USER_ID](state, userId) {
      Vue.set(state, storeStateNames.USER_ID, userId);
    },
    [userMutations.SET_STORAGE_USER_ID](user) {
      sessionStorage.setItem(storeKeyNames.USER_ID, user.userId);
    },
    [userMutations.SET_USER_NAME](state, name) {
      console.log(name);
      Vue.set(state, storeStateNames.NAME, name);
    }
    [userMutations.SET_USER](state, user) {
      Vue.set(state, storeStateNames.USER, user);
    },
    [userMutations.SET_USERS](state, user) {
        Vue.set(state, storeStateNames.USERS, user);
    },
  },
  actions: {
    async [userActions.AUTHENTICATE]({ commit }, payload) {
      await vueAuth
        .authenticate(payload.providerName)
        .then(response => {
          commit(userMutations.SET_AUTHENTICATE, true);
          commit(userMutations.SET_USER_ID, response.data.user_id);
          commit(userMutations.SET_STORAGE_USER_ID, response.data.user_id);
        })
        .catch(err => {
          console.log(err);
          commit(userMutations.SET_AUTHENTICATE, false);
        });
    },
    [userActions.VALIDATE_AUTHENTICATION]({ commit, dispatch }) {
      // eslint-disable-next-line no-undef
      const token = $cookies.get(storeKeyNames.ACCESS_TOKEN);
      // eslint-disable-next-line no-unused-vars
      const userId =
        this.state.user[storeStateNames.USER_ID] || sessionStorage.getItem(storeKeyNames.USER_ID);
      //TODO: needs to validate token from backend and also check that token has correct userid
      if (token && token.length > 0 && parseInt(userId) > 0) {
        commit(userMutations.SET_AUTHENTICATE, true);
      } else {
        dispatch(userActions.REVOKE_AUTHENTICATION);
      }
    },
    async [userActions.REVOKE_AUTHENTICATION]({ commit }) {
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
      commit(userMutations.SET_AUTHENTICATE, false);
      commit(userMutations.SET_USER_ID, 0);
      commit(userMutations.SET_STORAGE_USER_ID, 0);
    },
    async [userActions.GET_USER_NAME]({ commit }, userId) {
      const response = await api.user.getUserData(userId);
      if (response && response.code === 200) {
        console.log(response.data);
        commit(userMutations.SET_USER_NAME, response.data.name);
        commit(userMutations.SET_USER, response.data);
      }
    },
    async [userActions.GET_USERS]({ commit }) {
      const response = await api.user.getUsers();
      if (response && response.code === 200) {
        commit(userMutations.SET_USERS, response.data);
      }
    },
    async [userActions.AUTHENTICATE_LOCAL_USER]({ commit }, authenticateData) {
      const response = await api.user.authenticateLocalUser(authenticateData);

      if (response && response.code === 200) {
        commit(userMutations.SET_AUTHENTICATE, true);
        commit(userMutations.SET_USER_ID, response.user_id);
        commit(userMutations.SET_STORAGE_USER_ID, response.user_id);

        // eslint-disable-next-line no-undef
        $cookies.set(storeKeyNames.ACCESS_TOKEN, response.access_token);
        // eslint-disable-next-line no-undef
        $cookies.set(storeKeyNames.REFRESH_TOKEN, response.refresh_token);
      } else {
        commit(userMutations.SET_AUTHENTICATE, false);
      }
    },
    [userActions.GET_USER_ID_FROM_STORAGE]({ commit }) {
      const userId = sessionStorage.getItem(storeKeyNames.USER_ID);
      if (userId && userId > 0) {
        commit(userMutations.SET_USER_ID, userId);
      }
    }
  }
};
