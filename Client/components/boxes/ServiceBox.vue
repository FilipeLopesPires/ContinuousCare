<template>
    <div class="col-lg-3 col-md-6">
        <div class="single_service">
            <span :class="icon"></span> <!-- "lnr lnr-rocket","lnr lnr-bug","lnr lnr-users",etc. -->
            <nuxt-link to="/">
                <h4>{{ title1 }} <br> {{ title2 }}</h4>
            </nuxt-link>
            <p>{{ description }}</p>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ServiceBox',
    props: {
        icon: {
            type: String,
            required: true
        },
        title1: {
            type: String,
            required: true
        },
        title2: {
            type: String,
            required: true
        },
        description: {
            type: String,
            required: true
        }
    }
}
</script>

<style>

</style>
