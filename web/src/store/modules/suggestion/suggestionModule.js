import Vue from 'vue';
import { mapActions, mapGetters, mapMutations } from 'vuex';
import api from '../../../api';
import {
  namespace,
  storeStateNames,
  sessionStorageKeyNames,
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
    [suggestionGetters.GET_SEARCH_QUERY]: state => state[storeStateNames.SEARCH_QUERY],
    [suggestionGetters.GET_FILTERS]: state => state[storeStateNames.FILTERS],
    [suggestionGetters.GET_PAGINATION_SUGGESTIONS]: state => state[storeStateNames.PAGINATED_ITEMS],
    [suggestionGetters.GET_SELECTED_SORT]: state => state[storeStateNames.SELECTED_SORT]
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
    },
    [suggestionMutations.SET_FILTERS](state, filters) {
      Vue.set(state, storeStateNames.FILTERS, filters);
    },
    [suggestionMutations.SET_PAGINATION_SUGGESTIONS](state, suggestions) {
      Vue.set(state, storeStateNames.PAGINATED_ITEMS, suggestions);
    },
    [suggestionMutations.SET_SELECTED_SORT](state, sortkey) {
      Vue.set(state, storeStateNames.SELECTED_SORT, sortkey);
    }
  },
  actions: {
    async [suggestionActions.GET_SUGGESTIONS]({ commit }) {
      const result = await api.suggestion.getSuggestions();
      if (result && result.code == 200) {
        commit(suggestionMutations.SET_SUGGESTIONS, result.data);
      }
    },
    async [suggestionActions.GET_OPEN_SUGGESTIONS]({ commit }) {
      const result = await api.suggestion.getOpenSuggestions();
      if (result && result.code == 200) {
        commit(suggestionMutations.SET_OPEN_SUGGESTIONS_COUNT, result.items);
      }
    },
    async [suggestionActions.GET_RESOLVED_SUGGESTIONS]({ commit }) {
      const result = await api.suggestion.getResolvedSuggestions();
      if (result && result.code == 200) {
        commit(suggestionMutations.SET_RESOLVED_SUGGESTIONS_COUNT, result.items);
      }
    },
    async [suggestionActions.GET_SORTED_SUGGESTIONS]({ commit }, sortValue) {
      const result = await api.suggestion.getSortedSuggestions(sortValue);
      if (result && result.code == 200) {
        commit(suggestionMutations.SET_SUGGESTIONS, result.data);
      }
    },
    async [suggestionActions.GET_SUGGESTION_BY_ID]({ commit }, suggestionId) {
      const result = await api.suggestion.getSuggestionById(suggestionId);
      if (result && result.code == 200) {
        commit(suggestionMutations.SET_SUGGESTIONS, [result.data]);
      }
    },
    [suggestionActions.GET_SELECTED_SORT_KEY]({ commit }) {
      const sortKey = sessionStorage[sessionStorageKeyNames.SELECTED_SORT];
      commit(suggestionMutations.SET_SELECTED_SORT, sortKey);
    },
    [suggestionActions.SET_SELECTED_SORT_KEY]({ commit }, sortKey) {
      Vue.set(sessionStorage, sessionStorageKeyNames.SELECTED_SORT, sortKey);
      commit(suggestionMutations.SET_SELECTED_SORT, sortKey);
    }
  }
};
