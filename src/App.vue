<template>
    <div class="container">
        <div class="languages">
            <a v-on:click="changeLang('en')">English</a>
            <a v-on:click="changeLang('zh')">中文</a>
        </div>
        <h1>{{this.$store.state.languages[this.$store.state.lang].title}}</h1>
        <p>This page is built by Vue</p>
        <div class="layout">
            <router-link to="/visuals">Visuals</router-link>
            <router-link to="/visuals/add">Add</router-link>
            <router-view></router-view>
        </div>
        <MusicPlayer></MusicPlayer>
    </div>
</template>
<script>
import MusicPlayer from './views/MusicPlayer.vue';
export default {
    components: {
        MusicPlayer
    },
    data() {
        return {
        };
    },
    methods: {
        changeLang(lang) {
            this.$store.commit('changeLang', lang);
            
        }
    }
};
</script>
<style type="text/css">
html, body{
    background-color: rgb(236, 236, 236);
}
.container {
    background-color: #ffffff;
    margin: auto;
    width: 100%;
    max-width: 1024px;
    padding: 20px;
}
</style>