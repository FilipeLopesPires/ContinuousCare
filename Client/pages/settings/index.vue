<template>
    <div style="overflow-x: none;">
        <body>
            <!--================ Header Menu Area =================-->
            <HeaderMenu activePage="Settings" />

            <!--================ Banner Area =================-->
            <PageBanner parent_page="Home" page="Settings" />

            <!--================ Profile Area =================-->
            <div class="row m0 justify-content-center align-items-center" >
                <div class="col-lg-6">
                    <div class="whole-wrap">
                        <div class="container">
                            <ProfileForm />
                        </div>
                    </div>
                </div>
            </div>
            
            <!--================ Footer Area =================-->
            <PageFooter />
            
        </body>
        <nuxt/>
    </div>
</template>

<script>
import ProfileForm from '@/components/forms/ProfileForm.vue'

export default {
    components: {
        ProfileForm
    },
    middleware: ['check-log', 'log'],
    head: {
        title: "Settings"
    }
}
</script>

<style scoped>

</style>
