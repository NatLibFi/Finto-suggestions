import Vue from 'vue';
import { mapGetters, mapActions } from 'vuex';
import api from '../../../api';
import {
  namespace,
  storeStateNames,
} from './bundledStoreItemsConst';

// something = 'thumbs_up' || 'thumbs_down || ''happy ...;
// export const emojis = {
//   THUMBS_UP: 'thumbs_up',
//   THUMBS_DOWN: 'thumbs_down',
//   HAPPY: 'happy',
//   CONFUSED: 'confused',
//   RAISED_EYEBROW: 'raised_eyebrow',
//   ROCKET: 'rocket',
//   EYES: 'eyes',
//   HOORAY: 'hooray'
// };

let Tag = function(){
  this.label = '';
  this.color = '';
}
let Reaction = function(){
  this.user_id = 0;
  this.user_name = '';
  this.code = 0;
}
let Comment = function(){
  this.id = 0;
  this.user_id = 0;
  this.created = '';
  this.modified = '';
  this.text = '';
}
let Suggestion = function () {
  this.id = 0;
  this.suggestion_type = '';
  this.preferred_label = []; // [fi, sv ,en]
  this.alternative_labels = []; // [0..n]
  this.broader_labels = []; // [0..1]
  this.created = '';
  this.description = '';
  this.status = '';
  this.groups = []; // [0..n]
  this.created = '';
  this.modified = '';
  this.narrower_labels = []; // [0..n]
  this.organization = '';
  this.reason = '';
  this.related_labels = []; // [0..n]
  this.uri = ''
  this.scopeNote = '';
  this.exactMatches = '' 
  this.neededFor = ''
  this.yse_term = '';
  this.user_id = 0,
  this.reactions = [];
  this.tags = [];
  this.comments = [];
}

// const state = () => {
//   return {
//     ...
//   }
// }


export default {

  namespaced: true,
  state: {
    // [storeStateNames.ITEMS]: [],
    directives2: {
      sorting: 
      {
        sort: ''
      },
      search: 
      {
        search_word: '',
        filter: ''
      },
      paging: 
      {
        previous_page: 0,
        current_page: 0,
        next_page: 0,
        offset: 0,
        limit: 0
      }
    },
    user2: { 
      id: 0,
      name: '',
      email: '',
      created: '',
      imageUrl: '',
      role: '',
      organization: '',
      title: '' 
    },
    suggestions2: [],
    // storeStateItems: []
  },
  getters: {
    getSuggestions2: state => state[suggestions2]
  },
  mutations: {
    // Kokeillaan aluksi tapaa, jossa mutaatiolle tarjotaan actionissa Suggestion-tyyppinen
    // taulukko eli tämän tyyppinen taulukko muodostetaan actionissa 
    setSuggestions2(state, suggestions) {
      Vue.set(state, suggestions2, suggestions);
    },
    // setInitialData(state, initialData) {
    //   Vue.set(state, storeStateItems.ITEMS, initialData);
    // }
  },
  actions: {
    async getSuggestions2({ commit }, { offset, sort, filters, searchWord }) {
      const response = await api.suggestion.getSuggestions(offset, sort, filters, searchWord);
      if (response && response.code == 200) {
        console.log("Tähän alamme muodostaa responssia statelle sopivaan muotoon");
        console.log(response);
        // commit(suggestionMutations.SET_SUGGESTIONS, response.data);
        return response.items;
      } else {
        return '';
      }
    },
    // async addInitialData({ dispatch }, { data, suggestionId }) {
    //   const response = await api.suggestion.addInitialData()(data, suggestionId);
    //   if (response && response.code === 201) {
    //     commit(mutations.setInitialData(data));
    //   }
    // },
  },
  // mutations: {
  //   mutate(state, payload) {
  //       state[payload.property] = payload.with;
  //     }
  //   },
    
  async fetchAndCommitData({ state, commit }, payload) {
    try {
        let body = { jokuAvain: state.jokuArvo };
        if (payload) {
            body = Object.assign({}, payload.body, body);
        }
        let response = await api.post(
            body,
            state.config.serviceHeaders
        );
        if (payload.commit) {
            commit('mutate', {
                property: payload.stateProperty,
                with: response.data[payload.stateProperty]
            });
        }
        return response.data;
    } catch (error) {
        throw error;
    }
  },


};
