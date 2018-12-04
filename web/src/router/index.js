import Vue from 'vue';
import Router from 'vue-router';
import Index from '../views/Index.vue';
import Suggestion from '../views/Suggestion.vue';
import Meetings from '../views/Meetings.vue';
import Meeting from '../views/Meeting.vue';

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
    },
    {
      path: '/meetings',
      name: 'meetings',
      component: Meetings
    },
    {
      path: 'meeting/:meetingId',
      name: 'meeting',
      component: Meeting,
      props: true
    }
  ],
  mode: 'history'
});
