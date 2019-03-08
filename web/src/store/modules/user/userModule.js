import Vue from 'vue';
import { mapGetters, mapActions, mapMutations } from 'vuex';

import { namespace, storeStateNames, userGetters, userActions, userMutations } from './userConsts';

import api from '../../../api';

export const mapUserGetters = getters => mapGetters(namespace, getters);
export const mapUserActions = actions => mapActions(namespace, actions);
export const mapUserMutations = mutations => mapMutations(namespace, mutations);

export default {
  namespaced: true,
  state: {
    [storeStateNames.USER]: '',
    [storeStateNames.USERS]: []
  },
  getters: {
    [userGetters.GET_USER]: state => state[storeStateNames.USER],
    [userGetters.GET_USERS]: state => state[storeStateNames.USERS]
  },
  mutations: {
    [userMutations.SET_USER](state, user) {
      Vue.set(state, storeStateNames.USER, user);
    },
    [userMutations.SET_USERS](state, users) {
      Vue.set(state, storeStateNames.USERS, users);
    }
  },
  actions: {
    async [userActions.GET_USER]({ commit }, userId) {
      const response = await api.user.getUser(userId);
      if (response && response.code === 200) {
        commit(userMutations.SET_USER, response.data);
      }
    },
    async [userActions.GET_USERS]({ commit }) {
      const response = await api.user.getUsers();
      if (response && response.code === 200) {
        commit(userMutations.SET_USERS, response.data);
      }
    },
    async [userActions.PATCH_USER]({ commit }, params) {
      const response = await api.user.patchUser(params.userId, params.data);
      if (response && response.code === 200) {
        await commit(userMutations.SET_USER, response.data);
      } else {
        throw 'Error in patching user information.';
      }
    },
    // eslint-disable-next-line no-empty-pattern
    async [userActions.RESET_PASSWORD]({}, email) {
      const response = await api.user.resetPassword(email);
      if (response && response.code === 201) {
        return;
      } else {
        throw `Could not reset user password that email is ${email}`;
      }
    }
  }
};
