<template>
    <div class="form">
        <h2>Form</h2>
        <mu-raised-button label="Add Image" class="demo-raised-button" primary v-on:click="gotoAddImage()" />
        
        <mu-raised-button slot="actions" flat color="primary" @click="toggleSearch" v-if="visual.id == 0">Search on Douban</mu-raised-button>
        <mu-dialog title="Dialog" width="360" scrollable :open.sync="searchOpen">
            <mu-text-field fullWidth label="Search From Douban" labelFloat v-on:change="searchDouban" />
            <mu-list>
                <mu-list-item v-for="s in searchs" v-bind:title="s.title" key="s.id" v-on:click="renderFromSearch(s.id)">
                    <mu-avatar v-bind:src="s.images.large" slot="rightAvatar"/>
                </mu-list-item>
            </mu-list>
            <mu-raised-button slot="actions" flat color="primary" @click="toggleSearch">Close</mu-raised-button>
        </mu-dialog>
        <mu-row gutter>
            <mu-col width="100" tablet="50" desktop="25">
                <mu-text-field fullWidth label="Title" labelFloat v-model="visual.title" />
            </mu-col>
            <mu-col width="100" tablet="50" desktop="25">
                <mu-text-field fullWidth label="Original Title" labelFloat v-model="visual.original_title" />
            </mu-col>
            <mu-col width="100" tablet="50" desktop="25">
                <mu-text-field fullWidth label="Douban Id" labelFloat v-model="visual.douban_id" v-on:change="renderDouban" />
            </mu-col>
            <mu-col width="100" tablet="50" desktop="25">
                <mu-text-field fullWidth label="Douban Rating" labelFloat v-model="visual.douban_rating" />
            </mu-col>
        </mu-row>
        <mu-raised-button label="Get Douban Data" class="demo-raised-button" v-on:click="renderDouban" secondary/>
        <mu-row gutter>
            <mu-col width="100" tablet="50" desktop="25">
                <mu-text-field fullWidth label="IMDB ID" labelFloat v-model="visual.imdb_id" v-on:change="renderIMDB" />
            </mu-col>
            <mu-col width="100" tablet="50" desktop="25">
                <mu-text-field fullWidth label="IMDB Rating" labelFloat v-model="visual.imdb_rating" />
            </mu-col>
            <mu-col width="100" tablet="50" desktop="25">
                <mu-text-field fullWidth label="Episodes" labelFloat v-model="visual.episodes" />
            </mu-col>
            <mu-col width="100" tablet="50" desktop="25">
                <mu-text-field fullWidth label="Current Episode" labelFloat v-model="visual.current_episode" />
            </mu-col>
        </mu-row>
        <mu-raised-button label="Get IMDB Data" class="demo-raised-button" v-on:click="renderIMDB" secondary/>
        <mu-row>
            <mu-col width="100" tablet="50" desktop="25">
                <!--<mu-text-field fullWidth label="Release Date" labelFloat v-model="visual.release_date" />-->
                <mu-select-field label="Release Date" readonly v-model="visual.release_date" full-width>
                    <mu-menu-item v-for="release_date in release_dates" :key="release_date" :label="release_date" :value="release_date.substring(0, 10)" :title="release_date"></mu-menu-item>
                </mu-select-field>
            </mu-col>
            <mu-col width="100" tablet="50" desktop="25">
                <mu-text-field fullWidth label="Poster" labelFloat v-model="visual.poster" />
            </mu-col>
            <mu-col width="100" tablet="50" desktop="25">
                <mu-select-field fullWidth v-model="visual.visual_type" label="Visual Type">
                    <mu-menu-item value="movie" title="Movie"/>
                    <mu-menu-item value="tv" title="Tv" />
                </mu-select-field>
            </mu-col>
        </mu-row>
        <div class="form-group">
            <mu-text-field fullWidth label="Summary" multiLine :rows="3" :rowsMax="6" labelFloat v-model="visual.summary" />
        </div>
        <mu-raised-button label="Submit" class="demo-raised-button" primary v-on:click="handleSubmit" />
        
        <div class="songs">
            <mu-raised-button label="Add Song" class="demo-raised-button" primary v-on:click="gotoAddSong()" />
            <mu-list>
                <mu-list-item v-for="s in songs" v-bind:title="s.title" key="s.id" v-on:click="editSong(s)">
                    <mu-avatar v-bind:src="s.image" slot="rightAvatar"/>
                </mu-list-item>
            </mu-list>
        </div>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                searchOpen: false,
                searchs: [],
                visual: {
                    id: 0,
                    title: '',
                    original_title: '',
                    douban_id: '',
                    douban_rating: '0.0',
                    imdb_id: '',
                    imdb_rating: '0.0',
                    rotten_id: '',
                    rotten_rating: 0,
                    rotten_audience_rating: 0,
                    release_date: '',
                    poster: '',
                    summary: '',
                    online_source: '',
                    episodes: 1,
                    current_episode: 0,
                    visual_type: 'movie'
                },
                release_dates: [],
                songs: []
            };
        },
        mounted() {
            const id = this.$route.params.id;
            if (typeof id != 'undefined') {
                this.getVisual(id);
                this.getSongs(id);
            }
        },
        methods: {
            toggleSearch() {
                this.searchOpen = !this.searchOpen;
            },
            gotoAddSong() {
                this.$router.push({path: '/visuals/' + this.$route.params.id + '/song/add'});
            },
            gotoAddImage() {
                this.$router.push({path: '/visuals/' + this.$route.params.id + '/image/add'});
            },
            renderFromSearch(id) {
                this.toggleSearch();
                this.visual.douban_id = id;
                this.renderDouban();
            },
            handleSubmit() {
                const options = this.visual;
                this.$http.post(this.$store.state.api.visualSubmit, options).then(res => {
                    if (res.status == 200) {
                        this.$router.push({ path: '/visuals' });
                    }
                });
            },
            getVisual(id) {
                this.$http.get(this.$store.state.api.visualDetail + id).then(res => {
                    this.visual = res.body.result;
                });
            },
            searchDouban(e) {
                const val = e.target.value;
                this.$http.jsonp('https://api.douban.com/v2/movie/search?q=' + val).then(res => {
                    this.searchs = [];
                    if (res.status == 200) {
                        this.searchs = res.body.subjects;
                    }
                });
            },
            renderDouban() {
                if (this.visual.douban_id == '') {
                    alert('Empty douban id');
                    return;
                }
                this.getImdbId();
                this.$http.jsonp('https://api.douban.com/v2/movie/subject/' + this.visual.douban_id).then(res => {
                    const douban = res.body;
                    if (this.visual.summary == '') {
                        this.visual.summary = douban.summary;
                    }
                    this.visual.title = douban.title;
                    this.visual.poster = douban.images.large;
                    this.visual.douban_rating = douban.rating.average;
                    if (douban.episodes_count) {
                        this.visual.episodes = douban.episodes_count;
                        this.visual.visual_type = 'tv';
                    }
                }, res => {
                    //error
                });
            },
            getImdbId() {
                const options = {
                    params: {
                        douban_id: this.visual.douban_id
                    }
                };
                this.$http.get(this.$store.state.api.visualImdb, options).then(res => {
                    this.visual.imdb_id = res.body.imdb_id;
                    this.release_dates = res.body.release_dates;
                    this.renderIMDB();
                }, res => {
                    
                });
            },
            renderIMDB() {
                if (this.visual.imdb_id == '') return;
                const options = {
                    params: {
                        i: this.visual.imdb_id,
                        apikey: '6ad10fa5'
                    }
                };
                this.$http.jsonp('https://www.omdbapi.com/', options).then(res => {
                    if (res.body.Response != 'False') {
                        this.visual.original_title = res.body.Title;
                        this.visual.imdb_rating = res.body.imdbRating;
                        if (res.body.Ratings[1] && res.body.Ratings[1].Source == 'Rotten Tomatoes') {
                            this.visual.rotten_rating = res.body.Ratings[1].Value.replace('%', '');   
                        }
                        this.visual.poster = res.body.Poster;
                    }
                });
            },
            getSongs(visual_id) {
                this.$http.get(this.$store.state.api.songList + '?visual_id=' + visual_id).then((res) => {
                    if (res.status == 200) {
                        this.songs = res.body.results;
                    }
                });
            },
            editSong(s) {
                let visual_id = this.$route.params.id;
                this.$router.push({ path: '/song/' + s.id + '/edit' });
            }
        }
    };
</script>