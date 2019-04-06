<template>
    <div class="register-form" >
        <h3 class="mt-120 mb-30 title_color text-center" >Join the ContinuousCare Community!</h3>
        <form class="form-wrap" @submit.prevent="onSubmit">
            <!-- First and Last Name -->
            <div class="row justify-content-center d-flex align-items-center">
                <div class="mt-10 col-lg-6 col-md-6 single-team " >
                    <input required class="single-input" v-bind="$attrs" v-on="$listeners" v-model="filledform.first_name" type="text" name="first_name" placeholder="First Name *" onfocus="this.placeholder = ''" onblur="this.placeholder = 'First Name *'">
                </div>
                <div class="mt-10 col-lg-6 col-md-6 single-team ">
                    <input required class="single-input" v-bind="$attrs" v-on="$listeners" v-model="filledform.last_name" type="text" name="last_name" placeholder="Last Name *" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Last Name *'">
                </div>
            </div>
            <!-- Username -->
            <div class="input-group-icon mt-10">
                <div class="icon">
                    <i class="fa fa-user" aria-hidden="true"></i>
                </div>
                <input required class="single-input" v-bind="$attrs" v-on="$listeners" v-model="filledform.username" type="text" name="username" placeholder="Username *" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Username *'">
            </div>
            <!-- Email -->
            <div class="input-group-icon mt-10">
                <div class="icon">
                    <i class="fa fa-envelope" aria-hidden="true"></i>
                </div>
                <input required class="single-input" v-bind="$attrs" v-on="$listeners" v-model="filledform.email" type="email" name="EMAIL" placeholder="Email Address *" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Email Address *'" > <!-- class="single-input-primary"/"single-input-accent"/"single-input-secondary" -->
            </div>
            <!-- Public Health Personal Number -->
            <div class="input-group-icon mt-10">
                <div class="icon">
                    <i class="fa fa-plus" aria-hidden="true"></i>
                </div>
                <input required class="single-input" v-bind="$attrs" v-on="$listeners" v-model="filledform.phpn" type="text" name="phpn" placeholder="Public Health Personal Number *" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Public Health Personal Number *'">
            </div>
            <!-- Password -->
            <div class="row justify-content-center d-flex align-items-center">
                <div class="mt-10 col-lg-6 col-md-6 single-team " >
                    <input required class="single-input" v-bind="$attrs" v-on="$listeners" v-model="filledform.password" type="password" name="password" placeholder="Password *" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Password *'">
                </div>
                <div class="mt-10 col-lg-6 col-md-6 single-team ">
                    <input required class="single-input" v-bind="$attrs" v-on="$listeners" v-model="filledform.password_confirmation" type="password" name="password_confirmation" placeholder="Confirm Password *" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Confirm Password *'">
                </div>
            </div>
            
            <!-- Birthdate -->
            <div class="input-group-icon mt-10 single-team single-input justify-content-center d-flex align-items-center">
                <p class="mt-10">Date of Birth </p> 
                <!-- <DatePicker v-bind="$attrs" v-on="$listeners" v-model="filledform.birthdate" /> -->
                <datepicker v-bind="$attrs" v-on="$listeners" :value="filledform.birthdate" format="DD-MM-YYYY" name="birthdate" placeholder="Date of Birth"></datepicker>
                
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
            <!-- Weight and Height -->
            <div class="row justify-content-center d-flex align-items-center">
                <div class="mt-10 col-lg-6 col-md-6 single-team " >
                    <input class="single-input" v-bind="$attrs" v-on="$listeners" v-model="filledform.weight" type="text" name="weight" placeholder="Weight" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Weight'">
                </div>
                <div class="mt-10 col-lg-6 col-md-6 single-team ">
                    <input class="single-input" v-bind="$attrs" v-on="$listeners" v-model="filledform.height" type="text" name="height" placeholder="Height" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Height'">
                </div>
            </div>
            <!-- Aditional Info -->
            <div class="mt-10">
                <textarea class="single-textarea" v-bind="$attrs" v-on="$listeners" v-model="filledform.aditional_info" placeholder="Aditional Information" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Aditional Information'"></textarea>
            </div>
            <!-- Submit -->
            <div class="row justify-content-center d-flex align-items-center">
                <div class="mt-10 col-lg-4 col-md-3">
                    <button class="main_btn text-uppercase" type="submit">Register</button>
                </div>
                <div class="mt-10 col-lg-8 col-md-9">
                    <p>Already have an account? <nuxt-link to="" @click="logMeIn">Sign In!</nuxt-link> </p> 
                    <p>I forgot my password <nuxt-link to="" @click="forgotMyPassword">Help!</nuxt-link> </p> 
                </div>
            </div>
        </form>
        <div><p></p></div>
    </div>
</template>

<script>
/* import DatePicker from '@/components/forms/DatePicker.vue'; */
import datepicker from 'vue-date-picker'

export default {
    components: {
        /* DatePicker */
        datepicker
    },
    data() {
        return {
            filledform: {
                first_name: "",
                last_name: "",
                username: "",
                email: "",
                phpn: "",
                password: "",
                password_confirmation: "",
                birdthdate: new Date,
                weight: "",
                height: "",
                aditional_info: ""
            }
        }
    },
    methods: {
        onSubmit() {
            console.log(this.filledform);
        },
        logMeIn() {
            console.log("change to login form");
        },
        forgotMyPassword() {
            console.log("ask for email");
        }
    }
};
</script>

<style>
.register-form {
    margin-top: 25%;
    margin-bottom: 15%;
}
</style>
