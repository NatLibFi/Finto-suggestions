import Vue from 'vue';
import cookies from 'vue-cookies';
import App from './App.vue';
import router from './router/index';
import store from './store/index';

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  cookies,
  render: h => h(App)
}).$mount('#app');
