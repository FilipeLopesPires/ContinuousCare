<template>
    <div class="login-form" >
        <h3 class="mt-120 mb-30 title_color text-center" >Welcome Back!</h3>
        <form class="form-wrap" @submit.prevent="onSubmit">
            <!-- Username -->
            <div class="mt-10">
                <input required class="single-input" v-bind="$attrs" v-on="$listeners" v-model="filledform.username" type="text" name="username" placeholder="Username" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Username'">
            </div>
            <!-- Password -->
            <div class="mt-10">
                <input required class="single-input" v-bind="$attrs" v-on="$listeners" v-model="filledform.password" type="password" name="password" placeholder="Password" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Password'">
            </div>
            <!-- Submit -->
            <div class="row justify-content-center d-flex align-items-center">
                <div class="mt-10 col-lg-4 col-md-3 justify-content-center d-flex align-items-center">
                    <button class="genric-btn info radius text-uppercase" type="submit">Log In</button>
                </div>
                <div class="mt-10 col-lg-8 col-md-9">
                    <p class="mt-10">
                        Not registered yet? <nuxt-link to="/register">Start Now!</nuxt-link> 
                        <br>I forgot my password 
                        <nuxt-link to="" @click.native="forgotMyPassword">Help!</nuxt-link>
                    </p>
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
        return {
            filledform: {
                username: null,
                password: null
            }
        }
    },
    methods: {
        async onSubmit() {
            var result = await this.checkLogin(this.filledform);
            if(result) {
                if(result.status==0){ // login successful
                    this.$store.dispatch('setSessionToken', result.data.token);
                    result = await this.getProfile(this.$store.getters.sessionToken); // or simply result.data.token
                    if(result) {
                        if(result.status==0){ // profile info retrieval successful
                            var profile;
                            var push = "/";
                            if(result.data.user_type == "client") {
                                profile = {
                                    full_name: this.convertEmpty(result.data.full_name),
                                    email: this.convertEmpty(result.data.email),
                                    health_number: this.convertEmpty(result.data.health_number),
                                    birth_date: this.convertEmpty(result.data.birth_date),
                                    weight: this.convertEmpty(result.data.weight),
                                    height: this.convertEmpty(result.data.height),
                                    additional_info: this.convertEmpty(result.data.additional_info),
                                    company: null,
                                    specialities: null
                                }
                            } else {
                                profile = {
                                    full_name: this.convertEmpty(result.data.full_name),
                                    email: this.convertEmpty(result.data.email),
                                    health_number: null,
                                    birth_date: null,
                                    weight: null,
                                    height: null,
                                    additional_info: null,
                                    company: this.convertEmpty(result.data.company),
                                    specialities: this.convertEmpty(result.data.specialities)
                                }
                                push += "patients";
                            }

                            if(this.$store.getters.isLoggedIn){
                                this.$store.dispatch("setVue", this)
                                this.$store.dispatch("setReloadControl")
                                console.log("Connecting to WebSocket");
                                this.$connect('ws://mednat.ieeta.pt:8344', {store:this.$store,reconnectionAttempts: 5,reconnectionDelay: 3000})
                            }

                            this.$store.dispatch('setUserType', result.data.user_type);
                            this.$store.dispatch('setProfile', profile);
                            this.$router.push(push);
                        } 
                    } 
                } 
            }
            /* this.logInDev("medic"); */
        }, 
        forgotMyPassword() {
            //this.showToast("This feature is not yet implemented. We are sorry for the inconvenience :(", 5000);
            this.$router.push("/contact");
        },

        async checkLogin(filledform) {
            const config = {
                'username': filledform.username,
                'password': filledform.password
            }
            return await this.$axios.$post("/signin", config)
                        .then(res => {
                            if(res.status != 0) {
                                // warn which login field is invalid
                                console.log(res);
                                //this.showToast("Invalid username or password. Please make sure you fill in the fields correctly.", 5000);
                                if(res.status == 1) {
                                    this.showToast(res.msg, 5000);
                                } else if(res.status == 4) {
                                    this.$toasted.show(res.msg, {position: 'bottom-center', duration: 7500});
                                    this.$router.push("/login");
                                } else {
                                    this.showToast("Something went wrong with the login process. The server might be down at the moment. Please re-submit or try again later.", 7500);
                                }
                                return null;
                            }
                            return res;
                        })
                        .catch(e => {
                            // unable to login
                            console.log(e);
                            this.showToast("Something went wrong with the login process. The server might be down at the moment. Please re-submit or try again later.", 7500);
                            return null;
                        });
        },
        async getProfile(AuthToken) {
            const config = {
                headers: {'AuthToken': AuthToken}
            }
            return await this.$axios.$get("/profile", config)
                        .then(res => {
                            if(res.status != 0) {
                                // warn what exactly went wrong inside the server
                                console.log(res);
                                //this.showToast("Something went terribly wrong while trying to retrieve information about the user. Please try to login again, if it does not work contact us through email.", 7500);
                                if(res.status == 1) {
                                    this.showToast(res.msg, 5000);
                                } else if(res.status == 4) {
                                    this.$toasted.show(res.msg, {position: 'bottom-center', duration: 7500});
                                    this.$router.push("/login");
                                } else {
                                    this.showToast("Something went wrong while trying to retrieve information about the user. The server might be down at the moment. Please re-submit or try again later.", 7500);
                                }
                                return null;
                            }
                            return res;
                        })
                        .catch(e => {
                            // unable to retrieve profile info
                            console.log(e);
                            this.showToast("Something went wrong while trying to retrieve information about the user. The server might be down at the moment. Please re-submit or try again later.", 7500);
                            return null;
                        });
        },
        convertEmpty(field) {
            if(field == "null" || field == "" || field == null) {
                return null;
            }
            return field;
        },
        showToast(message, duration) {
            this.$toasted.show(message, {position: 'bottom-center', duration: duration});
        },
        logInDev(type) {
            this.$store.dispatch('setSessionToken', 'development-token');
            this.$store.dispatch('setUserType', type);
            var dev_profile = {
                full_name: "Admin Developer",
                email: "admin@admin.com",
                health_number: 1234,
                birth_date: "01-01-0001",
                weight: 50,
                height: 1.70,
                additional_info: "allergies",
                company: "pt gov",
                specialities: "ginobs"
            }
            this.$store.dispatch('setProfile', dev_profile); 
            if(type == "medic") {
                this.$router.push("/patients");
            } else {
                this.$router.push("/");
            }
        }
    }
};
</script>

<style>
.login-form {
    margin-top: 50%;
    margin-bottom: 50%;
}
</style>
