<template>
    <div>
        <h2>List Visual</h2>
        <mu-row gutter>
            <mu-col v-for="v in list" :key="v.id" desktop="25">
                <mu-card>
                    <mu-card-media :title="v.original_title" subTitle="">
                        <img :src="v.poster" />
                    </mu-card-media>
                    <mu-card-actions>
                        <router-link :to="{ name: 'edit', params: { id: v.id }}">Edit</router-link>
                    </mu-card-actions>
                </mu-card>
            </mu-col>
        </mu-row>
    </div>
</template>
<script>
    export default {
        data() {
            return {
                list: []
            };
        },
        mounted() {
            this.getVisuals();
        },
        methods: {
            getVisuals() {
                this.$http.get('/api/visuals').then(res => {
                    this.list = res.body.results;
                });
            }
        }
    };
</script>