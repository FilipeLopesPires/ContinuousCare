<template>
    <div class="register-form" >
        <h3 class="mt-120 mb-30 title_color text-center" >Join the ContinuousCare Community!</h3>
        <div class="container col-lg-9 col-md-9 switch-wrap d-flex justify-content-between">
            <p class="col-lg-6 col-md-6">Account type:</p>
            <div v-if="accountTypeChecked" class="row col-lg-8 col-md-8">
                <div class="col-lg-1 col-md-1 primary-switch-inverted">
                    <input type="checkbox" id="primary-switch-inverted" @click="changeAccountType" checked>
                    <label for="primary-switch-inverted"></label>
                </div>
                <p class="col-lg-10 col-md-10">Doctor</p>
            </div>
            <div v-else class="row col-lg-8 col-md-8">
                <div class="col-lg-1 col-md-1 confirm-switch">
                    <input type="checkbox" id="confirm-switch" @click="changeAccountType" checked>
                    <label for="confirm-switch"></label>
                </div>
                <p class="col-lg-10 col-md-10">Regular User</p>
            </div>
        </div>
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
            <!-- Password -->
            <div class="row justify-content-center d-flex align-items-center">
                <div class="mt-10 col-lg-6 col-md-6 single-team " >
                    <input required class="single-input" v-bind="$attrs" v-on="$listeners" v-model="filledform.password" type="password" name="password" placeholder="Password *" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Password *'">
                </div>
                <div class="mt-10 col-lg-6 col-md-6 single-team ">
                    <input required class="single-input" v-bind="$attrs" v-on="$listeners" v-model="filledform.password_confirmation" type="password" name="password_confirmation" placeholder="Confirm Password *" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Confirm Password *'">
                </div>
            </div>
            <!-- Public Health Personal Number & birth_date-->
            <div v-if="!accountTypeChecked" class="row ">
                <div class="input-group-icon mt-10 col-lg-6 col-md-6">
                    <div class="icon ml-15">
                        <i class="fa fa-plus" aria-hidden="true"></i>
                    </div>
                    <input required class="single-input" v-bind="$attrs" v-on="$listeners" v-model="filledform.health_number" type="text" name="health_number" placeholder="Public Health Personal Number *" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Public Health Personal Number *'">
                </div>
                <div class="mt-10 col-lg-6 col-md-6 single-team " >
                    <datepicker placeholder="Date of Birth" v-model="filledform.birth_date" format="dd-MM-yyyy" :disabledDates="this.disabledDates" input-class="input-group-icon single-team single-input justify-content-center d-flex align-items-center"></datepicker>
                </div>
            </div>
            <!-- Weight and Height -->
            <div v-if="!accountTypeChecked" class="row justify-content-center d-flex align-items-center">
                <div class="mt-10 col-lg-6 col-md-6 single-team " >
                    <input class="single-input" v-bind="$attrs" v-on="$listeners" v-model="filledform.weight" type="number" name="weight" placeholder="Weight (kg)" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Weight (kg)'">
                </div>
                <div class="mt-10 col-lg-6 col-md-6 single-team ">
                    <input class="single-input" v-bind="$attrs" v-on="$listeners" v-model="filledform.height" type="number" min="0.10" max="2.50" step="0.10" name="height" placeholder="Height (m)" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Height (m)'">
                </div>
            </div>
            <!-- Aditional Info -->
            <div v-if="!accountTypeChecked" class="mt-10">
                <textarea class="single-textarea" v-bind="$attrs" v-on="$listeners" v-model="filledform.additional_info" placeholder="Additional Information" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Additional Information'"></textarea>
            </div>
            <!-- Company and Specialities -->
            <div v-if="accountTypeChecked" class="row justify-content-center d-flex align-items-center">
                <div class="mt-10 col-lg-6 col-md-6 single-team " >
                    <input class="single-input" v-bind="$attrs" v-on="$listeners" v-model="filledform.company" type="text" name="company" placeholder="Company" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Company'">
                </div>
                <div class="mt-10 col-lg-6 col-md-6 single-team ">
                    <input class="single-input" v-bind="$attrs" v-on="$listeners" v-model="filledform.specialities" type="text" min="10" max="250" name="specialities" placeholder="Specialities" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Specialities'">
                </div>
            </div>
            <!-- Submit -->
            <div class="row justify-content-center d-flex align-items-center">
                <div class="mt-10 col-lg-4 col-md-3 justify-content-center d-flex align-items-center">
                    <button v-if="accountTypeChecked" class="genric-btn primary radius text-uppercase" type="submit">Register</button>
                    <button v-else                    class="genric-btn info    radius text-uppercase" type="submit">Register</button>
                </div>
                <div class="mt-10 col-lg-8 col-md-9">
                    <p class="mt-10">
                        Already have an account? <nuxt-link to="/login">Sign In!</nuxt-link> 
                        <br>* These fields are mandatory
                    </p>
                </div>
            </div>
        </form>
        <div><p></p></div>
    </div>
</template>

<script>
import Datepicker from 'vuejs-datepicker'

export default {
    components: {
        Datepicker,
    },
    data() {
        return {
            accountTypeChecked: false,
            disabledDates: {
                to: new Date(1900, 0, 1),
                from: new Date()
            },
            filledform: {
                first_name: null,
                last_name: null,
                username: null,
                email: null,
                password: null,
                password_confirmation: null,
                
                health_number: null,
                birdthdate: null,
                weight: null,
                height: null,
                additional_info: null,

                company: null,
                specialities: null,
            }
        }
    },
    methods: {
        changeAccountType() {
            if(this.accountTypeChecked) {
                this.accountTypeChecked = false;
            } else {
                this.accountTypeChecked = true;
            }
        },

        async onSubmit() {
            /* Fields Validation */
            if(this.filledform.password != this.filledform.password_confirmation) {
                this.showToast("Password inputs must match!", 2500);
                return;
            }
            if(this.filledform.weight < 0) {
                this.showToast("Do you really weight less than 0kg?", 2500);
                return;
            }
            if(this.filledform.height < 0) {
                this.showToast("Are you really negative centimeters high?", 2500);
                return;
            }

            /* Server Validation */
            var result;
            if(this.accountTypeChecked) {
                result = await this.checkRegistration(this.filledform, 'medic');
            } else {
                result = await this.checkRegistration(this.filledform, 'client');
            }
            if(result) { 
                if(result.status==0){ // registration successful
                    result = await this.checkLogin(this.filledform);
                    if(result) {
                        if(result.status==0){ // login successful
                            var profile = {
                                full_name: this.filledform.first_name + " " + this.filledform.last_name,
                                email: this.filledform.email,
                                health_number: this.filledform.health_number,
                                birth_date: this.filledform.birth_date,
                                weight: this.filledform.weight,
                                height: this.filledform.height,
                                additional_info: this.filledform.additional_info,
                                company: this.filledform.company,
                                specialities: this.filledform.specialities
                            };
                            this.$store.dispatch('setSessionToken', result.data.token);
                            this.$store.dispatch('setProfile', profile);
                            if(this.accountTypeChecked) {
                                this.$store.dispatch('setUserType', 'medic');
                                this.$router.push("/patients");
                            } else {
                                this.$store.dispatch('setUserType', 'client');
                                this.$router.push("/");
                            }
                        } else {
                            // deal with error
                            // this should never happen
                            return;
                        }
                    } else {
                        // deal with error
                        return;
                    }
                } else {
                    // deal with error
                    return;
                }
            } else {
                // deal with error
                return;
            }
        },

        async checkRegistration(filledform, account_type) {
            const config = {
                'type': account_type,
                'name': filledform.first_name + " " + filledform.last_name,
                'username': filledform.username,
                'email': filledform.email,
                'health_number': filledform.health_number,
                'password': filledform.password,
                'birth_date': this.convertDate(filledform.birth_date),
                'weight': this.convertNull(filledform.weight),
                'height': this.convertNull(filledform.height),
                'additional_info': filledform.additional_info,
                'company': filledform.company,
                'specialities': filledform.specialities,
            }
            return await this.$axios.$post("/signup",config)
                        .then(res => {
                            if(res.status != 0) {
                                // warn which registration fields are invalid
                                console.log(res);
                                if(res.status == 1) {
                                    // warn that phpn must be uniuqe
                                }
                                this.showToast("Registration was invalid. Please make sure you fill in the form correctly.", 5000);
                            }
                            return res;
                        })
                        .catch(e => {
                            // unable to register
                            console.log(e);
                            this.showToast("Something went wrong with the registration process. The server might be down at the moment. Please re-submit or try again later.", 7500);
                            return null;
                        });
        },
        async checkLogin(filledform) {
            const config = {
                'username': filledform.username,
                'password': filledform.password
            }
            return await this.$axios.$post("/signin",config)
                        .then(res => {
                            if(res.status != 0) {
                                console.log(res);
                                this.showToast("Something went terribly wrong with the registration process. Please try to login, if it does not work contact us through email.", 7500);
                            }
                            return res;
                        })
                        .catch(e => {
                            console.log(e);
                            // toast
                            return null;
                        });
        },

        convertDate(birth_date) {
            if(birth_date) {
                var dd = birth_date.getDate();
                var mm = birth_date.getMonth() + 1; //January is 0!
                var yyyy = birth_date.getFullYear();

                if (dd < 10) { dd = '0' + dd; } 
                if (mm < 10) { mm = '0' + mm; } 

                return dd + '-' + mm + '-' + yyyy;
            }   
            return null;
        },
        convertNull(field) {
            if(field) {
                return parseFloat(field);
            }
            return null;
        },
        showToast(message, duration) {
            this.$toasted.show(message, {position: 'bottom-center', duration: duration});
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
