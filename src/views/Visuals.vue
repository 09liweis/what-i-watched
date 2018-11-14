<template>
    <div>
        <h2>I have watched {{list.length}}</h2>
        <mu-circular-progress :size="90" color="red" v-if="list.length == 0"/>
        <div class="filters">
            <mu-checkbox name="type" label="Movie" nativeValue="movie" class="demo-checkbox" v-model="filters" />
            <mu-checkbox name="type" label="Tv" nativeValue="tv" class="demo-checkbox" v-model="filters" />
            <mu-checkbox name="type" label="Not Start" nativeValue="not_start" class="demo-checkbox" v-model="filters" />
        </div>
        <transition-group v-if="list.length > 0" name="visual" class="row" appear>
            <mu-col class="visual" v-for="v in resultVisuals" :key="v.id" desktop="25" tablet="33" width="50">
                <mu-card>
                    <mu-card-media title="" subTitle="">
                        <span class="visual__progress-episodes">{{v.current_episode}} / {{v.episodes}}</span>
                        <span class="visual__status">{{getStatus(v)}}</span>
                        <img class="visual__poster" :src="v.poster" />
                    </mu-card-media>
                    <mu-card-actions>
                        <div class="visual__titles">
                            <h3 class="visual__title">{{v.original_title ? v.original_title : v.title}}</h3>
                        </div>
                        <div class="visual__ratings">
                            <a class="visual__rating link" v-bind:href="getLink(v, 'douban')" target="_blank">
                                <img class="visual__rating icon" src="https://img3.doubanio.com/f/talion/2f3c0bc0f35b031d4535fd993ae3936f4e40e6c8/pics/icon/dou32.png" alt="douban icon" />
                                <span class="visual__rating">{{v.douban_rating}}</span>
                            </a>
                            <a class="visual__rating link" v-if="v.imdb_id" v-bind:href="getLink(v, 'imdb')" target="_blank">
                                <img class="visual__rating icon" src="https://a4.mzstatic.com/us/r30/Purple71/v4/eb/6a/9d/eb6a9d94-4631-194c-3e24-852a06dc4ced/icon175x175.jpeg" alt="imdb icon" />
                                <span class="visual__rating">{{v.imdb_rating}}</span>
                            </a>
                            <a>
                                <img class="visual__rating icon" src="https://vignette.wikia.nocookie.net/greatest-movies/images/1/16/Rotten_Tomatoes_fresh_rating_icon.png/revision/latest?cb=20170918174417" alt="Rotten Tomatoes Icon" />
                                <span class="visual__rating">{{v.rotten_rating}}</span>
                            </a>
                        </div>
                        <div class="visual__progress">
                            <mu-linear-progress mode="determinate" :value="getProgress(v)"/>
                        </div>
                        <div class="visual__action" v-if="admin">
                            <router-link :to="{ name: 'edit', params: { id: v.id }}">Edit</router-link>
                            <a class="visual__increaseepisode" v-if="v.episodes != v.current_episode" v-on:click="increaseEpisode(v.id)">+ 1 ep</a>
                        </div>
                    </mu-card-actions>
                </mu-card>
            </mu-col>
        </transition-group>
    </div>
</template>
<script>
    export default {
        data() {
            return {
                list: [],
                filters: [],
                loading: true,
                admin: window.localStorage.getItem('admin') || false
            };
        },
        computed: {
            resultVisuals() {
                if (this.filters.length != 0) {
                    return this.list.filter((v) => {
                        if (this.filters.indexOf('not_start') != -1) {
                            return v.current_episode == 0;
                        } else {
                            return this.filters.indexOf(v.visual_type) != -1;
                        }
                    });
                } else {
                    return this.list;   
                }
            }
        },
        mounted() {
            this.getVisuals();
        },
        methods: {
            gotoAdmin() {
                window.localStorage.setItem('admin', true);
                this.admin = true;
            },
            increaseEpisode(id) {
                this.$http.get(this.$store.state.api.increaseEpisode + '?id=' + id).then(res => {
                    this.getVisuals();
                });
            },
            getVisuals() {
                this.$http.get(this.$store.state.api.visualList).then(res => {
                    this.list = res.body.results;
                    this.loading = false;
                });
            },
            getLink(v, type) {
                if (type == 'douban') {
                    return 'https://movie.douban.com/subject/' + v.douban_id;
                } else if (type == 'imdb') {
                    if (v.imdb_id) {
                        return 'https://www.imdb.com/title/' + v.imdb_id;   
                    }
                }
            },
            getProgress(v) {
                if (v.current_episode == v.episodes) {
                    return 100;
                }
                return (v.current_episode/v.episodes) * 100;
            },
            getStatus(v) {
                if (v.current_episode == v.episodes) {
                    return 'Done';
                } else if (v.current_episode == 0) {
                    return 'Not Started';
                } else if (v.current_episode < v.episodes) {
                    return 'In Progress';
                }
            }
        }
    };
</script>
<style>
    .visual {
        margin-bottom: 20px;
    }
    .visual__poster {
        border-radius: 4px;
    }
    .visual__title {
        margin: 0 0 10px;
    }
    .visual__rating {
        display: inline-block;
        vertical-align: middle;
    }
    .visual__rating.icon {
        width: 20px;
        height: 20px;
        margin-right: 5px;
    }
    .visual__progress {
        position: relative;
        margin: 15px 0;
    }
    .visual__status {
        position: absolute;
        top: 10px;
        right: 10px;
        background: #FFFFFF;
        color: #000000;
        padding: 5px;
        border-radius: 5px;
    }
    .visual__progress-episodes {
        position: absolute;
        top: 10px;
        left: 10px;
        background: #FFFFFF;
        color: #000000;
        padding: 5px;
        border-radius: 5px;
    }
    .mu-linear-progress-determinate {
        background: #57c263;
    }

    /* moving */
    .visual-move {
        transition: all 600ms ease-in-out 50ms;
    }
    
    /* appearing */
    .visual-enter-active {
        transition: all 300ms ease-out;
        transform: translateX(20%);
    }
    
    /* disappearing */
    .visual-leave-active {
        transition: all 200ms ease-in;
    }
    
    /* appear at / disappear to */
    .visual-enter,
    .visual-leave-to {
        opacity: 0;
        transform: translateX(-20%);
    }
</style>