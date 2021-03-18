<template>
    <div>
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
import RegisterForm from '@/components/forms/RegisterForm.vue'

export default {
    components: {
        RegisterForm
    },
    head: {
        title: "Register"
    }
}
</script>

<style scoped>

</style>