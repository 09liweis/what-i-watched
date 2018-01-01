import Vue from 'vue';
import VueResource from 'vue-resource';
import App from './App.vue';
import router from './router.js';
import MuseUI from 'muse-ui';
// import 'muse-ui/dist/muse-ui.css';
Vue.use(MuseUI);
Vue.use(VueResource);

const http =  {
    emulateJSON: true,
    emulateHTTP: true
};

Vue.http.options.emulateJSON = true;

new Vue({
    http,
    router,
    el: '#app',
    render: h => h(App)
});