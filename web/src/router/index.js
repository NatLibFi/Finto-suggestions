import Vue from 'vue';
import Router from 'vue-router';
import Index from '../views/Index.vue';
import Suggestion from '../views/Suggestion.vue';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'index',
      component: Index
    },
    {
      path: '/suggestion/:suggestionID',
      name: 'suggestion',
      component: Suggestion
    }
  ],
  mode: 'history'
});
