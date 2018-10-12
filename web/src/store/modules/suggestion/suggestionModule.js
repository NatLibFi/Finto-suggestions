import Vue from 'vue';
import { mapActions, mapGetters } from 'vuex';
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

export default {
  namespaced: true,
  state: {
    items: [],
    openCount: 0,
    resolvedCount: 0
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
    [suggestionMutations.SET_SEARCH_QUERY](state, searchQuery) {
      Vue.set(state, storeStateNames.SEARCH_QUERY, searchQuery);
    }
  },
  getters: {
    [suggestionGetters.GET_SUGGESTIONS]: state => state[storeStateNames.ITEMS],
    [suggestionGetters.GET_OPEN_SUGGESTIONS_COUNT]: state => state[storeStateNames.OPEN_COUNT],
    [suggestionGetters.GET_RESOLVED_SUGGESTIONS_COUNT]: state =>
      state[storeStateNames.RESOLVED_COUNT],
    [suggestionGetters.GET_SEARCH_QUERY]: state => state[storeStateNames.SEARCH_QUERY]
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
    async [suggestionActions.GET_SEARCHED_SUGGESTIONS]({ commit }, searchQuery) {
      const result = await api.suggestions.searchSuggestions(searchQuery);
      commit(suggestionMutations.SET_SUGGESTIONS, result.data);
    },
    [suggestionActions.SET_SEARCH_QUERY]({ commit }, searchQuery) {
      commit(suggestionMutations.SET_SEARCH_QUERY, searchQuery);
    }
  }
};
