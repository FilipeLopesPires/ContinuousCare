<template>
    <div style="overflow-x: none;">
        <body>
            <!--================ Header Menu Area =================-->
            <HeaderMenu activePage="Patients" />

            <!--================ Banner Area =================-->
            <PageBanner parent_page="Home" page="Patients" />

            <!--================ Permissions Boxes Area ============-->
            <PermissionsDiv />
            
            <!--================ Footer Area =================-->
            <PageFooter />
            
        </body>
        <nuxt/>
    </div>
</template>

<script>
import PermissionsDiv from '@/components/boxes/PermissionsDiv.vue'

export default {
    middleware: ['check-log', 'log'],
    components: {
        PermissionsDiv
    },
    head: {
        title: "Patients"
    }
}
</script>

<style>
</style>
