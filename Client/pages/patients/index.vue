<template>
    <div style="overflow-x: none;">
        <body>
            <!--================ Header Menu Area =================-->
            <HeaderMenu activePage="Patients" />

            <!--================ Banner Area =================-->
            <PageBanner parent_page="Home" page="Patients" />

            <!--================ Permissions Boxes Area ============-->
            <div class="row justify-content-center align-items-center">
                <div class="col-lg-9 col-md-9">
                    <PermissionsDiv />
                </div>
            </div>
            
            <!--================ Footer Area =================-->
            <PageFooter />
            
        </body>
        <nuxt/>
    </div>
</template>

<script>
import PermissionsDiv from '@/components/boxes/PermissionsDiv.vue'

export default {
    middleware: ['check-log', 'log', 'medics-only'],
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
