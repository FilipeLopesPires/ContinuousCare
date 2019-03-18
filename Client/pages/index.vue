<template>
  <html lang="en">
    <!--================ HTML Header =================-->
    <HeaderHTML />

    <body>
      <!--================Header Menu Area =================-->
      <HeaderMenuHome />

      <!--================ Home Banner Area =================-->
      <HomeBanner />

      <!--================ Offered Services Area =================-->
      <section class="service_area section_gap">
        <div class="container">
          <div class="row justify-content-center section-title-wrap">
            <div class="col-lg-12">
              <h1>Our Offered Services</h1>
              <p>
                Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
              </p>
            </div>
          </div>

          <div class="row">
            <ServiceBox />
            <ServiceBox />
            <ServiceBox />
            <ServiceBox />
          </div>
        </div>
      </section>

      <!--================ Footer Area =================-->
      <PageFooter />

    </body>
    <nuxt/>
  </html>
</template>

<script>
import HeaderHTML from '@/components/headers/HeaderHTML.vue'
import HeaderMenuHome from '@/components/headers/HeaderMenuHome.vue'
import HomeBanner from '@/components/banners/HomeBanner.vue'
import ServiceBox from '@/components/boxes/ServiceBox.vue'
import PageFooter from '@/components/footers/PageFooter.vue'

export default { 
  components: {
    HeaderHTML,
    HeaderMenuHome,
    HomeBanner,
    ServiceBox,
    PageFooter
  }
}
</script>

<style scoped>

</style>
