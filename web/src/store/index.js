import Vue from 'vue';
import Vuex from 'vuex';

import suggestionModule from './modules/suggestion/suggestionModule';
import meetingModule from './modules/meeting/meetingModule';
import tagModule from './modules/tag/tagModule';
import eventModule from './modules/event/eventModule';
import authModule from './modules/auth/authModule';

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    suggestion: suggestionModule,
    meeting: meetingModule,
    tag: tagModule,
    event: eventModule,
    auth: authModule
  }
});
