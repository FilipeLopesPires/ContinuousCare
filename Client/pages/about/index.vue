<template>
    <div>
        <!--================ HTML Header =================-->
        <HeaderHTML page="About" />

        <body>
            <!--================ Header Menu Area =================-->
            <HeaderMenu activePage="About" />

            <!--================ Banner Area =================-->
            <PageBanner page="About" parent_page="Home" />

            <!--================ Content Area =================-->
            <section class="sample-text-area">
                <div class="container">
                    <h3 class="text-heading title_color">About ContinuousCare</h3>
                    <p class="sample-text">This is a project for the 'Projeto em Informática' subject of the 3rd year of LEI (2018/19).</p>
                    <p class="sample-text">The main purpose of this project is to develop a web information system that allows the integrated collecting and visualization of clinical and environmental data sources related to the daily life of a citizen.</p>
                    <p class="sample-text">The solution must be capable of automatically collecting several types of data, such as weather conditions, air quality indicators, vital signals, geolocalization, etc. On the other side, the application must allow the simplified registration of basic physical and mental health states of a person, such as local pains, depression, anxiety, fatigue, etc.</p>
                </div>
            </section>

            <!--================ Footer Area =================-->
            <PageFooter />
            
        </body>
        <nuxt/>
    </div>
</template>

<script>
import HeaderHTML from '@/components/headers/HeaderHTML.vue'
import HeaderMenu from '@/components/headers/HeaderMenu.vue'
import PageBanner from '@/components/banners/PageBanner.vue'
import PageFooter from '@/components/footers/PageFooter.vue'

export default {
    components: {
        HeaderHTML,
        HeaderMenu,
        PageBanner,
        PageFooter
    }
}
</script>

<style scoped>

</style>
