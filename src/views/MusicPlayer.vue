<template>
    <div id="player" v-bind:class="{opened: open}">
        <div id="player__toggle" v-on:click="toggle()"></div>
        <mu-list>
            <mu-list-item v-for="s in songs" v-bind:title="s.title" key="s.id" v-on:click="selectSong(s)">
                <mu-avatar v-bind:src="s.image" slot="rightAvatar"/>
            </mu-list-item>
        </mu-list>
        <audio ref="player" controls v-if="song.url">
            <source :src="song.url" type="audio/mpeg" />
        </audio>
    </div>
</template>
<script>
export default {
    name: 'MusicPlayer',
    data() {
        return {
            open: true,
            song: {
                url: '',
                image: '',
                title: '',
                artist: ''
            },
            songs: []
        };
    },
    mounted() {
        this.open = window.localStorage.getItem('musicPlayerShow') == 'true';
        this.getSongs();
        // this.$refs.player.addEventListener("ended", function(){
        //     console.log("ended");
        // });
    },
    methods: {
        toggle() {
            this.open = !this.open;
            window.localStorage.setItem('musicPlayerShow', this.open);
        },
        getSongs() {
            this.$http.get(this.$store.state.api.songList).then((res) => {
                this.songs = res.body.results;
                this.song = this.songs[0];
            });
        },
        selectSong(s) {
            this.song = s;
            this.$refs.player.load();
            this.$refs.player.play();
        }
    }
};
</script>
<style>
#player {
    position: fixed;
    right: 0;
    bottom: 0;
    padding: 10px;
    background-color: #ffffff;
    border: 1px solid #cccccc;
    transition: all 0.4s ease;
    transform: translateX(322px);
}
#player.opened {
    transform: translateX(0);
}
#player__toggle {
    position: absolute;
    width: 20px;
    height: 40px;
    background-color: #cccccc;
    top: 50%;
    left: -20px;
    cursor: pointer;
}
</style>