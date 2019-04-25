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
                        <br>I forgot my password <nuxt-link to="" @click="forgotMyPassword">Help!</nuxt-link> 
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
                username: "",
                password: ""
            }
        }
    },
    methods: {
        async onSubmit() {
            /* var result = await this.checkLogin(this.filledform);
            if(result) {
                if(result.status==0){
                    // store user token
                    this.$store.dispatch('setSessionToken', result.data.token);

                    result = await this.getProfile(this.$store.getters.sessionToken); // or simply result.data.token
                    if(result) {
                        if(result.status==0){
                            // store user personal info
                            var profile = {
                                client_id: result.data.client_id,
                                full_name: result.data.full_name,
                                email: result.data.email,
                                health_number: result.data.health_number,
                                birth_date: result.data.birth_date,
                                weight: result.data.weight,
                                height: result.data.height
                            }
                            this.$store.dispatch('setUserType', result.type);
                            this.$store.dispatch('setProfile', profile);
                            if(result.type == "doctor") {
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
            } */
            this.$store.dispatch('setSessionToken', 'development-token');
            this.$store.dispatch('setUserType', "client");
            this.$router.push("/");
        }, 
        forgotMyPassword() {
            this.$toasted.show('This feature is not yet implemented. We are sorry for the inconvenience :(', 
                {position: 'bottom-center', duration: 5000});
        },

        async checkLogin(filledform) {
            const config = {
                'username': filledform.username,
                'password': filledform.password
            }
            return await this.$axios.$post("/signin",config)
                        .then(res => {
                            if(res.status != 0) {
                                // warn which login field is invalid
                                console.log(res)
                                this.$toasted.show('Invalid username or password. Please make sure you fill in the fields correctly.', 
                                    {position: 'bottom-center', duration: 5000});
                            }
                            return res;
                        })
                        .catch(e => {
                            // unable to login
                            this.$toasted.show('Something went wrong with the login process. The server might be down at the moment. Please re-submit or try again later.', 
                                {position: 'bottom-center', duration: 7500});
                            return null;
                        });
        },
        async getProfile(AuthToken) {
            const config = {
                headers: {'AuthToken': AuthToken}
            }
            return await this.$axios.$get("/profile",config)
                        .then(res => {
                            if(res.status != 0) {
                                // warn what exactly went wrong inside the server
                                console.log(res)
                                this.$toasted.show('Something went terribly wrong while trying to retrieve information about the user. Please try to login again, if it does not work contact us through email.', 
                                    {position: 'bottom-center', duration: 7500});
                            }
                            return res;
                        })
                        .catch(e => {
                            // unable to retrieve profile info
                            this.$toasted.show('Something went wrong while trying to retrieve information about the user. The server might be down at the moment. Please re-submit or try again later.', 
                                {position: 'bottom-center', duration: 7500});
                            return null;
                        });
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
