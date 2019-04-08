<template>
    <nav class="blog-pagination justify-content-center d-flex">
        <ul class="pagination">
            <li class="page-item">
                <a href="#" class="page-link" aria-label="Previous">
                    <span aria-hidden="true">
                        <span class="lnr lnr-chevron-left"></span>
                    </span>
                </a>
            </li>
            <li class="page-item active" @click="switchChart(1)">
                <nuxt-link class="page-link" to="/history">1</nuxt-link>
            </li>
            <li class="page-item" @click="switchChart(2)">
                <nuxt-link class="page-link" to="/history">2</nuxt-link>
            </li>
            <li class="page-item" @click="switchChart(3)">
                <nuxt-link class="page-link" to="/history">3</nuxt-link>
            </li>
            <li class="page-item" @click="switchChart(4)">
                <nuxt-link class="page-link" to="/history">4</nuxt-link>
            </li>
            <li class="page-item" @click="switchChart(5)">
                <nuxt-link class="page-link" to="/history">5</nuxt-link>
            </li>
            <li class="page-item">
                <a href="#" class="page-link" aria-label="Next">
                    <span aria-hidden="true">
                        <span class="lnr lnr-chevron-right"></span>
                    </span>
                </a>
            </li>
        </ul>
    </nav>
</template>

<script>
export default {
    name: 'PaginationBox',
    props: {
        
    },
    methods: {
        switchChart(number) {
            console.log(number);
        }
    },
}
</script>

<style>

</style>
