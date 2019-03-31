<template>
    <div>
        <!--================ HTML Header =================-->
        <HeaderHTML page="Devices" />

        <body>
            <!--================ Header Menu Area =================-->
            <HeaderMenu />

            <!--================ Banner Area =================-->
            <PageBanner parent_page="Home" page="Devices" />
            
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