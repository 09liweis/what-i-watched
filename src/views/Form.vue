<template>
    <div class="form">
        <h2>Form</h2>
        <mu-row gutter>
            <mu-col width="100" tablet="50" desktop="25">
                <mu-text-field fullWidth label="Title" labelFloat v-model="visual.title" />
            </mu-col>
            <mu-col width="100" tablet="50" desktop="25">
                <mu-text-field fullWidth label="Original Title" labelFloat v-model="visual.original_title" />
            </mu-col>
            <mu-col width="100" tablet="50" desktop="25">
                <mu-text-field fullWidth label="Douban Id" labelFloat v-model="visual.douban_id" />
            </mu-col>
            <mu-col width="100" tablet="50" desktop="25">
                <mu-text-field fullWidth label="Douban Rating" labelFloat v-model="visual.douban_rating" />
            </mu-col>
        </mu-row>
        <button v-on:click="renderDouban">Get Douban Data</button>
        <mu-row gutter>
            <mu-col width="100" tablet="50" desktop="50">
                <mu-text-field fullWidth label="IMDB ID" labelFloat v-model="visual.imdb_id" />
            </mu-col>
            <mu-col width="100" tablet="50" desktop="50">
                <mu-text-field fullWidth label="IMDB Rating" labelFloat v-model="visual.imdb_rating" />
            </mu-col>
        </mu-row>
        <mu-row>
            <mu-col width="100" tablet="50" desktop="25">
                <mu-text-field fullWidth label="Release Date" labelFloat v-model="visual.release_date" />
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
    </div>
</template>

<script>
    export default {
        data() {
            return {
                visual: {
                    id: 0,
                    title: '',
                    original_title: '',
                    douban_id: '20495023',
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
                    episodes: 0,
                    current_episode: 0,
                    visual_type: 'movie'
                }
            };
        },
        mounted() {
            const id = this.$route.params.id;
            if (typeof id != 'undefined') {
                this.getVisual(id);
            }
        },
        methods: {
            handleSubmit() {
                const options = this.visual;
                this.$http.post('/api/visual/submit', options).then(res => {
                    if (res.status == 200) {
                        this.$router.push({ path: '/' });
                    }
                });
            },
            getVisual(id) {
                this.$http.get('/api/visual/' + id).then(res => {
                    this.visual = res.body.result;
                    console.log(res);
                });
            },
            renderDouban() {
                if (this.visual.douban_id == '') {
                    alert('Empty douban id');
                    return;
                }
                this.$http.jsonp('https://api.douban.com/v2/movie/subject/' + this.visual.douban_id).then(res => {
                    this.getImdbId();
                    console.log(res);
                    const douban = res.body;
                    this.visual.title = douban.title;
                    this.visual.summary = douban.summary;
                    this.visual.poster = douban.images.large;
                    this.visual.douban_rating = douban.rating.average;
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
                this.$http.get('/api/get_imdb_id', options).then(res => {
                    this.visual.imdb_id = res.body.imdb_id;
                    this.renderIMDB();
                }, res => {
                    
                });
            },
            renderIMDB() {
                if (this.visual.imdb_id == '') return;
                const options = {
                    params: {
                        i: this.visual.imdb_id,
                        apikey: 'BanMePlz'
                    }
                };
                this.$http.jsonp('https://www.omdbapi.com/', options).then(res => {
                    console.log(res);
                    this.visual.original_title = res.body.Title;
                    this.visual.imdb_rating = res.body.imdbRating;
                    this.visual.rotten_rating = res.body.Ratings[1].Value.replace('%', '');
                    this.visual.poster = res.body.Poster;
                    this.visual.release_date = res.body.Year;
                });
            }
        }
    };
</script>