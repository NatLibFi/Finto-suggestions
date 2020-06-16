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
        if(response.data[2].id) {
          oneSuggestion.id = response.data[2].id; //
        }
        if(response.data[2].suggestion_type) {
          oneSuggestion.suggestion_type = response.data[2].suggestion_type;
        }
        if(response.data[2].preferred_label['fi']) {
          oneSuggestion.preferred_label["fi"] = response.data[2].preferred_label['fi']['value'] //
        }
        if(response.data[2].preferred_label['sv']) {
          oneSuggestion.preferred_label["sv"] = response.data[2].preferred_label['sv']['value'] //
        }
        if(response.data[2].preferred_label['en']) {
          oneSuggestion.preferred_label["en"] = response.data[2].preferred_label['en']['value'] //
        }
        for (let index = 0; index < Object.keys(response.data[2].alternative_labels).length; index++) {
          oneSuggestion.alternative_labels.push(response.data[2].alternative_labels[index]['value'])
        }
        if(response.data[2].broader_labels[0]){
          let tempObjectForBroaderLabels = {}
          for (let index = 0; index < Object.keys(response.data[2].broader_labels).length; index++) {
            tempObjectForBroaderLabels['uri'] = response.data[2].broader_labels[index]['uri']
            tempObjectForBroaderLabels['value'] = response.data[2].broader_labels[index]['value']
            oneSuggestion.broader_labels.push(tempObjectForBroaderLabels)
            tempObjectForBroaderLabels = {}
          }
        }
        if(response.data[2].created){
          oneSuggestion.created = response.data[2].created
        }
        if(response.data[2].description){
          oneSuggestion.description = response.data[2].description
        }
        if(response.data[2].status){
          oneSuggestion.status = response.data[2].status
        }
        if(response.data[2].groups[0]){
          let tempObjectForGroups = {}
          for (let index = 0; index < Object.keys(response.data[2].groups).length; index++) {
            tempObjectForGroups['uri'] = response.data[2].groups[index]['uri']
            tempObjectForGroups['value'] = response.data[2].groups[index]['value']
            oneSuggestion.groups.push(tempObjectForGroups)
            tempObjectForGroups = {}
          }
        }
        if(response.data[2].created){
          oneSuggestion.created = response.data[2].created
        }
        if(response.data[2].modified){
          oneSuggestion.modified = response.data[2].modified
        }
        if(response.data[2].narrower_labels[0]){
          let tempObjectForNarrowerLabels = {}
          for (let index = 0; index < Object.keys(response.data[2].narrower_labels).length; index++) {
            tempObjectForNarrowerLabels['uri'] = response.data[2].narrower_labels[index]['uri']
            tempObjectForNarrowerLabels['value'] = response.data[2].narrower_labels[index]['value']
            oneSuggestion.narrower_labels.push(tempObjectForNarrowerLabels)
            tempObjectForNarrowerLabels = {}
          }
        }
        if(response.data[2].organization){
          oneSuggestion.organization = response.data[2].organization
        }
        if(response.data[2].reason){
          oneSuggestion.reason = response.data[2].reason
        }
        let tempObjectForRelatedLabels = {}
        if(response.data[2].related_labels[0]){
          for (let index = 0; index < Object.keys(response.data[2].related_labels).length; index++) {
            tempObjectForRelatedLabels['uri'] = response.data[2].related_labels[index]['uri']
            tempObjectForRelatedLabels['value'] = response.data[2].related_labels[index]['value']
            oneSuggestion.related_labels.push(tempObjectForRelatedLabels)
            tempObjectForRelatedLabels = {}
          }
        }
        if(response.data[2].exactMatches[0]){
          let tempObjectForExactMatches = {}
          for (let index = 0; index < Object.keys(response.data[2].exactMatches).length; index++) {
            tempObjectForExactMatches['value'] = response.data[2].exactMatches[index]['value']
            tempObjectForExactMatches['vocab'] = response.data[2].exactMatches[index]['vocab']
            oneSuggestion.exactMatches.push(tempObjectForExactMatches)
            tempObjectForExactMatches = {}
          }
        }
        if(response.data[2].neededFor){
          oneSuggestion.neededFor = response.data[2].neededFor; //
        }
        if(response.data[2].yse_term){
          oneSuggestion.yse_term = response.data[2].yse_term; //
        }
        if(response.data[2].user_id){
          oneSuggestion.user_id = response.data[2].user_id; //
        }

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
