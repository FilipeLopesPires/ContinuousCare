<template>
    <header :class="headerClass">
        <HeaderInfo />
        <div class="main_menu">
            <nav class="navbar navbar-expand-lg navbar-light">
                <div class="container">
                    <!-- Brand and toggle get grouped for better mobile display -->
                    <nuxt-link class="navbar-brand logo_h" to="/patients"> 
                        <img src="~/assets/img/logo/logo_cc_2.png" alt="">
                    </nuxt-link>
                    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent"
                    aria-expanded="false" aria-label="Toggle navigation">
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                    </button>
                    <!-- Collect the nav links, forms, and other content for toggling -->
                    <div :class="account_class" class="collapse navbar-collapse offset" id="navbarSupportedContent" >
                        <div class="row ml-0 w-100">
                            <div class="col-lg-12 pr-0">
                                <ul class="nav navbar-nav center_nav pull-right">
                                    <nuxt-link :class="{ active: isActive('Patients') }" class="nav-item" to="/patients">
                                        <span class="nav-link">Patients</span>     <!-- ... !!! TO DO !!! ... -->
                                    </nuxt-link>
                                    <li class="nav-item submenu dropdown">
                                        <a href="" :class="{ active: isActive('Settings') }" class="nav-link dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Help</a>
                                        <ul class="dropdown-menu">
                                            <li class="nav-item" >
                                                <nuxt-link class="nav-link" to="/settings">Profile Settings</nuxt-link>
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

export default {
    name: 'HeaderMenuMedic',
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
        var account_class = "";
        if(this.$store.getters.userType == "medic") {
            account_class += "medic";
        }
        return {
            scrolled: false,
            headerClass: "header_area",
            account_class,
        };
    },
    methods: {
        isActive(menuItem) {
            return this.activePage === menuItem;
        },
        logout() {
            this.$nextTick(() => { 
                this.$store.dispatch('logout'),
                this.$router.push("/login")
            });
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
