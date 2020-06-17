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
      const response = await api.suggestion.getSuggestions(offset, 'COMMENTS_DESC', filters, searchWord);
      if (response && response.code == 200) {
        let suggestionItems = [];
        for (let rootIndex = 0; rootIndex < Object.keys(response.data).length; rootIndex++) {
          const oneSuggestion = new Suggestion();
          if(response.data[rootIndex].id) {
            oneSuggestion.id = response.data[rootIndex].id; //
          }
          if(response.data[rootIndex].suggestion_type) {
            oneSuggestion.suggestion_type = response.data[rootIndex].suggestion_type;
          }
          if(response.data[rootIndex].preferred_label['fi']) {
            oneSuggestion.preferred_label["fi"] = response.data[rootIndex].preferred_label['fi']['value'] //
          }
          if(response.data[rootIndex].preferred_label['sv']) {
            oneSuggestion.preferred_label["sv"] = response.data[rootIndex].preferred_label['sv']['value'] //
          }
          if(response.data[rootIndex].preferred_label['en']) {
            oneSuggestion.preferred_label["en"] = response.data[rootIndex].preferred_label['en']['value'] //
          }
          if(response.data[rootIndex].alternative_labels[0]){
            for (let index = 0; index < Object.keys(response.data[rootIndex].alternative_labels).length; index++) {
              oneSuggestion.alternative_labels.push(response.data[rootIndex].alternative_labels[index]['value'])
            }
          }
          if(response.data[rootIndex].broader_labels[0]){
            let tempObjectForBroaderLabels = {}
            for (let index = 0; index < Object.keys(response.data[rootIndex].broader_labels).length; index++) {
              tempObjectForBroaderLabels['uri'] = response.data[rootIndex].broader_labels[index]['uri']
              tempObjectForBroaderLabels['value'] = response.data[rootIndex].broader_labels[index]['value']
              oneSuggestion.broader_labels.push(tempObjectForBroaderLabels)
              tempObjectForBroaderLabels = {}
            }
          }
          if(response.data[rootIndex].created){
            oneSuggestion.created = response.data[rootIndex].created
          }
          if(response.data[rootIndex].description){
            oneSuggestion.description = response.data[rootIndex].description
          }
          if(response.data[rootIndex].status){
            oneSuggestion.status = response.data[rootIndex].status
          }
          if(response.data[rootIndex].groups[0]){
            let tempObjectForGroups = {}
            for (let index = 0; index < Object.keys(response.data[rootIndex].groups).length; index++) {
              tempObjectForGroups['uri'] = response.data[rootIndex].groups[index]['uri']
              tempObjectForGroups['value'] = response.data[rootIndex].groups[index]['value']
              oneSuggestion.groups.push(tempObjectForGroups)
              tempObjectForGroups = {}
            }
          }
          if(response.data[rootIndex].created){
            oneSuggestion.created = response.data[rootIndex].created
          }
          if(response.data[rootIndex].modified){
            oneSuggestion.modified = response.data[rootIndex].modified
          }
          if(response.data[rootIndex].narrower_labels[0]){
            let tempObjectForNarrowerLabels = {}
            for (let index = 0; index < Object.keys(response.data[rootIndex].narrower_labels).length; index++) {
              tempObjectForNarrowerLabels['uri'] = response.data[rootIndex].narrower_labels[index]['uri']
              tempObjectForNarrowerLabels['value'] = response.data[rootIndex].narrower_labels[index]['value']
              oneSuggestion.narrower_labels.push(tempObjectForNarrowerLabels)
              tempObjectForNarrowerLabels = {}
            }
          }
          if(response.data[rootIndex].organization){
            oneSuggestion.organization = response.data[rootIndex].organization
          }
          if(response.data[rootIndex].reason){
            oneSuggestion.reason = response.data[rootIndex].reason
          }
          let tempObjectForRelatedLabels = {}
          if(response.data[rootIndex].related_labels[0]){
            for (let index = 0; index < Object.keys(response.data[rootIndex].related_labels).length; index++) {
              tempObjectForRelatedLabels['uri'] = response.data[rootIndex].related_labels[index]['uri']
              tempObjectForRelatedLabels['value'] = response.data[rootIndex].related_labels[index]['value']
              oneSuggestion.related_labels.push(tempObjectForRelatedLabels)
              tempObjectForRelatedLabels = {}
            }
          }
          if(response.data[rootIndex].exactMatches[0]){
            let tempObjectForExactMatches = {}
            for (let index = 0; index < Object.keys(response.data[rootIndex].exactMatches).length; index++) {
              tempObjectForExactMatches['value'] = response.data[rootIndex].exactMatches[index]['value']
              tempObjectForExactMatches['vocab'] = response.data[rootIndex].exactMatches[index]['vocab']
              oneSuggestion.exactMatches.push(tempObjectForExactMatches)
              tempObjectForExactMatches = {}
            }
          }
          if(response.data[rootIndex].neededFor){
            oneSuggestion.neededFor = response.data[rootIndex].neededFor; //
          }
          if(response.data[rootIndex].yse_term){
            oneSuggestion.yse_term = response.data[rootIndex].yse_term; //
          }
          if(response.data[rootIndex].user_id){
            oneSuggestion.user_id = response.data[rootIndex].user_id; //
          }
          if(response.data[rootIndex].events[0]){
            let commentsArray = []
            for (let index = 0; index < Object.keys(response.data[rootIndex].events).length; index++) {
              if (response.data[rootIndex].events[index].event_type === 'COMMENT') {
                const oneComment = new Comment()
                oneComment.id = response.data[rootIndex].events[index].id
                oneComment.user_id = response.data[rootIndex].events[index].user_id
                oneComment.created = response.data[rootIndex].events[index].created
                oneComment.modified = response.data[rootIndex].events[index].modified
                oneComment.text = response.data[rootIndex].events[index].text


                ///
                // // async [reactionActions.GET_REACTIONS_BY_SUGGESTION]({ commit }, suggestion_id) {
                //   // console.log(response.data[rootIndex].events[index].id)
                // const reactionsForOneComment = await api.reaction.getReactionsByEvent(6064);
                // // const reactionsForOneComment = await api.reaction.getReactionsByEvent(response.data[rootIndex].events[index].id);
                // if (reactionsForOneComment && reactionsForOneComment.code === 200) {
                //   const oneReaction = new Reaction()
                //   // oneReaction.code = reactionsForOneComment.data[rootIndex].events[index].user_id
                //   // commit(reactionMutations.SET_REACTIONS, response.data);
                //   // console.log("SDSDSDSDSSDSDSSDSDSSDSDSDSDS")
                //   for (let index = 0; index < Object.keys(reactionsForOneComment.data).length; index++) {
                //     console.log(reactionsForOneComment.data[index].code)
                    
                //   }
                // }
                // }

                ///

                commentsArray.push(oneComment)
              }
              oneSuggestion.comments = commentsArray
            }
          }
          suggestionItems.push(oneSuggestion)
        }
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
