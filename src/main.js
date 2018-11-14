import Vue from 'vue';
import VueSource from 'vue-resource';
import MuseUI from 'muse-ui';
import router from './router/router.js';
import store from './store/store.js';

import App from './App.vue';

Vue.use(MuseUI);
Vue.use(VueSource);

const http =  {
    emulateJSON: true,
    emulateHTTP: true
};

Vue.http.options.emulateJSON = true;

Vue.config.productionTip = true;
new Vue({
    http,
    router,
    store,
    el: '#app',
    render: h => h(App)
});