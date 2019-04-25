<template>
    <div class="register-form" >
        <h1 class="mt-120 mb-30 title_color text-center" >My Profile</h1>
        <form class="form-wrap" @submit.prevent="onSubmit">
            <!-- Account Type -->
            <p v-if="accountTypeChecked" class="title-form-wrap">Account type: Regular User</p>
            <p v-else class="title-form-wrap">Account type: Doctor</p>
            <!-- First and Last Name -->
            <p class="title-form-wrap">Name:</p>
            <div class="row justify-content-center d-flex align-items-center">
                <div class="mt-10 col-lg-6 col-md-6 single-team " >
                    <input required class="single-input" v-bind="$attrs" v-on="$listeners" v-model="filledform.first_name" type="text" name="first_name" placeholder="First Name" onfocus="this.placeholder = ''" onblur="this.placeholder = 'First Name'">
                </div>
                <div class="mt-10 col-lg-6 col-md-6 single-team ">
                    <input required class="single-input" v-bind="$attrs" v-on="$listeners" v-model="filledform.last_name" type="text" name="last_name" placeholder="Last Name" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Last Name'">
                </div>
            </div>
            <!-- Username -->
            <p class="title-form-wrap">Username:</p>
            <div class="input-group-icon mt-10">
                <div class="icon">
                    <i class="fa fa-user" aria-hidden="true"></i>
                </div>
                <input required class="single-input" v-bind="$attrs" v-on="$listeners" v-model="filledform.username" type="text" name="username" placeholder="Username" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Username'">
            </div>
            <!-- Email -->
            <p class="title-form-wrap">Email:</p>
            <div class="input-group-icon mt-10">
                <div class="icon">
                    <i class="fa fa-envelope" aria-hidden="true"></i>
                </div>
                <input required class="single-input" v-bind="$attrs" v-on="$listeners" v-model="filledform.email" type="email" name="EMAIL" placeholder="Email Address" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Email Address'" > <!-- class="single-input-primary"/"single-input-accent"/"single-input-secondary" -->
            </div>
            <!-- Password -->
            <p class="title-form-wrap">Password:</p>
            <div class="row d-flex ">
                <div class="mt-10 col-lg-6 col-md-6 single-team " >
                    <input required class="single-input" v-bind="$attrs" v-on="$listeners" v-model="filledform.password" type="password" name="password" placeholder="Password" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Password'">
                </div>
            </div>
            <p class="title-form-wrap">New Password:</p>
            <div class="row justify-content-center d-flex align-items-center">
                <div class="mt-10 col-lg-6 col-md-6 single-team " >
                    <input required class="single-input" v-bind="$attrs" v-on="$listeners" v-model="filledform.new_password" type="password" name="new_password" placeholder="New Password" onfocus="this.placeholder = ''" onblur="this.placeholder = 'New Password'">
                </div>
                <div class="mt-10 col-lg-6 col-md-6 single-team ">
                    <input required class="single-input" v-bind="$attrs" v-on="$listeners" v-model="filledform.new_password_confirmation" type="password" name="new_password_confirmation" placeholder="Confirm New Password" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Confirm New Password'">
                </div>
            </div>
            <!-- Public Health Personal Number & Birthdate-->
            <p v-if="!accountTypeChecked" class="title-form-wrap">Public Health Personal Number and Birthdate</p>
            <div v-if="!accountTypeChecked" class="row ">
                <div class="input-group-icon mt-10 col-lg-6 col-md-6">
                    <div class="icon ml-15">
                        <i class="fa fa-plus" aria-hidden="true"></i>
                    </div>
                    <input required class="single-input" v-bind="$attrs" v-on="$listeners" v-model="filledform.phpn" type="text" name="phpn" placeholder="PHPN" onfocus="this.placeholder = ''" onblur="this.placeholder = 'PHPN'">
                </div>
                <div class="mt-10 col-lg-6 col-md-6 single-team " >
                    <datepicker placeholder="Date of Birth" v-model="filledform.birthdate" format="dd-MM-yyyy" :disabledDates="this.disabledDates" input-class="input-group-icon single-team single-input justify-content-center d-flex align-items-center"></datepicker>
                </div>
            </div>
            <!-- Weight and Height -->
            <p v-if="!accountTypeChecked" class="title-form-wrap">Weight and Height:</p>
            <div v-if="!accountTypeChecked" class="row justify-content-center d-flex align-items-center">
                <div class="mt-10 col-lg-6 col-md-6 single-team " >
                    <input class="single-input" v-bind="$attrs" v-on="$listeners" v-model="filledform.weight" type="number" name="weight" placeholder="Weight (kg)" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Weight (kg)'">
                </div>
                <div class="mt-10 col-lg-6 col-md-6 single-team ">
                    <input class="single-input" v-bind="$attrs" v-on="$listeners" v-model="filledform.height" type="number" min="0.10" max="2.50" step="0.10" name="height" placeholder="Height (m)" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Height (m)'">
                </div>
            </div>
            <!-- Aditional Info -->
            <p v-if="!accountTypeChecked" class="title-form-wrap">Aditional Information:</p>
            <div v-if="!accountTypeChecked" class="mt-10">
                <textarea class="single-textarea" v-bind="$attrs" v-on="$listeners" v-model="filledform.additional_info" placeholder="Additional Information" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Additional Information'"></textarea>
            </div>
            <!-- Company and Specialities -->
            <p v-if="accountTypeChecked" class="title-form-wrap">Company and Specialities:</p>
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
                <div class="mt-10 col-lg-8 col-md-9"> </div>
                <div class="mt-10 col-lg-4 col-md-3 justify-content-center d-flex align-items-center">
                    <button v-if="accountTypeChecked" class="genric-btn primary radius text-uppercase" type="submit">Update</button>
                    <button v-else class="genric-btn info radius text-uppercase" type="submit">Update</button>
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
                first_name: "",
                last_name: "",
                username: "",
                email: "",
                password: "",
                password_confirmation: "",
                
                phpn: "",
                birdthdate: "",
                weight: null,
                height: null,
                additional_info: "",

                company: "",
                specialities: "",
            }
        }
    },
    methods: {
        changeAccountType() {
            if(this.accountTypeChecked) {
                this.accountTypeChecked = false
            } else {
                this.accountTypeChecked = true
            }
        },

        async onSubmit() {
            /* Fields Validation */
            //console.log(this.filledform);
            if(this.filledform.password != this.filledform.password_confirmation) {
                this.$toasted.show('Password inputs must match!', 
                    {position: 'bottom-center', duration: 2500});
                return;
            }
            if(this.filledform.weight < 0) {
                this.$toasted.show('Do you really weight less than 0kg?', 
                    {position: 'bottom-center', duration: 2500});
                return;
            }
            if(this.filledform.height < 0) {
                this.$toasted.show('Are you really negative centimeters high?', 
                    {position: 'bottom-center', duration: 2500});
                return;
            }

            /* Server Validation */
            var result;
            if(this.accountTypeChecked) {
                result = await this.checkRegistration(this.filledform, 'doctor');
            } else {
                result = await this.checkRegistration(this.filledform, 'client');
            }
            if(result) {
                if(result.status==0){
                    result = await this.checkLogin(this.filledform);
                    if(result) {
                        if(result.status==0){
                            this.$store.dispatch('setSessionToken', result.data.token);
                            if(this.accountTypeChecked) {
                                this.$router.push("/patients");
                            } else {
                                this.$router.push("/");
                            }
                        } else {
                            // this should never happen
                            return;
                        }
                    } else {
                        return;
                    }
                } else {
                    return;
                }
            } else {
                return;
            }
        },

        async checkRegistration(filledform, account_type) {
            const config = {
                'type': account_type,
                'name': filledform.first_name + " " + filledform.last_name,
                'username': filledform.username,
                'email': filledform.email,
                'phpn': filledform.phpn,
                'password': filledform.password,
                'birth_date': this.convertDate(filledform.birthdate),
                'weight': this.convertNull(filledform.weight),
                'height': this.convertNull(filledform.height),
                'additional_information': filledform.additional_info,
                'company': filledform.company,
                'specialities': filledform.specialities,
            }
            //console.log(config)
            return await this.$axios.$post("/signup",config)
                        .then(res => {
                            if(res.status != 0) {
                                // warn which registration fields are invalid
                                console.log(res)
                                this.$toasted.show('Registration was invalid. Please make sure you fill in the form correctly.', 
                                    {position: 'bottom-center', duration: 5000});
                            }
                            return res;
                        })
                        .catch(e => {
                            // unable to register
                            this.$toasted.show('Something went wrong with the registration process. The server might be down at the moment. Please re-submit or try again later.', 
                                {position: 'bottom-center', duration: 7500});
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
                                console.log(res)
                                this.$toasted.show('Something went terribly wrong with the registration process. Please try to login, if it does not work contact us through email.', 
                                    {position: 'bottom-center', duration: 7500});
                            }
                            return res;
                        })
                        .catch(e => {
                            return null;
                        });
        },

        convertDate(birthdate) {
            if(birthdate) {
                var dd = birthdate.getDate();
                var mm = birthdate.getMonth() + 1; //January is 0!
                var yyyy = birthdate.getFullYear();

                if (dd < 10) { dd = '0' + dd; } 
                if (mm < 10) { mm = '0' + mm; } 

                return dd + '-' + mm + '-' + yyyy;
            }   
            return "00-00-0000";
        },

        convertNull(field) {
            if(field) {
                return parseFloat(field);
            }
            return -1;
        }
    }
};
</script>

<style>
.register-form {
    margin-top: 25%;
    margin-bottom: 15%;
}
.title-form-wrap {
    font-size: 16px;
    font-weight: 600;
    margin-bottom: -12px;
    margin-top: 10px;
}
</style>
