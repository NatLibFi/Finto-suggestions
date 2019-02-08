import Vue from 'vue';

import Vuelidate from 'vuelidate';
Vue.use(Vuelidate);

import App from './App.vue';
import router from './router/index';
import store from './store/index';

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app');
