<template>
    <div>
        <body>
            <!--================ Header Menu Area =================-->
            <HeaderMenu activePage="Contact" />

            <!--================ Banner Area =================-->
            <PageBanner parent_page="Home" page="Contact Us" />

            <!--================ Contact Form Area =================-->
            <div class="row justify-content-center align-items-center" >
                <div class="col-lg-6 col-md-6">
                    <div class="whole-wrap">
                        <div class="container">
                            <ContactForm />
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
import ContactForm from '@/components/forms/ContactForm.vue'

export default {
    components: {
        ContactForm,
    },
    head: {
        title: "Contact"
    }
}
</script>

<style scoped>

</style>
