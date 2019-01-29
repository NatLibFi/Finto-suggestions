import Vue from 'vue';
import Router from 'vue-router';
import Index from '../views/Index.vue';
import Suggestion from '../views/Suggestion.vue';
import User from '../views/User.vue';
import UserSettings from '../views/UserSettings.vue';
import Meetings from '../views/Meetings.vue';
import MeetingSuggestionList from '../views/MeetingSuggestionList.vue';
import MeetingSuggestion from '../views/MeetingSuggestion.vue';

import GithubAuthentication from '../components/auth/GithubAuthentication';

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
      path: '/users/:userId',
      name: 'user',
      component: User,
      props: true
      // TODO: beforeEnter check authentication
    },
    {
      path: '/settings',
      name: 'settings',
      component: UserSettings,
      props: true
      // TODO: beforeEnter check authentication
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
    },
    {
      path: '/github',
      beforeEnter() {
        const github_url = process.env.VUE_APP_GITHUB_LOGIN_URL;
        const client_id = process.env.VUE_APP_GITHUB_CLIENT_ID;
        window.location.href = `${github_url}&client_id=${client_id}`;
      }
    },
    {
      path: '/auth/redirect/github',
      name: 'oauth-redirect',
      component: GithubAuthentication,
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
