<template>
<!-- Using 'login' as a catch-all term for signups and logins -->
<div class="login-dialog">
  <h3>Tunnus luotu onnistuneesti</h3>
  <p>Tunnuksesi on luotu!</p>
  <p>Voit nyt kirjautua sisään.</p>
</div>
</template>

<style scoped>
.login-dialog {
  padding-top: 20px;
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
