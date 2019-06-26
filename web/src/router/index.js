import Vue from 'vue';
import Router from 'vue-router';
import Suggestions from '../views/Suggestions';
import Suggestion from '../views/Suggestion';
import User from '../views/User';
import UserSettings from '../views/UserSettings';
import Meetings from '../views/Meetings';
import MeetingSuggestionList from '../views/MeetingSuggestionList';
import MeetingSuggestion from '../views/MeetingSuggestion';

import GithubAuthentication from '../components/auth/GithubAuthentication';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'index',
      component: Suggestions,
      props: () => ({
        page: 1
      })
    },
    {
      path: '/suggestions/:page',
      name: 'suggestions',
      component: Suggestions,
      props: route => ({
        page: route.params.page
      })
    },
    {
      path: '/suggestion/:suggestionId',
      name: 'suggestion',
      component: Suggestion,
      props: true
    },
    {
      path: '/users/:userId/:page',
      name: 'user',
      component: User,
      props: route => ({
        userId: route.params.userId,
        page: route.params.page
      })
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
      path: '/meetings/:meetingId/:page',
      name: 'meeting-suggestion-list',
      component: MeetingSuggestionList,
      props: route => ({
        meetingId: route.params.meetingId,
        page: route.params.page
      })
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
    },
    {
      path: '*',
      redirect: '/'
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
