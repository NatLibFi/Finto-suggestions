<template>
<div>
  <p v-if="!hasFailed">
    Kirjaudutaan sisään GitHub-tunnuksilla...
  </p>
  <p v-if="hasFailed">
    Kirjautuminen epäonnistui. Palataan takaisin ehdotusalustalle.
  </p>
</div>
</template>

<script>
import router from '../../router/index';
// eslint-disable-next-line
import { mapAuthenticatedUserActions, mapAuthenticatedUserGetters } from '../../store/modules/authenticatedUser/authenticatedUserModule';
// eslint-disable-next-line
import { authenticatedUserActions, authenticatedUserGetters } from '../../store/modules/authenticatedUser/authenticatedUserConsts';

export default {
  data: () => ({
    code: '',
    hasFailed: false
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
        if (splitArray && splitArray.length > 0) {
          this.code = splitArray[1];
        }
      }
    },
    async callAuthenticate() {
      if (this.code && this.code.length > 0) {
        await this.authenticate({ code: this.code })
        .catch(() => {
          this.hasFailed = true;
          setTimeout(() => {
            this.hasFailed = false;
            this.goToFrontPage();
          }, 2000);
        });
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
      router.go(-1);
    }
  }
};
</script>
