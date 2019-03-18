<template>
    <html lang="en">
        <!--================ HTML Header =================-->
        <HeaderHTML />

        <body>
            <!--================ Header Menu Area =================-->
            <HeaderMenu />

            <!--================ Banner Area =================-->
            <PageBanner />

            <!--================ Testing Area =================-->
            <div class="testing">
                <h1>About ContinuousCare</h1>
                <p>This is a project for the 'Projeto em Informática' subject of the 3rd year of LEI (2018/19).</p>
                <p>The main purpose of this project is to develop a web information system that allows the integrated collecting and visualization of clinical and environmental data sources related to the daily life of a citizen.</p>
                <p>The solution must be capable of automatically collecting several types of data, such as weather conditions, air quality indicators, vital signals, geolocalization, etc. On the other side, the application must allow the simplified registration of basic physical and mental health states of a person, such as local pains, depression, anxiety, fatigue, etc.</p>
            </div>

            <!--================ Footer Area =================-->
            <PageFooter />
            
        </body>
        <nuxt/>
    </html>
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
