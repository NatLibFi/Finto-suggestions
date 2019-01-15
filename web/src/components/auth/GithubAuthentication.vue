<template>
</template>

<script>
import router from '../../router/index';

import { mapAuthenticatedUserActions, mapAuthenticatedUserGetters } from '../../store/modules/authenticatedUser/authenticatedUserModule';
import { authenticatedUserActions, authenticatedUserGetters } from '../../store/modules/authenticatedUser/authenticatedUserConsts';

export default {
  data: () => ({
    code: ''
  }),
  computed: {
    ...mapAuthenticatedUserGetters({
      isAuthenticated: authenticatedUserGetters.GET_IS_AUTHENTICATED,
      error: authenticatedUserGetters.GET_AUTHENTICATE_ERROR
    })
  },
  created() {
    this.parseCodeFromQueryString(window.location.search);
  },
  methods: {
    ...mapAuthenticatedUserActions({
      authenticate: authenticatedUserActions.AUTHENTICATE
    }),
    parseCodeFromQueryString(query) {
      if (query && query.length > 0) {
        const splitArray = query.split('=');
        if(splitArray && splitArray.length > 0) {
          this.code = splitArray[1];
        }
      }
    },
    async callAuthenticate() {
      if(this.code && this.code.length > 0) {
        await this.authenticate({ code: this.code });
      }
    },
    goToFrontPage() {
      router.push('/');
    }
  },
  watch: {
    async code() {
      await this.callAuthenticate();
    },
    isAuthenticated() {
      this.goToFrontPage();
    },
    error() {
      this.goToFrontPage();
    }
  }
};
</script>
