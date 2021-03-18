<template>
    <header :class="headerClass">
        <HeaderInfo />
        <div class="main_menu" >
            <nav class="navbar navbar-expand-lg navbar-light">
                <div class="container">
                    <!-- Brand and toggle get grouped for better mobile display -->
                    <nuxt-link class="navbar-brand logo_h" to="/"> 
                        <img src="~/assets/img/logo/logo_cc.png" alt="" class="navbar-logo">
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
                                <ul class="nav navbar-nav center_nav pull-right">
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

export default {
    name: 'HeaderMenuDefault',
    props: {
        activePage: {
			type: String,
			required: true
		},
    },
    components: {
        HeaderInfo
    },
    data() {
        var scrolled;
        var headerClass;
        return {
            scrolled: false,
            headerClass: "header_area"
        };
    },
    methods: {
        isActive(menuItem) {
            return this.activePage === menuItem;
        },
        handleScroll () {
            this.scrolled = window.scrollY > 30;
            if(this.scrolled) {
                this.headerClass = "header_area navbar_fixed"
            } else {
                this.headerClass = "header_area"
            }
        },
    },
    beforeMount () {
        window.addEventListener('scroll', this.handleScroll);
    },
    beforeDestroy () {
        window.removeEventListener('scroll', this.handleScroll);
    }
}
</script>

<style>

</style>
