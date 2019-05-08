<template>
    <div class="contact-form" >
        <h3 class="mt-10 mb-30 title_color text-center" >Our Information:</h3>
        <p class="mb-50">We are present at Campus Universitário de Santiago, 3810-193 Aveiro.
        <br>You can reach us through phone call +351 123 456 789 or email general_email@continuouscare.com</p>
        <h3 class="mt-10 mb-30 title_color text-center" >Send us an email here:</h3>
        <form class="form-wrap" @submit.prevent="onSubmit">
            <!-- Email -->
            <div class="mt-10">
                <input required class="single-input" v-bind="$attrs" v-on="$listeners" v-model="mail.email" type="email" name="email" placeholder="Email" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Email'">
            </div>
            <!-- Subject -->
            <div class="mt-10">
                <input required class="single-input" v-bind="$attrs" v-on="$listeners" v-model="mail.subject" type="text" name="subject" placeholder="Subject" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Subject'">
            </div>
            <!-- Message -->
            <div class="mt-10">
                <textarea required class="single-textarea" v-bind="$attrs" v-on="$listeners" v-model="mail.message" name="message" placeholder="Your message ..." onfocus="this.placeholder = ''" onblur="this.placeholder = 'Your message ...'"></textarea>
            </div>
            <!-- Submit and Newsletter -->
            <div class="row container">
                <div class="mt-10"> 
                    <button class="genric-btn radius text-uppercase" :class="btn_class" type="submit">Send</button>
                </div>
                <div class="mt-10 ml-15 switch-wrap d-flex justify-content-between">
                    <div class="mr-10 confirm-checkbox">
                        <input type="checkbox" id="confirm-checkbox">
                        <label for="confirm-checkbox"></label>
                    </div>
                    <p>Please send me updates about ContinuousCare</p>
                </div>
            </div>
        </form>
        <div><p></p></div>
    </div>
</template>

<script>

export default {
    components: {

    },
    data() {
        var btn_class = "info";
        if(this.$store.getters.isMedic) {
            btn_class = "primary";
        }
        return {
            btn_class,
            mail: {
                email: null,
                subject: null,
                message: null
            }
        }
    },
    methods: {
        onSubmit() {
            this.$toasted.show('This feature is not yet implemented. We are sorry for the inconvenience :(', 
                {position: 'bottom-center', duration: 4000});
        }, 
    }
};
</script>

<style>
.contact-form {
    margin-top: 10%;
    margin-bottom: 10%;
}
</style>
