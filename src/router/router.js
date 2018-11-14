import Vue from 'vue';
import VueRouter from 'vue-router';

import Home from '../views/Home.vue';
import Urls from '../views/Urls.vue';
import Visuals from '../views/Visuals.vue';
import VisualForm from '../views/VisualForm.vue';

import SongForm from '../views/SongForm.vue';
import ImageForm from '../views/ImageForm.vue';

Vue.use(VueRouter);

export default new VueRouter({
    //mode: 'history',
    base: __dirname,
    routes: [
         { path: '/', component: Home },
         { path: '/page', component: Urls },
         { path: '/visuals', component: Visuals, name: 'home' },
         { path: '/visuals/add', component: VisualForm },
         { path: '/visuals/edit/:id', component: VisualForm, name: 'edit' },
         
         { path: '/visuals/:id/song/add', component: SongForm, name: 'addSong' },
         { path: '/song/:songId/edit', component: SongForm, name: 'editSong' },
         
         { path: '/visuals/:id/image/add', component: ImageForm, name: 'addImage'}
    ]
});