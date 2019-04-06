<template>
    <div>
        <!--================ HTML Header =================-->
        <HeaderHTML page="Register" />

        <body style="overflow-x: none;">
            <!--================ Header Menu Area =================-->
            <HeaderMenu activePage="Login or Register" />

            <!--================ Register Form Area =================-->
            
            <div class="row m0 justify-content-center align-items-center" >
                <div class="col-lg-6">
                    <div class="whole-wrap">
                        <div class="container">
                            <RegisterForm />
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
import HeaderHTML from '@/components/headers/HeaderHTML.vue'
import HeaderMenu from '@/components/headers/HeaderMenu.vue'
import PageBanner from '@/components/banners/PageBanner.vue'
import PageFooter from '@/components/footers/PageFooter.vue'
import RegisterForm from '@/components/forms/RegisterForm.vue'

export default {
    components: {
        HeaderHTML,
        HeaderMenu,
        PageBanner,
        PageFooter,
        RegisterForm
    }
}
</script>

<style scoped>

</style>