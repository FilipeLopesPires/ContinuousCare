<template>
    <div>
        <body>
            <!--================ Header Menu Area =================-->
            <HeaderMenu activePage="Help" />

            <!--================ Banner Area =================-->
            <PageBanner parent_page="Home" page="Contact Us" />
            
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
        title: "Contact"
    }
}
</script>

<style scoped>

</style>
