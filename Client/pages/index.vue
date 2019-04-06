<template>
  <div>
    <!--================ HTML Header =================-->
    <HeaderHTML page="Home" />

    <body>
      <!--================Header Menu Area =================-->
      <HeaderMenu activePage="Home" />

      <!--================ Home Banner Area =================-->
      <HomeBanner />

      <!--================ Services Area =================-->
      <section class=" section_gap">
        <div class="container">
          <div class="row justify-content-center section-title-wrap">
            <div class="col-md-12 col-lg-12">
              <h1>Our Offered Services</h1>
              <p>Our system is capable of automatically collect health-oriented data, such as weather conditions, air quality indicators, vital signals, geolocalization, etc. once a client configures the health-tracking devices.
                We make simple the registration of basic physical and mental health states of each client through our web application, such as local pains, depression, anxiety, fatigue and more, while respecting the privacy of all members.
                This information is treated and presented to the client in an intuitive form, focusing on the relevant episodes throughout time.</p>
            </div>
          </div>

          <div class="row">
            <ServiceBox icon="lnr lnr-map-marker" title="Environment Analysis based on Geolocation" 
                        description="... description here ..."/>
            <ServiceBox icon="lnr lnr-heart-pulse" title="Real-time Health Status Tracking" 
                        description="... description here ..."/>
            <ServiceBox icon="lnr lnr-picture" title="User Friendly Data Visualization" 
                        description="... description here ..."/>
            <ServiceBox icon="lnr lnr-users" title="Data Sharing for Medical Consultations" 
                        description="... description here ..."/>
          </div>
        </div>
      </section>

      <!--================ Footer Area =================-->
      <PageFooter />

    </body>
    <nuxt/>
  </div>
</template>

<script>
import HeaderHTML from '@/components/headers/HeaderHTML.vue'
import HeaderMenu from '@/components/headers/HeaderMenu.vue'
import HomeBanner from '@/components/banners/HomeBanner.vue'
import ServiceBox from '@/components/boxes/ServiceBox.vue'
import PageFooter from '@/components/footers/PageFooter.vue'

export default { 
  components: {
    HeaderHTML,
    HeaderMenu,
    HomeBanner,
    ServiceBox,
    PageFooter
  }
}
</script>

<style scoped>

</style>
