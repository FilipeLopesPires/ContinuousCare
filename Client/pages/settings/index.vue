<template>
    <div style="overflow-x: none;">
        <body>
            <!--================ Header Menu Area =================-->
            <HeaderMenu activePage="Settings" />

            <!--================ Banner Area =================-->
            <PageBanner parent_page="Home" page="Settings" />
            
            <!--================ Footer Area =================-->
            <PageFooter />
            
        </body>
        <nuxt/>
    </div>
</template>

<script>

export default {
    components: {
        
    },
    head: {
        title: "Settings"
    }
}
</script>

<style scoped>

</style>
