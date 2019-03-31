<template>
    <div class="register-form">
        <h3 class="mt-120 mb-30 title_color text-center">Join the ContinuousCare Community!</h3>
        <form class="form-wrap" action="#">
            <div class="row justify-content-center d-flex align-items-center">
                <div class="mt-10 col-lg-6 col-md-6 single-team " >
                    <input type="text" name="first_name" placeholder="First Name *" onfocus="this.placeholder = ''" onblur="this.placeholder = 'First Name *'"
                    required class="single-input">
                </div>
                <div class="mt-10 col-lg-6 col-md-6 single-team ">
                    <input type="text" name="last_name" placeholder="Last Name *" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Last Name *'"
                    required class="single-input">
                </div>
            </div>
            <div class="input-group-icon mt-10">
                <div class="icon">
                    <i class="fa fa-user" aria-hidden="true"></i>
                </div>
                <input type="text" name="username" placeholder="Username *" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Username *'"
                    required class="single-input">
            </div>
            <div class="input-group-icon mt-10">
                <div class="icon">
                    <i class="fa fa-envelope" aria-hidden="true"></i>
                </div>
                <input type="email" name="EMAIL" placeholder="Email Address *" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Email Address *'"
                required class="single-input"> <!-- class="single-input-primary"/"single-input-accent"/"single-input-secondary" -->
            </div>
            <div class="input-group-icon mt-10">
                <div class="icon">
                    <i class="fa fa-plus" aria-hidden="true"></i>
                </div>
                <input type="text" name="phpn" placeholder="Public Health Personal Number *" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Public Health Personal Number *'"
                    required class="single-input">
            </div>
            <div class="row justify-content-center d-flex align-items-center">
                <div class="mt-10 col-lg-6 col-md-6 single-team " >
                    <input type="password" name="password" placeholder="Password *" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Password *'"
                    required class="single-input">
                </div>
                <div class="mt-10 col-lg-6 col-md-6 single-team ">
                    <input type="password" name="password_confirmation" placeholder="Confirm Password *" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Confirm Password *'"
                    required class="single-input">
                </div>
            </div>
            
            <div class="input-group-icon mt-10 single-team single-input justify-content-center d-flex align-items-center">
                <p class="mt-10">Date of Birth * </p> 
                <DatePicker />
            </div>
            
            <!-- <div class="appointment-area appointment-right input-group-icon mt-10">
                <div class="icon">
                    <i class="fa fa-plane" aria-hidden="true"></i>
                </div>
                <div class="form-select" id="default-select">
                    <div class="nice-select open" tabindex="0">
                        <span class="current">City *</span>
                        <ul class="list">
                            <li data-value="City" class="option selected focus">Disease Type</li>
                            <li data-value="1" class="option">Type One</li>
                            <li data-value="2" class="option">Type Two</li>
                            <li data-value="3" class="option">Type Three</li>
                            <li data-value="4" class="option">Type Four</li
                        ></ul>
                    </div>
                </div>
            </div> -->
            <div class="row justify-content-center d-flex align-items-center">
                <div class="mt-10 col-lg-6 col-md-6 single-team " >
                    <input type="text" name="weight" placeholder="Weight *" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Weight *'"
                    required class="single-input">
                </div>
                <div class="mt-10 col-lg-6 col-md-6 single-team ">
                    <input type="text" name="height" placeholder="Height *" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Height*'"
                    required class="single-input">
                </div>
            </div>
            <div class="mt-10">
                <textarea class="single-textarea" placeholder="Aditional Information" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Aditional Information'"></textarea>
            </div>
            <div class="row justify-content-center d-flex align-items-center">
                <div class="mt-10 col-lg-4 col-md-3">
                    <button class="main_btn text-uppercase">Register</button>
                </div>
                <div class="mt-10 col-lg-8 col-md-9">
                    <p>Already have an account? <nuxt-link to="#">Sign In!</nuxt-link> </p> 
                </div>
            </div>
        </form>
        <div><p></p></div>
    </div>
</template>

<script>
import DatePicker from '@/components/forms/DatePicker.vue';

export default {
    components: {
        DatePicker
    },
};
</script>

<style>

</style>
