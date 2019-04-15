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
    middleware: ['check-log', 'log'],
    components: {
        
    },
    head: {
        title: "Settings"
    }
}
</script>

<style scoped>

</style>
