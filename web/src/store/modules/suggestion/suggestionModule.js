import Vue from 'vue';
import { mapActions, mapGetters, mapMutations } from 'vuex';
import api from '../../../api';
import {
  namespace,
  storeStateNames,
  suggestionMutations,
  suggestionGetters,
  suggestionActions
} from './suggestionConsts';

export const mapSuggestionGetters = getters => mapGetters(namespace, getters);
export const mapSuggestionActions = actions => mapActions(namespace, actions);
export const mapSuggestionMutations = mutations => mapMutations(namespace, mutations);

export default {
  namespaced: true,
  state: {
    [storeStateNames.ITEMS]: [],
    [storeStateNames.OPEN_COUNT]: 0,
    [storeStateNames.RESOLVED_COUNT]: 0,
    [storeStateNames.FILTERS]: []
  },
  getters: {
    [suggestionGetters.GET_SUGGESTIONS]: state => state[storeStateNames.ITEMS],
    [suggestionGetters.GET_OPEN_SUGGESTIONS_COUNT]: state => state[storeStateNames.OPEN_COUNT],
    [suggestionGetters.GET_RESOLVED_SUGGESTIONS_COUNT]: state =>
      state[storeStateNames.RESOLVED_COUNT],
    [suggestionGetters.GET_FILTERS]: state => state[storeStateNames.FILTERS]
  },
  mutations: {
    [suggestionMutations.SET_SUGGESTIONS](state, suggestions) {
      Vue.set(state, storeStateNames.ITEMS, suggestions);
    },
    [suggestionMutations.SET_OPEN_SUGGESTIONS_COUNT](state, count) {
      Vue.set(state, storeStateNames.OPEN_COUNT, count);
    },
    [suggestionMutations.SET_RESOLVED_SUGGESTIONS_COUNT](state, count) {
      Vue.set(state, storeStateNames.RESOLVED_COUNT, count);
    },
    [suggestionMutations.SET_FILTERS](state, filters) {
      Vue.set(state, storeStateNames.FILTERS, filters);
    }
  },
  actions: {
    async [suggestionActions.GET_SUGGESTIONS]({ commit }) {
      const result = await api.suggestions.getSuggestions();
      commit(suggestionMutations.SET_SUGGESTIONS, result.data);
    },
    async [suggestionActions.GET_OPEN_SUGGESTIONS]({ commit }) {
      const result = await api.suggestions.getOpenSuggestions();
      commit(suggestionMutations.SET_OPEN_SUGGESTIONS_COUNT, result.items);
    },
    async [suggestionActions.GET_RESOLVED_SUGGESTIONS]({ commit }) {
      const result = await api.suggestions.getResolvedSuggestions();
      commit(suggestionMutations.SET_RESOLVED_SUGGESTIONS_COUNT, result.items);
    },
    async [suggestionActions.GET_SORTED_SUGGESTIONS]({ commit }, sortValue) {
      const result = await api.suggestions.getSortedSuggestions(sortValue);
      commit(suggestionMutations.SET_SUGGESTIONS, result.data);
    },
    async [suggestionActions.GET_FILTERED_SUGGESTIONS]({ commit }, filters) {
      const result = await api.suggestions.filterSuggestions(filters);
      commit(suggestionMutations.SET_SUGGESTIONS, result.data);
    },
    async [suggestionActions.GET_SUGGESTION_BY_ID]({ commit }, suggestionId) {
      const result = await api.suggestions.getSuggestionById(suggestionId);
      commit(suggestionMutations.SET_SUGGESTIONS, [result.data]);
    }
  }
};
