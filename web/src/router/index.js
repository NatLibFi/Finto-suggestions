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
      path: '/suggestion/:suggestionId',
      name: 'suggestion',
      component: Suggestion,
      props: true
    }
  ],
  mode: 'history'
});
