<template>
    <div id="bookmarks">
        <div class="bookmark" v-for="url in urls">
            <img class="bookmark__icon" :src="url.favicon" />
            <h5 class="bookmark__title"><a class="bookmark__link" target="_blank" v-bind:href="url.link">{{url.title}}</a></h5>
        </div>
    </div>
</template>
<script>
export default {
    name: 'home',
    components: {
        
    },
    data() {
        return {
            urls: []
        };
    },
    mounted() {
        this.getURLs();
    },
    methods: {
        getURLs() {
            this.$http.get('https://favourite-site.herokuapp.com/api/urls').then(res => {
                if (res.status == 200) {
                    this.urls = res.body.urls;
                    console.log(res.body.urls);
                }
            }, res => {
                //error
            });
        }
    }
};
</script>