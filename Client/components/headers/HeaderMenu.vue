<template>
    <header class="header_area">
        <HeaderInfo />
        <div class="main_menu">
            <nav class="navbar navbar-expand-lg navbar-light">
                <div class="container">
                    <!-- Brand and toggle get grouped for better mobile display -->
                    <nuxt-link class="navbar-brand logo_h" to="/"> 
                        <img src="~/assets/img/logo/logo_cc.png" alt="">
                    </nuxt-link>
                    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent"
                    aria-expanded="false" aria-label="Toggle navigation">
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    </button>
                    <!-- Collect the nav links, forms, and other content for toggling -->
                    <div class="collapse navbar-collapse offset" id="navbarSupportedContent" >
                        <div class="row ml-0 w-100">
                            <div class="col-lg-12 pr-0">
                                <ul v-if="!loggedIn()" class="nav navbar-nav center_nav pull-right">
                                    <nuxt-link :class="{ active: isActive('Home') }" class="nav-item" to="/">
                                        <span class="nav-link">Home</span>
                                    </nuxt-link>
                                    <nuxt-link :class="{ active: isActive('About') }" class="nav-item" to="/about">
                                        <span class="nav-link">About</span>
                                    </nuxt-link>
                                    <nuxt-link :class="{ active: isActive('Contact') }" class="nav-item" to="/contact">
                                        <span class="nav-link">Contact Us</span>
                                    </nuxt-link>
                                    <li class="nav-item submenu dropdown">
                                        <a href="" :class="{ active: isActive('Login or Register') }" class="nav-link dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Login or Register</a>
                                        <ul class="dropdown-menu">
                                            <li class="nav-item">
                                                <nuxt-link class="nav-link" to="/login">Login</nuxt-link>
                                            </li>
                                            <li class="nav-item">
                                                <nuxt-link class="nav-link" to="/register">Register</nuxt-link>
                                            </li>
                                        </ul>
                                    </li>
                                </ul>
                                <ul v-else class="nav navbar-nav center_nav pull-right">
                                    <nuxt-link :class="{ active: isActive('Home') }" class="nav-item" to="/">
                                        <span class="nav-link">Home</span>
                                    </nuxt-link>
                                    <nuxt-link :class="{ active: isActive('TMP') }" class="nav-item" to="/tmp">
                                        <span class="nav-link">TMP</span>
                                    </nuxt-link>
                                    <nuxt-link :class="{ active: isActive('History') }" class="nav-item" to="/history">
                                        <span class="nav-link">History</span>
                                    </nuxt-link>
                                    <nuxt-link :class="{ active: isActive('Devices') }" class="nav-item" to="/devices">
                                        <span class="nav-link">Devices</span>
                                    </nuxt-link>
                                    <li class="nav-item submenu dropdown">
                                        <a href="" class="nav-link dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Help</a>
                                        <ul class="dropdown-menu">
                                            <li class="nav-item" :class="{ active: isActive('Settings') }">
                                                <nuxt-link class="nav-link" to="/settings">Account Settings</nuxt-link>
                                            </li>
                                            <li class="nav-item">
                                                <nuxt-link class="nav-link" to="/contact">Contact Us</nuxt-link>
                                            </li>
                                            <li class="nav-item" @click="logout()">
                                                <nuxt-link class="nav-link" to="/" >Logout</nuxt-link>
                                            </li>
                                        </ul>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </nav>
        </div>
        <nuxt/>
    </header>
</template>

<script>
import HeaderInfo from '@/components/headers/HeaderInfo.vue'

/* import * as Cookies from 'js-cookie' */

export default {
    name: 'HeaderMenu',
    props: {
        activePage: {
			type: String,
			required: true
		},
    },
    components: {
        HeaderInfo
    },
    methods: {
        loggedIn() {
            //console.log("Token:")
            //console.log(this.$store.getters.sessionToken);
            if(this.$store.getters.sessionToken == null) {
                //console.log("not logged in")
                this.$nextTick(() => { this.$store.dispatch('setSessionToken', this.$store.getters.sessionToken) });
                return false
            }
            //console.log("logged in")
            this.$nextTick(() => { this.$store.dispatch('setSessionToken', this.$store.getters.sessionToken) });
            return true
        },
        isActive(menuItem) {
            return this.activePage === menuItem;
        },
        logout() {
            //$cookies.remove()
            console.log("testing logout");
            this.$nextTick(() => { 
                this.$store.dispatch('loadedDevices', []),
                this.$store.dispatch('setSessionToken', null) 
            });
        }
    }
}
</script>

<style>

</style>
