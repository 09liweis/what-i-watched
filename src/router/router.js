import Vue from 'vue';
import VueRouter from 'vue-router';

import Visuals from '../views/Visuals.vue';
import VisualForm from '../views/VisualForm.vue';

import SongForm from '../views/SongForm.vue';
import ImageForm from '../views/ImageForm.vue';

Vue.use(VueRouter);

export default new VueRouter({
    //mode: 'history',
    base: __dirname,
    routes: [
         { path: '/', component: Visuals, name: 'home' },
         { path: '/add', component: VisualForm },
         { path: '/edit/:id', component: VisualForm, name: 'edit' },
         
         { path: '/:id/song/add', component: SongForm, name: 'addSong' },
         { path: '/song/:songId/edit', component: SongForm, name: 'editSong' },
         
         { path: '/:id/image/add', component: ImageForm, name: 'addImage'}
    ]
});