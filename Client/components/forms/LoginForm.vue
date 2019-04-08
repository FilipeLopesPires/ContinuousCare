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
                <div class="mt-10 col-lg-4 col-md-3">
                    <button class="main_btn text-uppercase" type="submit">Register</button>
                </div>
                <div class="mt-10 col-lg-8 col-md-9">
                    <p>Not registered yet? <nuxt-link to="/register">Start Now!</nuxt-link> </p> 
                    <p>I forgot my password <nuxt-link to="" @click="forgotMyPassword">Help!</nuxt-link> </p> 
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
        onSubmit() {
            console.log(this.filledform);
        },
        forgotMyPassword() {
            console.log("ask for email");
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
