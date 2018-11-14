<template>
    <section>
        <h2>Visual Image Form</h2>
        <mu-text-field fullWidth label="Title" labelFloat v-model="image.title" />
        <mu-text-field fullWidth label="source" labelFloat v-model="image.url" />
        <mu-raised-button label="Submit" class="demo-raised-button" primary v-on:click="handleSubmit" />
    </section>
</template>
<script>
export default {
    data() {
        return {
            image: {
                id: 0,
                title: '',
                url: '',
                visual_id: this.$route.params.id
            }
        };
    },
    methods: {
        handleSubmit() {
            const options = this.image;
            this.$http.post(this.$store.state.api.imageSubmit, options).then(res => {
                if (res.status == 200) {
                    this.$router.push({ path: '/visuals/edit/' + this.image.visual_id });
                }
            });
        }
    }
};
</script>