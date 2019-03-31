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
                                <ul class="nav navbar-nav center_nav pull-right">
                                    <nuxt-link class="nav-item active" to="/">
                                        <span class="nav-link">Home</span>
                                    </nuxt-link>
                                    <nuxt-link class="nav-item" to="/tmp">
                                        <span class="nav-link">TMP</span>
                                    </nuxt-link>
                                    <nuxt-link class="nav-item" to="/history">
                                        <span class="nav-link">History</span>
                                    </nuxt-link>
                                    <nuxt-link class="nav-item" to="/devices">
                                        <span class="nav-link">Devices</span>
                                    </nuxt-link>
                                    <nuxt-link class="nav-item" to="/about">
                                        <span class="nav-link">About</span>
                                    </nuxt-link>
                                    <li class="nav-item submenu dropdown">
                                        <a href="#" class="nav-link dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Help</a>
                                        <ul class="dropdown-menu">
                                            <li class="nav-item">
                                                <nuxt-link class="nav-link" to="/settings">Account Settings</nuxt-link>
                                            </li>
                                            <li class="nav-item">
                                                <nuxt-link class="nav-link" to="/settings">Contact Us</nuxt-link>
                                            </li>
                                        </ul>
                                    </li>
                                    <nuxt-link class="nav-item" to="/login">
                                        <span class="nav-link">Login or Register</span>
                                    </nuxt-link>
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
    name: 'HeaderMenu',
    props: {
        
    },
    components: {
        HeaderInfo
    }
}
</script>

<style>

</style>
