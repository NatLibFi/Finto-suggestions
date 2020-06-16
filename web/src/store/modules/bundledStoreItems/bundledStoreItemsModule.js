import Vue from 'vue';
import api from '../../../api';

// anotherWay = 'thumbs_up' || 'thumbs_down || ''happy ...;
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

class Tag {
  constructor(){
    this.label = '';
    this.color = '';
  }
}
class Reaction{
  constructor() {
    this.user_id = 0;
    this.user_name = '';
    this.code = 0;
  }
}
class Comment{
  constructor() {
    this.id = 0;
    this.user_id = 0;
    this.created = '';
    this.modified = '';
    this.text = '';
  }
}
class Suggestion{
  constructor() {
    this.id = 0;
    this.suggestion_type = '';
    this.preferred_label = {}; // [fi, sv ,en]
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
    this.exactMatches = []; 
    this.neededFor = ''
    this.yse_term = '';
    this.user_id = 0,
    this.reactions = [];
    this.tags = [];
    this.comments = [];
  }
}

const bundledItems = {
  namespaced: true,
  state: {
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
  },
  getters: {
    getSuggestions2: state => state[suggestions2]
  },
  mutations: {
    setSuggestions2(state, data) {
      state.suggestions2 = data;
    },
  },
  actions: {
    async getSuggestionsFromDBAndCommitState({ commit }, { offset, sort, filters, searchWord }) {
      const response = await api.suggestion.getSuggestions(offset, sort, filters, searchWord);
      if (response && response.code == 200) {
        let suggestionItems = [];
        console.log("Tähän alamme muodostaa responssia statelle sopivaan muotoon");
        const oneSuggestion = new Suggestion();
        console.log("The size of response.data for the looping under construction is:")
        console.log(Object.keys(response.data).length)
        oneSuggestion.id = response.data[2].id; //
        oneSuggestion.suggestion_type = response.data[2].suggestion_type;
        console.log("The size of preferred_label for the looping under construction is:")
        console.log(Object.keys(response.data[2].preferred_label).length)
        oneSuggestion.preferred_label["fi"] = response.data[2].preferred_label['fi']['value'] //
        oneSuggestion.preferred_label["sv"] = response.data[2].preferred_label['sv']['value'] //
        oneSuggestion.preferred_label["en"] = response.data[2].preferred_label['en']['value'] //
        console.log("The size of alternative_labels for the looping under construction is:")
        console.log(Object.keys(response.data[2].alternative_labels).length)
        oneSuggestion.alternative_labels.push(response.data[2].alternative_labels[0]['value'])
        oneSuggestion.alternative_labels.push(response.data[2].alternative_labels[1]['value'])
        oneSuggestion.alternative_labels.push(response.data[2].alternative_labels[2]['value'])
        console.log("The size of broader_labels for the looping under construction is:")
        console.log(Object.keys(response.data[2].broader_labels).length)
        let tempObjectForBroaderLabels = {}
        tempObjectForBroaderLabels['uri'] = response.data[2].broader_labels[0]['uri']
        tempObjectForBroaderLabels['value'] = response.data[2].broader_labels[0]['value']
        oneSuggestion.broader_labels.push(tempObjectForBroaderLabels)
        tempObjectForBroaderLabels = {}
        oneSuggestion.created = response.data[2].created
        oneSuggestion.description = response.data[2].description
        oneSuggestion.status = response.data[2].status
        let tempObjectForGroups = {}
        tempObjectForGroups['uri'] = response.data[2].groups[0]['uri']
        tempObjectForGroups['value'] = response.data[2].groups[0]['value']
        oneSuggestion.groups.push(tempObjectForGroups)
        tempObjectForGroups = {}
        oneSuggestion.created = response.data[2].created
        oneSuggestion.modified = response.data[2].modified
        let tempObjectForNarrowerLabels = {}
        if(!!response.data[2].narrower_labels[0]){
          console.log("The size of narrower_labels for the looping under construction is:")
          console.log(Object.keys(response.data[2].narrower_labels).length)
          tempObjectForNarrowerLabels['uri'] = response.data[2].narrower_labels[0]['uri']
        }
        if(!!response.data[2].narrower_labels[0]){
          console.log("The size of narrower_labels for the looping under construction is:")
          console.log(Object.keys(response.data[2].narrower_labels).length)
          tempObjectForNarrowerLabels['value'] = response.data[2].narrower_labels[0]['value']
        }
        oneSuggestion.narrower_labels.push(tempObjectForNarrowerLabels)
        tempObjectForNarrowerLabels = {}
        oneSuggestion.organization = response.data[2].organization
        oneSuggestion.reason = response.data[2].reason
        if(!!response.data[2].related_labels[0]){
          console.log("The size of related_labels for the looping under construction is:")
          console.log(Object.keys(response.data[2].related_labels).length)
        }
        if(!!response.data[2].related_labels[0]){
          console.log("The size of related_labels for the looping under construction is:")
          console.log(Object.keys(response.data[2].related_labels).length)
        }
        let tempObjectForExactMatches = {}
        if(!!response.data[2].exactMatches[0]){
          console.log("The size of exactMatches for the looping under construction is:")
          console.log(Object.keys(response.data[2].exactMatches).length)
          tempObjectForExactMatches['vocab'] = response.data[2].exactMatches[0]['vocab']
          tempObjectForExactMatches['value'] = response.data[2].exactMatches[0]['value']
        }
        oneSuggestion.exactMatches.push(tempObjectForExactMatches)
        tempObjectForExactMatches = {}
        if(!!response.data[2].exactMatches[1]){
          console.log("The size of exactMatches for the looping under construction is:")
          console.log(Object.keys(response.data[2].exactMatches).length)
          tempObjectForExactMatches['vocab'] = response.data[2].exactMatches[1]['vocab']
          tempObjectForExactMatches['value'] = response.data[2].exactMatches[1]['value']
        }
        oneSuggestion.exactMatches.push(tempObjectForExactMatches)
        tempObjectForExactMatches = {}
        oneSuggestion.neededFor = response.data[2].neededFor; //
        oneSuggestion.yse_term = response.data[2].yse_term; //
        oneSuggestion.user_id = response.data[2].user_id; //

        suggestionItems.push(oneSuggestion)
        // this.reactions = [];
        // this.tags = [];
        // this.comments = [];        

        // if (response.data.suggestions2['id'] === 8137){
        // }
        // function goThroughEntireObjectTree(o) {
        //   for (var i in o) {
        //       if (!!o[i] && typeof(o[i])=="object") {
        //           // console.log(i, o[i]);
        //           console.log("Avain on:");
        //           console.log(i); // Tämä on avain
        //           console.log("ja sen arvo on:");
        //           console.log(o[i]);
        //           goThroughEntireObjectTree(o[i]);
        //       } 
        //       // else {
        //       //     // console.log(i, o[i]);
        //       //     // console.log("Ei kuulu joukkoon")
        //       //     null
        //       // }
        //   }
        // }
        // goThroughEntireObjectTree(response.data);
        // next toimii
        // commit('setSuggestions2', response.data);
        
        commit('setSuggestions2', suggestionItems);
        return response.data;
      } else {
        return '';
      }
    },
  },
  // "ORIG"
  // actions: {
  //   async getSuggestionsFromDBAndCommitState({ commit }, { offset, sort, filters, searchWord }) {
  //     const response = await api.suggestion.getSuggestions(offset, 8138sort, filters, searchWord);
  //     if (response && response.code == 200) {
  //       console.log("Tähän alamme muodostaa responssia statelle sopivaan muotoon");
  //       console.log(response.data);
  //       commit('setSuggestions2', response);
  //       return response.items;
  //     } else {
  //       return '';
  //     }
  //   },
  // },
  ///
  // *** The mutations will be dealt with a dedicated function.
  // *** It is a way to dramatically decrease the amount of boilerplate code
  // *** for the mutatons. It is same with the actions. There will be only one
  // *** action for all the "actions"
  // *** FOR MUTATIONs something like this:
  // mutations: {
  //   mutate(state, payload) {
  //       state[payload.property] = payload.with;
  //     }
  //   },
  // *** FOR ACTIONSs something like this:
  // async fetchAndCommitData({ state, commit }, payload) {
  //   try {
  //       let body = { jokuAvain: state.jokuArvo };
  //       if (payload) {
  //           body = Object.assign({}, payload.body, body);
  //       }
  //       let response = await api.somePathToEndPoint.post(
  //           body,
  //           state.config.serviceHeaders
  //       );
  //       if (payload.commit) {
  //           commit('mutate', {
  //               property: payload.stateProperty,
  //               with: response.data[payload.stateProperty]
  //           });
  //           // or without 'mutate'
  //           commit({
  //             property: payload.stateProperty,
  //             with: response.data[payload.stateProperty]
  //         });
  //       }
  //       return response.data;
  //   } catch (error) {
  //       throw error;
  //   }
  // },
};

export default bundledItems
