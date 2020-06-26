import Vue from 'vue';
import api from '../../../api';
// import getTwoEntities from './tools'
import * as entitiesX from './tools';

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
    this.code = '';
  }
}
class Comment{
  constructor() {
    this.id = 0;
    this.user_id = 0;
    this.created = '';
    this.modified = '';
    this.text = '';
    this.reactions = [];
    this.path = null;
  }
}
class Suggestion{
  constructor() {
    this.id = 0;
    this.suggestion_type = {};
    // this.suggestion_type.path = null;
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
    this.pathItemName = '';
    this.pathItemNumber = Number;
    this.path = null;
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
      state.suggestions2 = data
      // suggestion_type
      // state.suggestions2[0]['suggestion_type'] = 'MODIFY' // normilistaus
      // state.suggestions2[0].alternative_labels[0].value = "kattiXYZ" // normilistaus
      state.suggestions2[0].comments[1].text = "kattiXYZ" // eniten kommentteja

      // console.log("Objektin propertiesit:")
      // console.log(Object.keys(state.suggestions2).map(function(key){ return state.suggestions2[key] }));

      },
    },
    
    actions: {
      async getSuggestionsFromDBAndCommitState({ commit }, { offset, sort, filters, searchWord }) {
        const entityForTesting = {
          itemOne: "kohdistetaan talletus ",
          itemTwo: "tähän objektiin"
        }
        console.log(entitiesX.getTwoEntities(entityForTesting))
        let conditionForFilter = ''
        let secondConditionForFilter = ''
        let thirdConditionForFilter = ''
        var filterDefinitions = function(listItem) {
          return listItem[conditionForFilter]
        }
        // The next line for test purposes
        // const response = await api.suggestion.getSuggestions(offset, 'COMMENTS_DESC', filters, searchWord);
        const response = await api.suggestion.getSuggestions(offset, 'COMMENTS_DESC', filters, searchWord);
        if (response && response.code == 200) {
          let suggestionItems = [];
          for (let rootIndex = 0; rootIndex < Object.keys(response.data).length; rootIndex++) {
            const oneSuggestion = new Suggestion();
            // oneSuggestion.pathItemName = 'id'
            oneSuggestion.path = rootIndex
            if(response.data[rootIndex].id) {
              oneSuggestion.id = response.data[rootIndex].id; //
            }
            if(response.data[rootIndex].suggestion_type) {
              oneSuggestion.suggestion_type["suggestion_type"] = response.data[rootIndex].suggestion_type;
              oneSuggestion.suggestion_type["path"] = rootIndex+".suggestion_type"
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
            let tagsArrayForOneSuggestion = []
            if (response.data[rootIndex].tags[0]) {
              for (let index = 0; index < response.data[rootIndex].tags.length; index++) {
                const oneTagForSuggestion = new Tag()
                oneTagForSuggestion.color = response.data[rootIndex].tags[index]['color']
                oneTagForSuggestion.label = response.data[rootIndex].tags[index]['label']
                tagsArrayForOneSuggestion.push(oneTagForSuggestion)
              }
              oneSuggestion.tags = tagsArrayForOneSuggestion
              tagsArrayForOneSuggestion = []
            }
            const reactionsForSuggestionResponse = await api.reaction.getReactionsBySuggestion(response.data[rootIndex].id)
            let reactionsArrayForOneSuggestion = []
            if (reactionsForSuggestionResponse.data[0]) {
              for (let index = 0; index < reactionsForSuggestionResponse.data.length; index++) {
                const oneReactionForSuggestion = new Reaction()
                oneReactionForSuggestion.code = reactionsForSuggestionResponse.data[index]['code']
                oneReactionForSuggestion.user_id = reactionsForSuggestionResponse.data[index]['user_id']
                // oneReaction.user_name = someResponseInTheFuture[index]['user_name'] // Should be added later on
                reactionsArrayForOneSuggestion.push(oneReactionForSuggestion)
              }
              oneSuggestion.reactions = reactionsArrayForOneSuggestion
              reactionsArrayForOneSuggestion = []
            }
            if(response.data[rootIndex].alternative_labels[0]){
              conditionForFilter = 'value'
              oneSuggestion.alternative_labels = response.data[rootIndex].alternative_labels.filter(filterDefinitions)
              conditionForFilter = ''
            }
            if(response.data[rootIndex].broader_labels[0] && response.data[rootIndex].broader_labels.length < 2){
              conditionForFilter = 'uri'
              oneSuggestion.broader_labels = response.data[rootIndex].broader_labels.filter(filterDefinitions)
              conditionForFilter = ''
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
              conditionForFilter = 'value'
              oneSuggestion.groups = response.data[rootIndex].groups.filter(filterDefinitions)
              conditionForFilter = ''
            }
            if(response.data[rootIndex].created){
              oneSuggestion.created = response.data[rootIndex].created
            }
            if(response.data[rootIndex].modified){
              oneSuggestion.modified = response.data[rootIndex].modified
            }
            if(response.data[rootIndex].narrower_labels[0]){
              // Wait until you have found a good real life example of the suggestion with narrow_label
              // conditionForFilter = 'uri' // or 'value'
              // oneSuggestion.narrower_labels = response.data[rootIndex].narrower_labels.filter(filterDefinitions)
              // conditionForFilter = ''
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
            if(response.data[rootIndex].related_labels[0]){
              conditionForFilter = 'uri' // or value
              oneSuggestion.related_labels = response.data[rootIndex].related_labels.filter(filterDefinitions)
              conditionForFilter = ''
            }
            if(response.data[rootIndex].exactMatches[0]){
              conditionForFilter = 'value' // or 'vocab'
              oneSuggestion.exactMatches = response.data[rootIndex].exactMatches.filter(filterDefinitions)
              conditionForFilter = ''
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
                  oneComment.path = rootIndex+".comments."+(index-1)
                  const reactionsResponse = await api.reaction.getReactionsByEvent(response.data[rootIndex].events[index].id)
                  let reactionsArray = []
                    if (reactionsResponse.data[0]) {
                      for (let index = 0; index < reactionsResponse.data.length; index++) {
                        const oneReaction = new Reaction()
                        oneReaction.code = reactionsResponse.data[index]['code']
                        oneReaction.user_id = reactionsResponse.data[index]['user_id']
                        // oneReaction.user_name = someResponseInTheFuture[index]['user_name']
                        reactionsArray.push(oneReaction)
                      }
                    oneComment.reactions = reactionsArray
                    reactionsArray = []
                    }
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
