import Vue from 'vue';
import Router from 'vue-router';
import Index from '../views/Index.vue';
import Suggestion from '../views/Suggestion.vue';
import Meetings from '../views/Meetings.vue';
import MeetingSuggestionList from '../views/MeetingSuggestionList.vue';
import MeetingSuggestion from '../views/MeetingSuggestion.vue';

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
      path: '/meetings/:meetingId',
      name: 'meeting-suggestion-list',
      component: MeetingSuggestionList,
      props: true
    },
    {
      path: '/meetings/:meetingId/:suggestionId',
      name: 'meeting-suggestion',
      component: MeetingSuggestion,
      props: true
    }
  ],
  mode: 'history',
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    } else {
      return { x: 0, y: 0 };
    }
  }
});
