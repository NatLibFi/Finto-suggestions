<template>
<!-- Using 'login' as a catch-all term for signups and logins -->
<div class="login-dialog">
  <div v-if="signupSucceeded">
    <h3>Tunnus luotu onnistuneesti</h3>
    <p>Tunnuksesi on luotu!</p>
    <p>Voit nyt kirjautua sisään.</p>
  </div>
  <div v-else>
    <h3>Tunnuksesi luomisessa tuli virhe</h3>
    <p>{{ errorMessage }}</p>
    <p>
      Jos unohdit salasanasi, voit nollata sen
      <span class="changePassword" @click="showResetPasswordForm()">täältä</span>.
    </p>
  </div>
</div>
</template>

<script>
export default {
  props: {
    signupSucceeded: {
      type: Boolean,
      required: true
    },
    errorMessage: {
      type: String,
      required: false
    }
  },
  methods: {
    showResetPasswordForm() {
      this.$emit('openResetPasswordForm');
    }
  }
};
</script>


<style scoped>
.login-dialog {
  padding: 20px;
  overflow: none;
}

.changePassword {
  color: #06a798;
  font-weight: 600;
  transition: color 0.1s;
  cursor: pointer;
  cursor: hand;
}

.changePassword:hover {
  color: #21baac;
}
</style>
