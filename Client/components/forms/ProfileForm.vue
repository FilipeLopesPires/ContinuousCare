<template>
    <div class="profile-form" >
        <h1 class="mt-10 mb-30 title_color text-center">Your Profile</h1>
        <form class="form-wrap" @submit.prevent="onSubmit">
            <!-- Account Type -->
            <p v-if="!is_medic" class="title-form-wrap">Account type: Regular User</p>
            <p v-else           class="title-form-wrap">Account type: Doctor</p>
            <!-- First and Last Name -->
            <p class="title-form-wrap">Full Name:</p>
            <div class="row d-flex align-items-center">
                <div class="mt-10 col-lg-12 col-md-12" >
                    <p class="single-input"> {{ filledform.full_name }}* </p>
                </div>
            </div>
            <!-- Email -->
            <p class="title-form-wrap">Email:</p>
            <div class="input-group-icon mt-10">
                <div class="icon">
                    <i class="fa fa-envelope" aria-hidden="true"></i>
                </div>
                <input required class="single-input" v-model="filledform.email" type="email" name="EMAIL" placeholder="Email Address" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Email Address'" > <!-- class="single-input-primary"/"single-input-accent"/"single-input-secondary" -->
            </div>
            <!-- Password -->
            <p class="title-form-wrap">Password:</p>
            <div class="row d-flex ">
                <div class="mt-10 col-lg-6 col-md-6 single-team " >
                    <input class="single-input" v-bind="$attrs" v-on="$listeners" v-model="filledform.password" type="password" name="password" placeholder="Password" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Password'">
                </div>
            </div>
            <p class="title-form-wrap">New Password:</p>
            <div class="row justify-content-center d-flex align-items-center">
                <div class="mt-10 col-lg-6 col-md-6 single-team " >
                    <input class="single-input" v-bind="$attrs" v-on="$listeners" v-model="filledform.new_password" type="password" name="new_password" placeholder="New Password" onfocus="this.placeholder = ''" onblur="this.placeholder = 'New Password'">
                </div>
                <div class="mt-10 col-lg-6 col-md-6 single-team ">
                    <input class="single-input" v-bind="$attrs" v-on="$listeners" v-model="filledform.new_password_confirmation" type="password" name="new_password_confirmation" placeholder="Confirm New Password" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Confirm New Password'">
                </div>
            </div>
            <!-- Public Health Personal Number & Birth Date -->
            <p v-if="!is_medic" class="title-form-wrap">Public Health Personal Number and Birth Date</p>
            <div v-if="!is_medic" class="row ">
                <div class="input-group-icon mt-10 col-lg-6 col-md-6">
                    <div class="icon ml-15">
                        <i class="fa fa-plus" aria-hidden="true"></i>
                    </div>
                    <input required class="single-input" v-bind="$attrs" v-on="$listeners" v-model="filledform.health_number" type="text" name="health_number" placeholder="PHPN" onfocus="this.placeholder = ''" onblur="this.placeholder = 'health_number'">
                </div>
                <div class="mt-10 col-lg-6 col-md-6 single-team " >
                    <datepicker placeholder="Date of Birth" v-model="filledform.birth_date" format="dd-MM-yyyy" :disabledDates="this.disabledDates" input-class="input-group-icon single-team single-input justify-content-center d-flex align-items-center"></datepicker>
                </div>
            </div>
            <!-- Weight and Height -->
            <p v-if="!is_medic" class="title-form-wrap">Weight and Height:</p>
            <div v-if="!is_medic" class="row justify-content-center d-flex align-items-center">
                <div class="mt-10 col-lg-6 col-md-6 single-team " >
                    <input class="single-input" v-bind="$attrs" v-on="$listeners" v-model="filledform.weight" type="number" name="weight" placeholder="Weight (kg)" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Weight (kg)'">
                </div>
                <div class="mt-10 col-lg-6 col-md-6 single-team ">
                    <input class="single-input" v-bind="$attrs" v-on="$listeners" v-model="filledform.height" type="number" min="0.10" max="2.50" step="0.10" name="height" placeholder="Height (m)" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Height (m)'">
                </div>
            </div>
            <!-- Aditional Info -->
            <p v-if="!is_medic" class="title-form-wrap">Aditional Information:</p>
            <div v-if="!is_medic" class="mt-10">
                <textarea class="single-textarea" v-bind="$attrs" v-on="$listeners" v-model="filledform.additional_info" placeholder="Additional Information" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Additional Information'"></textarea>
            </div>
            <!-- Company and Specialities -->
            <p v-if="is_medic" class="title-form-wrap">Company and Specialities:</p>
            <div v-if="is_medic" class="row justify-content-center d-flex align-items-center">
                <div class="mt-10 col-lg-6 col-md-6 single-team " >
                    <input class="single-input" v-bind="$attrs" v-on="$listeners" v-model="filledform.company" type="text" name="company" placeholder="Company" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Company'">
                </div>
                <div class="mt-10 col-lg-6 col-md-6 single-team ">
                    <input class="single-input" v-bind="$attrs" v-on="$listeners" v-model="filledform.specialities" type="text" min="10" max="250" name="specialities" placeholder="Specialities" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Specialities'">
                </div>
            </div>
            <!-- Submit -->
            <div class="row justify-content-center d-flex align-items-center">
                <div class="mt-10 col-lg-8 col-md-9"> </div>
                <div class="mt-10 col-lg-4 col-md-3 justify-content-center d-flex align-items-center">
                    <button class="genric-btn radius text-uppercase" :class="btn_class" type="submit">Update</button>
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
        var is_medic = false;
        var btn_class = "info";
        if(this.$store.getters.isMedic) {
            btn_class = "primary";
            is_medic = true;
        }
        var stored_profile = this.$store.getters.profile;
        return {
            is_medic,
            btn_class,
            disabledDates: {
                to: new Date(1900, 0, 1),
                from: new Date()
            },
            filledform: {
                full_name: stored_profile.full_name,
                email: stored_profile.email,
                password: null,
                new_password: null,
                new_password_confirmation: null,
                
                health_number: stored_profile.health_number,
                birdthdate: stored_profile.birth_date,
                weight: parseFloat(stored_profile.weight),
                height: parseFloat(stored_profile.height),
                additional_info: stored_profile.additional_info,

                company: stored_profile.company,
                specialities: stored_profile.specialities,
            }
        }
    },
    methods: {
        async onSubmit() {
            /* Fields Validation */
            if(this.filledform.new_password) {
                if(this.filledform.new_password != this.filledform.new_password_confirmation) {
                    this.showToast("Password inputs must match!", 2500);
                    return;
                }
            }
            if(this.filledform.weight) {
                if(this.filledform.weight < 0) {
                    this.showToast("Do you really weight less than 0kg?", 2500);
                    return;
                }
            }
            if(this.filledform.height) {
                if(this.filledform.height < 0) {
                    this.showToast("Are you really negative centimeters high?", 2500);
                    return;
                }
            }
            
            /* Server Validation */
            var result = await this. checkUpdateProfile(this.filledform, this.$store.getters.sessionToken);
            if(result) {
                if(result.status==0){
                    var profile;
                    if(this.$store.getters.isMedic) {
                        profile = {
                            full_name: this.filledform.full_name,
                            email: this.filledform.email,
                            health_number: null,
                            birth_date: null,
                            weight: null,
                            height: null,
                            additional_info: null,
                            company: this.filledform.company,
                            specialities: this.filledform.specialities
                        }
                    } else {
                        profile = {
                            full_name: this.filledform.full_name,
                            email: this.filledform.email,
                            health_number: this.filledform.health_number,
                            birth_date: this.filledform.birth_date,
                            weight: this.filledform.weight,
                            height: this.filledform.height,
                            additional_info: this.filledform.additional_info,
                            company: null,
                            specialities: null
                        }
                    }
                    this.$store.dispatch('setProfile', profile);
                    this.$toasted.show("Profile updated with success.", {position: 'bottom-center', duration: duration});
                } else {
                    return;
                }
            } else {
                return;
            }
        },

        /* async checkProfile(AuthToken) {
            const config = {
                headers: {'AuthToken': AuthToken}
            }
            return await this.$axios.$get("/profile",config)
                        .then(res => {
                            if(res.status != 0) {
                                // warn what exactly went wrong inside the server
                                this.showToast("Something went terribly wrong while trying to update information about the user. Please re-submit, if it does not work contact us through email.", 7500);
                            }
                            return res;
                        })
                        .catch(e => {
                            // unable to retrieve profile info
                            this.showToast("Something went wrong while trying to update information about the user. The server might be down at the moment. Please re-submit or try again later.", 7500);
                            return null;
                        });
        }, */

        async checkUpdateProfile(filledform, AuthToken) {
            const config = {
                headers: {'AuthToken': AuthToken, "Content-Type":"application/json"},
                
            }
            var data = {
                'type': this.$store.getters.userType,
                'name': filledform.full_name,
                'email': filledform.email,
                'health_number': filledform.health_number,
                'password': filledform.password,
                'new_password': filledform.new_password,
                'birth_date': this.convertDate(filledform.birth_date),
                'weight': filledform.weight,
                'height': filledform.height,
                'additional_info': filledform.additional_info,
                'company': filledform.company,
                'specialities': filledform.specialities,
            }
            return await this.$axios.$put("/profile", data, config)
                        .then(res => {
                            if(res.status != 0) {
                                if(res.status == 4) {
                                    this.$toasted.show(res.msg, {position: 'bottom-center', duration: 7500});
                                    this.$disconnect()
                                    this.$nextTick(() => { 
                                        this.$store.dispatch('logout'),
                                        this.$router.push("/login")
                                    });
                                }
                                else if (res.status == 1) {
                                    this.showToast(res.msg, 5000);
                                }
                                else {
                                    console.log("Error status", res.status);
                                    console.log("message", res.msg);
                                    this.showToast("Update was invalid. Please make sure you fill in the form correctly.", 5000);
                                }
                            }
                            return res;
                        })
                        .catch(e => {
                            // unable to register
                            console.log(e);
                            this.showToast("Something went wrong with the process. The server might be down at the moment. Please re-submit changes or try again later.", 7500);
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

        showToast(message, duration) {
            this.$toasted.show(message, {position: 'bottom-center', duration: duration});
        }
    }
};
</script>

<style scoped>
.profile-form {
    margin-top: 10%;
    margin-bottom: 12%;
}
.title-form-wrap {
    font-size: 16px;
    font-weight: 600;
    margin-bottom: -12px;
    margin-top: 10px;
}
</style>
