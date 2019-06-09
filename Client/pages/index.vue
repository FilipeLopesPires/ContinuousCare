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
                        description="Visit your account on our website whenever you wish to know your health conditions for any time."/>
            <ServiceBox icon="lnr lnr-picture" title1="User Friendly" title2="Data Visualization" 
                        description="Take advantage of our intuitive features to know better your body and the environment you live in."/>
            <ServiceBox icon="lnr lnr-users" title1="Data Sharing" title2="for Medical Consultations" 
                        description="Share relevant information with your doctor to better understand, prevent and treat complaints and diseases."/>
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
      <PageBanner parent_page="Home" page="Profile" :name="full_name" />

      <!--================ Main Area =================-->
      <div class="justify-content-center d-flex align-items-top mb-20">
        <div class="justify-content-center d-flex align-items-top col-lg-11 col-md-11 max-width-1920">
          <div class="col-lg-5 col-md-5 col-sm-5 col-xs-5 mr--30 mt-30 ">
            <Events style="height:600px;" :startTime="startEvents" :endTime="endEvents" :refresh="refresh"/>
          </div>
          <div class="col-lg-7 col-md-7 col-sm-7 col-xs-7 ml--30">
            <TagsArea :areas="tags_area" @submited="refreshEvents"/>
          </div>
        </div>
      </div>

      <!--================ Sleep Area =================-->
      <div class="justify-content-center d-flex align-items-top mb-50">
        <div class="col-lg-9 col-md-9 col-sm-12 col-xs-12">
          <h3 class="widget_title"> Sleep Pattern </h3>
          <SleepBox />
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
import Events from '@/components/events/Events.vue'
import SleepBox from '@/components/boxes/SleepBox.vue'

export default { 
  middleware: ['check-log', 'clients-only'],
  components: {
    HomeBanner,
    ServiceBox,
    TagsArea,
    Events,
    SleepBox,
  },
  data() {
    var d = new Date()
    return {
      event: "",
      refresh: null,
      startEvents:parseInt(new Date().setHours(0,0,0,0)/1000),
      endEvents:parseInt(new Date().getTime()/1000),
      full_name: this.$store.getters.profile.full_name,
      tags_area: [
        {
          title: "How Are You Feeling Today?",
          tags: ["Amused","Calm","Cheerful","Dreamy","Excited","Flirty","Good","Happy","Joyful","Loving","Mellow","Optimistic","Peaceful","Silly","Sympathetic","Angry","Annoyed / Irritated","Apathetic","Bad","Cranky / Grumpy","Depressed","Envious","Frustrated","Gloomy","Guilty","Indifferent","Melancholy","Pessimistic","Rejected","Restless","Sad","Stressed","Weird"],
        },
        {
          title: "Would You Like To Take Note Of Any Complaints?",
          tags: ["Cold / Respiratory Pain","Insomnia / Difficult Night","Migraine / Headache","Muscle Soreness or Injury","Allergies","Back or Joint Pain","Skin Conditions","Stomache or Intestinal Disconforts","Overstress / Heart Disconfort"]
        }
      ],
    }
  },
 /* mounted() {
    this.full_name = this.$store.getters.profile.full_name;
  }, */
  methods: {
    refreshEvents(evt){
      this.endEvents=parseInt(new Date().getTime()/1000)
      this.refresh=evt.timestamp
    },
    loggedIn() {
      if(this.$store.getters.isLoggedIn) {
        this.$nextTick(() => { this.$store.dispatch('setSessionToken', this.$store.getters.sessionToken) });
        return true
      }
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
.widget_title {
    font-size: 18px;
    line-height: 25px;
    background: #3face4;
    text-align: center;
    color: #fff;
    padding: 8px 0px;
    margin-bottom: 30px; }
</style>
