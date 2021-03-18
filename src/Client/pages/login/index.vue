<template>
    <div>
        <body style="overflow-x: none;">
            <!--================ Header Menu Area =================-->
            <HeaderMenu activePage="Login or Register" />

            <!--================ Login Form Area =================-->
            <div class="row m0 justify-content-center align-items-center" >
                <div class="col-lg-6">
                    <div class="whole-wrap">
                        <div class="container">
                            <LoginForm />
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
import LoginForm from '@/components/forms/LoginForm.vue'

export default {
    components: {
        LoginForm
    },
    head: {
        title: "Login"
    }
}
</script>

<style scoped>

</style>