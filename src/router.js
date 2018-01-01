import Vue from 'vue';
import VueRouter from 'vue-router';

import List from './views/List.vue';
import Form from './views/Form.vue';

Vue.use(VueRouter);

export default new VueRouter({
    //mode: 'history',
    base: __dirname,
    routes: [
         { path: '/', component: List, name: 'home' },
         { path: '/add', component: Form },
         { path: '/edit/:id', component: Form, name: 'edit' },
    ]
});