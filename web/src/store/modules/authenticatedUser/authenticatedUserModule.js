import Vue from 'vue';
import { mapGetters, mapActions } from 'vuex';
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

Vue.use(VueCookies);

export const mapAuthenticatedUserGetters = getters => mapGetters(namespace, getters);
export const mapAuthenticatedUserActions = actions => mapActions(namespace, actions);

export default {
  namespaced: true,
  state: {
    [storeStateNames.IS_AUTHENTICATED]: false,
    [storeStateNames.USER_ID]: 0,
    [storeStateNames.NAME]: '',
    [storeStateNames.ERROR]: '',
    [storeStateNames.ROLE]: ''
  },
  getters: {
    [authenticatedUserGetters.GET_IS_AUTHENTICATED]: state =>
      state[storeStateNames.IS_AUTHENTICATED],
    [authenticatedUserGetters.GET_USER_ID]: state => state[storeStateNames.USER_ID],
    [authenticatedUserGetters.GET_USER_NAME]: state => state[storeStateNames.NAME],
    [authenticatedUserGetters.GET_AUTHENTICATE_ERROR]: state => state[storeStateNames.ERROR],
    [authenticatedUserGetters.GET_USER_ROLE]: state => state[storeStateNames.ROLE]
  },
  mutations: {
    [authenticatedUserMutations.SET_AUTHENTICATION](state, authenticatedData) {
      Vue.set(state, storeStateNames.IS_AUTHENTICATED, authenticatedData.authenticated);
      Vue.set(state, storeStateNames.ROLE, authenticatedData.role);
      Vue.set(state, storeStateNames.USER_ID, authenticatedData.user_id);
      Vue.set(sessionStorage, storeKeyNames.USER_ID, authenticatedData.user_id);
    },
    [authenticatedUserMutations.SET_USER_ID](state, userId) {
      Vue.set(state, storeStateNames.USER_ID, userId);
    },
    [authenticatedUserMutations.SET_USER_NAME](state, name) {
      Vue.set(state, storeStateNames.NAME, name);
    }
  },
  actions: {
    async [authenticatedUserActions.AUTHENTICATE]({ commit }, payload) {
      const response = await api.authenticate.authenticateGitHubUser(payload.code);
      if (response && response.code === 200) {
        commit(authenticatedUserMutations.SET_AUTHENTICATION, {
          authenticated: true,
          user_id: response.user_id
        });
        // eslint-disable-next-line no-undef
        $cookies.set(storeKeyNames.ACCESS_TOKEN, response.access_token);
        // eslint-disable-next-line no-undef
        $cookies.set(storeKeyNames.REFRESH_TOKEN, response.refresh_token);
      } else {
        commit(authenticatedUserMutations.SET_AUTHENTICATE_ERROR, response.error);
      }
    },
    async [authenticatedUserActions.VALIDATE_AUTHENTICATION]({ commit, dispatch }) {
      // eslint-disable-next-line no-undef
      const access_token = $cookies.get(storeKeyNames.ACCESS_TOKEN);
      // eslint-disable-next-line no-unused-vars
      const userId =
        this.state.user[storeStateNames.USER_ID] || sessionStorage.getItem(storeKeyNames.USER_ID);
      //TODO: needs to validate token from backend and also check that token has correct userid
      if (access_token && access_token.length > 0 && parseInt(userId) > 0) {
        const response = await api.user.getUser(userId);
        if (response && response.code === 200) {
          commit(authenticatedUserMutations.SET_AUTHENTICATION, {
            authenticated: true,
            user_id: userId,
            role: response.data.role
          });
        } else {
          dispatch(authenticatedUserActions.REVOKE_AUTHENTICATION);
        }
      } else {
        dispatch(authenticatedUserActions.REVOKE_AUTHENTICATION);
      }
    },
    async [authenticatedUserActions.REVOKE_AUTHENTICATION]({ commit }) {
      // eslint-disable-next-line no-undef
      $cookies.remove(storeKeyNames.ACCESS_TOKEN);
      // eslint-disable-next-line no-undef
      $cookies.remove(storeKeyNames.REFRESH_TOKEN);
      commit(authenticatedUserMutations.SET_AUTHENTICATION, {
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
        commit(authenticatedUserMutations.SET_AUTHENTICATION, {
          authenticated: true,
          user_id: response.user_id
        });

        // eslint-disable-next-line no-undef
        $cookies.set(storeKeyNames.ACCESS_TOKEN, response.access_token);
        // eslint-disable-next-line no-undef
        $cookies.set(storeKeyNames.REFRESH_TOKEN, response.refresh_token);
      } else {
        commit(authenticatedUserMutations.SET_AUTHENTICATION, false);
      }
    },
    [authenticatedUserActions.GET_USER_ID_FROM_STORAGE]({ commit }) {
      const userId = sessionStorage.getItem(storeKeyNames.USER_ID);
      if (userId && userId > 0) {
        commit(authenticatedUserMutations.SET_USER_ID, userId);
      }
    },
    async [authenticatedUserActions.REFRESH_AUTHORIZATION_TOKEN]({ dispatch }, payload) {
      const response = await api.authenticate.refreshAuthenticationToken(payload);
      if (response && response.code === 200) {
        // eslint-disable-next-line no-undef
        $cookies.set(storeKeyNames.ACCESS_TOKEN, response.access_token);
      } else {
        dispatch(authenticatedUserActions.REVOKE_AUTHENTICATION);
      }
    }
  }
};
