<template>
    <header class="header_area">
        <div class="top_menu row m0">
            <div class="container">
                <div class="float-left">
                    <ul class="left_side">
                        <li>
                            <a href="#">
                                <i class="fa fa-facebook-f"></i>
                            </a>
                        </li>
                        <li>
                            <a href="#">
                            <i class="fa fa-twitter"></i>
                            </a>
                        </li>
                        <li>
                            <a href="#">
                            <i class="fa fa-dribbble"></i>
                            </a>
                        </li>
                        <li>
                            <a href="#">
                            <i class="fa fa-behance"></i>
                            </a>
                        </li>
                    </ul>
                </div>
                <div class="float-right">
                    <ul class="right_side">
                        <li>
                            <a href="#">
                            <i class="lnr lnr-phone-handset"></i>
                            +351 123 456 789
                            </a>
                        </li>
                        <li>
                            <a href="#">
                            <i class="lnr lnr-envelope"></i>
                            general_cc@continuouscare.com
                            </a>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
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
                    <div class="collapse navbar-collapse offset" id="navbarSupportedContent">
                        <div class="row ml-0 w-100">
                            <div class="col-lg-12 pr-0">
                                <ul class="nav navbar-nav center_nav pull-right">
                                    <li class="nav-item active">
                                        <nuxt-link class="nav-link" to="/">Home</nuxt-link>
                                    </li>
                                    <li class="nav-item ">
                                        <nuxt-link class="nav-link" to="/about">About</nuxt-link>
                                    </li>
                                    <li class="nav-item ">
                                        <nuxt-link class="nav-link" to="/tmp">TMP</nuxt-link>
                                    </li>
                                    <li class="nav-item ">
                                        <nuxt-link class="nav-link" to="/login">Login/Register</nuxt-link>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </nav>
        </div>
    </header>
</template>

<script>
export default {
    
}
</script>

<style>

</style>
