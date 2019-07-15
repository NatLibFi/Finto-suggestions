import Vue from 'vue';
import { mapActions, mapGetters } from 'vuex';
import api from '../../../api';
import { namespace, storeStateNames, tagMutations, tagGetters, tagActions } from './tagConst';
import {
  namespace as suggestionNamespace,
  suggestionActions
} from '../suggestion/suggestionConsts';
import { namespace as eventNamespace, eventActions } from '../event/eventConsts';

export const mapTagGetters = getters => mapGetters(namespace, getters);
export const mapTagActions = actions => mapActions(namespace, actions);

export default {
  namespaced: true,
  state: {
    [storeStateNames.ITEMS]: []
  },
  getters: {
    [tagGetters.GET_TAGS]: state => state[storeStateNames.ITEMS]
  },
  mutations: {
    [tagMutations.SET_TAGS](state, tags) {
      Vue.set(state, storeStateNames.ITEMS, tags);
    }
  },
  actions: {
    async [tagActions.GET_TAGS]({ commit }) {
      const result = await api.tag.getTags();
      if (result && result.code == 200) {
        commit(tagMutations.SET_TAGS, result.data);
      }
    },
    async [tagActions.DELETE_TAG]({ dispatch }, params) {
      await api.tag.deleteTag(params.tagLabel);
      dispatch(tagActions.GET_TAGS);
    },
    async [tagActions.ADD_TAG_TO_SUGGESTION]({ dispatch }, params) {
      const response = await api.suggestion.addTagToSuggestion(
        params.suggestionId,
        params.tagLabel
      );
      if (response && response.code === 201) {
        dispatch(
          `${eventNamespace}/${eventActions.ADD_NEW_EVENT}`,
          {
            event: params.event,
            suggestionId: params.suggestionId
          },
          {
            root: true
          }
        );
        dispatch(
          `${suggestionNamespace}/${suggestionActions.GET_SUGGESTION_BY_ID}`,
          params.suggestionId,
          {
            root: true
          }
        );
      }
    },
    async [tagActions.REMOVE_TAG_FROM_SUGGESTION]({ dispatch }, params) {
      const response = await api.suggestion.removeTagFromSuggestion(
        params.suggestionId,
        params.tagLabel
      );
      if (response && response.code === 202) {
        dispatch(
          `${eventNamespace}/${eventActions.ADD_NEW_EVENT}`,
          {
            event: params.event,
            suggestionId: params.suggestionId
          },
          {
            root: true
          }
        );
        dispatch(
          `${suggestionNamespace}/${suggestionActions.GET_SUGGESTION_BY_ID}`,
          params.suggestionId,
          {
            root: true
          }
        );
      }
    }
  }
};
