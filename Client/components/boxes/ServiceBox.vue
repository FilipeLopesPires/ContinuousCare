<template>
    <div class="col-lg-3 col-md-6">
        <div class="single_service">
            <span :class="icon"></span> <!-- "lnr lnr-rocket","lnr lnr-bug","lnr lnr-users",etc. -->
            <a href="#">
                <h4>{{ title }}</h4>
            </a>
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
        title: {
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
