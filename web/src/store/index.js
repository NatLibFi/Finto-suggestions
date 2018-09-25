import Vue from 'vue';
import Vuex from 'vuex';

import suggestionModule from './modules/suggestion/suggestionModule';

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    suggestion: suggestionModule
  }
});
