<template>
    <html lang="en">
        <!--================ HTML Header =================-->
        <HeaderHTML />

        <body>
            <!--================ Header Menu Area =================-->
            <HeaderMenu />

            <!--================ Banner Area =================-->
            <PageBanner />
            
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
