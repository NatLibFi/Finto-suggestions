import Vue from 'vue';
import { mapGetters, mapActions } from 'vuex';
import api from '../../../api';
import {
  namespace,
  storeStateNames,
  reactionGetters,
  reactionMutations,
  reactionActions
} from './reactionConsts';
import {
  namespace as suggestionNamespace,
  suggestionActions
} from '../suggestion/suggestionConsts';
import { namespace as eventNamespace, eventActions } from '../event/eventConsts';

export const mapReactionGetters = getters => mapGetters(namespace, getters);
export const mapReactionActions = actions => mapActions(namespace, actions);

export default {
  namespaced: true,
  state: {
    [storeStateNames.ITEMS]: []
  },
  getters: {
    [reactionGetters.GET_REACTIONS]: state => state[storeStateNames.ITEMS]
  },
  mutations: {
    [reactionMutations.SET_REACTIONS](state, reactions) {
      Vue.set(state, storeStateNames.ITEMS, reactions);
    }
  },
  actions: {
    async [reactionActions.ADD_REACTION]({ dispatch }, { data, suggestionId }) {
      const response = await api.reaction.addReaction(data);
      if (response && response.code === 201) {
        if (!data.event_id) {
          dispatch(
            `${suggestionNamespace}/${suggestionActions.GET_SUGGESTION_BY_ID}`,
            suggestionId,
            {
              root: true
            }
          );
        } else if (data.event_id) {
          dispatch(`${eventNamespace}/${eventActions.GET_EVENTS_BY_SUGGESTION}`, suggestionId, {
            root: true
          });
        }
      }
    },
    async [reactionActions.GET_REACTIONS_BY_SUGGESTION]({ commit }, suggestion_id) {
      const response = await api.reaction.getReactionsBySuggestion(suggestion_id);
      if (response && response.code === 200) {
        commit(reactionMutations.SET_REACTIONS, response.data);
      }
    }
  }
};
