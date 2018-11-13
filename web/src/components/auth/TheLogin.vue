<template>
<div class="login-dialog">
  <h3>Kirjaudu sisään</h3>
  <p>Voit kirjautua sisään Github- ja Google-tunnuksilla</p>
  <div class="login-services">
    <div @click="login('github')" class="login-service-button">
      <div class="login-service-image"></div>
      <span>Kirjaudu GitHub-tunnuksilla</span>
    </div>
    <div @click="login('google')" class="login-service-button">
      <div class="login-service-image"></div>
      <span>Kirjaudu Google-tunnuksilla</span>
    </div>
  </div>
  <div class="login-own-credentials">
    <h4 v-if="!showOwnCredentialLogin" @click="showOwnCredentialLogin = !showOwnCredentialLogin">
      Kirjaudu sisään omilla tunnuksilla
    </h4>
    <div v-if="showOwnCredentialLogin" class="login-inputs">
      <div class="login-input">
        <span>Käyttäjätunnus</span>
        <input type="text">
      </div>
      <div class="login-input">
        <span>Salasana</span>
        <input type="password">
      </div>
      <div @click="login()" class="login-submit">
        <span>Kirjaudu sisään</span>
      </div>
      <div class="login-forgot-password">
        <span>Unohditko salasanasi?</span>
      </div>
    </div>
  </div>
</div>
</template>

<script>
export default {
  data: () => ({
    showOwnCredentialLogin: false
  }),
  methods: {
    login(service) {
      this.$emit('login', service);
    }
  }
};
</script>


<style scoped>
.login-dialog {
  padding-top: 20px;
  overflow: none;
}

.login-services {
  margin-top: 25px;
  border-bottom: 1px solid #eeeeee;
  padding-bottom: 20px;
}

.login-service-button {
  margin: 10px 15%;
  padding: 22px 0;
  border: 2px solid #eeeeee;
  border-radius: 2px;
  font-size: 13px;
  font-weight: 600;
  position: relative;
  transition: all 0.1s;
}

.login-service-button:hover {
  border: 2px solid #a7e7e1;
  cursor: pointer;
  cursor: hand;
}

.login-service-image {
  position: absolute;
  left: 20px;
  top: 50%;
  transform: perspective(1px) translateY(-50%);
  display: inline-block;
  height: 20px;
  width: 20px;
  background-color: #eeeeee;
}

.login-service-button span {
  position: absolute;
  right: 22px;
  top: 50%;
  transform: perspective(1px) translateY(-50%);
}

.login-own-credentials {
  padding-top: 10px;
}

.login-own-credentials h4 {
  color: #06a798;
  transition: color 0.1s;
}

.login-own-credentials h4:hover {
  color: #21baac;
  cursor: pointer;
  cursor: hand;
}

.login-input {
  margin: 10px 15%;
}

.login-input span {
  display: block;
  text-align: left;
  font-weight: 600;
  font-size: 13px;
  margin-bottom: 2px;
}

.login-input input {
  width: 100%;
  padding: 10px 0;
  border: 2px solid #eeeeee;
  border-radius: 1px;
  font-weight: 600;
  font-size: 13px;
  box-sizing: border-box;
}

.login-input [type='text'],
.login-input [type='password'] {
  padding: 11px 8px;
}

.login-submit {
  margin: 18px 15% 10px;
  padding: 12px 0 11px;
  background-color: #06a798;
  border: 2px solid #06a798;
  border-radius: 1px;
  color: #ffffff;
  font-weight: 600;
  font-size: 13px;
  cursor: pointer;
  cursor: hand;
  transition: all 0.1s;
}

.login-submit:hover {
  background-color: #21baac;
  border-color: #21baac;
}

.login-forgot-password {
  margin: 20px 0 10px;
}

.login-forgot-password span {
  font-weight: 600;
  color: #06a798;
  cursor: pointer;
  cursor: hand;
  transition: all 0.1s;
}

.login-forgot-password span:hover {
  color: #21baac;
}

@media (max-width: 750px) {
  .login-service-button {
    margin: 10px 6%;
  }

  .login-service-button span {
    left: 50px;
  }

  .login-input,
  .login-submit {
    margin: 10px 6%;
  }
}
</style>