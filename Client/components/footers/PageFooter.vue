<template>
    <footer class="footer-area section_gap">
        <div class="container">
            <div class="row">
                <div class="col-lg-3  col-md-6">
                    <div class="single-footer-widget">
                        <h6>Top Features</h6>
                        <ul class="footer-nav">
                            <li>
                                <p>Environment Analysis based on Geolocation</p>
                            </li>
                            <li>
                                <p>Real-time Health Status Tracking</p>
                            </li>
                            <li>
                                <p>User Friendly Data Visualization</p>
                            </li>
                            <li>
                                <p>Data Sharing for Medical Consultations</p>
                            </li>
                        </ul>
                    </div>
                </div>
                <div class="col-lg-3  col-md-6">
                    <div class="single-footer-widget mail-chimp">
                        <h6 class="mb-20">Contact Us</h6>
                        <p>
                            Campus Universitário de Santiago, 3810-193 Aveiro
                        </p>
                        <p>+351 123 456 789</p>
                        <p>general_email@continuouscare.com</p>
                    </div>
                </div>
                <div class="col-lg-6  col-md-12">
                    <div class="single-footer-widget newsletter">
                        <h6>Newsletter</h6>
                        <p>Keep informed about our latest updates!</p>
                        <div id="mc_embed_signup">
                            <form @submit.prevent="onSubmit" class="form-inline">
                                <div class="form-group row">
                                    <div class="col-lg-7 col-md-6 col-sm-12">
                                        <input name="EMAIL" placeholder="Your Email Address" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Your Email Address '" required="" type="email">
                                    </div>
                                    <div class="col-lg-5 col-md-12">
                                        <button :class="css_class_btn">Get Started
                                            <span class="lnr lnr-arrow-right"></span>
                                        </button>
                                    </div>
                                </div>
                                <div class="info"></div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>

            <div class="row footer-bottom d-flex justify-content-between">
                <p class="col-lg-8 col-sm-12 footer-text m-0">
                    Copyright &copy; 2019 All rights reserved | ContinuousCare
                </p>
                <div :class="css_class_social">
                    <a href="https://drive.google.com/open?id=1SzGB95gpO4g3TtLYx_FPNkP1XkCdRs-V">
                        <i class="fa fa-google"></i>
                    </a>
                    <a href="https://www.facebook.com/continuous.care.58">
                        <i class="fa fa-facebook-f"></i>
                    </a>
                    <a href="http://code.ua.pt/projects/personal_monitoring_system?jump=search">
                        <i class="fa fa-github"></i>
                    </a>
                </div>
            </div>
        </div>
    </footer>
</template>

<script>
export default {
    name: 'PageFooter',
    props: {
        
    },
    data() {
        var css_class_btn = "nw-btn circle main_btn";
        var css_class_social = "col-lg-4 col-sm-12 footer-social";
        if(this.$store.getters.userType == "medic") {
            css_class_btn += "_medic";
            css_class_social += "_medic";
        }
        return {
            css_class_btn,
            css_class_social
        }
    },
    methods: {
        onSubmit() {
            this.$toasted.show('This feature is not yet implemented. We are sorry for the inconvenience :(', 
                {position: 'bottom-center', duration: 4000});
        }, 
    }
}
</script>

<style>

</style>
