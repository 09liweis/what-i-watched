import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

const whatIWatched = 'https://what-i-watched.herokuapp.com/';
// const whatIWatched = 'https://what-i-watched-a09liweis-1.c9users.io/';

const state = {
    urls: [],
    message: 'Hello Vuex',
    api: {
        visualList: whatIWatched + 'api/visuals',
        visualDetail: whatIWatched + 'api/visual/',
        visualSubmit: whatIWatched + 'api/visual/submit',
        visualImdb: whatIWatched + 'api/get_imdb_id',
        visualCheck: whatIWatched + 'api/visual/check',
        increaseEpisode: whatIWatched + 'api/visual/increase_episode',
        songList: whatIWatched + 'api/songs',
        songDetail: whatIWatched + 'api/song/',
        songSubmit: whatIWatched + 'api/song/submit',
        imageList: whatIWatched + 'api/images',
        imageSubmit: whatIWatched + 'api/image/submit'
    },
    admin: window.localStorage.getItem('admin') | false,
    lang: 'en',
    languages: {
        en: {
            title: 'What I Watched'
        },
        zh: {
            title: '我看过啥'
        }
    }
};

const mutations = {
    loginAdmin(state) {
        state.admin = true;
    },
    changeLang(state, lang) {
        state.lang = lang;
    }
};

export default new Vuex.Store({
    state,
    mutations
});