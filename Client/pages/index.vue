<template>
  <div v-if="!loggedIn()">
    <body style="overflow-x: none;">
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
            <ServiceBox icon="lnr lnr-map-marker" title1="Environment Analysis" title2="based on Geolocation" 
                        description="Install our ContinuousCare Mobile app to keep track of the air quality of the places you visit."/>
            <ServiceBox icon="lnr lnr-heart-pulse" title1="Real-time Health" title2="Status Tracking" 
                        description="Visit ContinuousCare any time you wish to know your health conditions in any period of time."/>
            <ServiceBox icon="lnr lnr-picture" title1="User Friendly" title2="Data Visualization" 
                        description="Take advantage of our intuitive features to know better your body and the environment you live in."/>
            <ServiceBox icon="lnr lnr-users" title1="Data Sharing" title2="for Medical Consultations" 
                        description="Share relevant information with your local doctor to best understand, prevent and treat complaints and diseases."/>
          </div>
        </div>
      </section>

      <!--================ Footer Area =================-->
      <PageFooter />

    </body>
    <nuxt/>
  </div>
  <div v-else>
    <body style="overflow-x: none;">
      <!--================Header Menu Area =================-->
      <HeaderMenu activePage="Home" />

      <!--================ Banner Area =================-->
      <PageBanner parent_page="Home" page="Profile" />

      <!--================ Tags Area =================-->
      <div class="row justify-content-center d-flex align-items-center">
        <div class="col-lg-9">
          <TagsArea :areas="tags_area"/>
        </div>
      </div>

      <!--================ Footer Area =================-->
      <PageFooter />

    </body>
    <nuxt/>
  </div>
</template>

<script>
import HomeBanner from '@/components/banners/HomeBanner.vue'
import ServiceBox from '@/components/boxes/ServiceBox.vue'
import TagsArea from '@/components/boxes/TagsArea.vue'

export default { 
  middleware: 'check-log',
  components: {
    HomeBanner,
    ServiceBox,
    TagsArea,
  },
  data() {
    return {
      tags_area: [
        {area: {
          title: "How Are You Feeling Today?",
          tags: ["Amused","Calm","Cheerful","Dreamy","Excited","Flirty","Good","Happy","Joyful","Loving","Mellow","Optimistic","Peaceful","Silly","Sympathetic","Angry","Annoyed / Irritated","Apathetic","Bad","Cranky / Grumpy","Depressed","Envious","Frustrated","Gloomy","Guilty","Indifferent","Melancholy","Pessimistic","Rejected","Restless","Sad","Stressed","Weird"],
        }},
        {area: {
          title: "Would You Like To Take Note Of Any Complaints?",
          tags: ["Cold / Respiratory Pain","Insomnia / Difficult Night","Migraine / Headache","Muscle Soreness or Injury","Allergies","Back or Joint Pain","Skin Conditions","Stomache or Intestinal Disconforts","Overstress / Heart Disconfort"]
        }}
      ]
    }
  },
  methods: {
    loggedIn() {
      //console.log("Token:")
      //console.log(this.$store.getters.sessionToken);
      if(this.$store.getters.isLoggedIn) {
        //console.log("not logged in")
        this.$nextTick(() => { this.$store.dispatch('setSessionToken', this.$store.getters.sessionToken) });
        return true
      }
      //console.log("logged in")
      this.$nextTick(() => { this.$store.dispatch('setSessionToken', this.$store.getters.sessionToken) });
      return false
    }
  },
  head: {
    title: "ContinuousCare"
  }
}
</script>

<style scoped>

</style>
