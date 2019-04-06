<template>
    <div>
        <!--================ HTML Header =================-->
        <HeaderHTML page="Devices" />

        <body>
            <!--================ Header Menu Area =================-->
            <HeaderMenu activePage="Devices" />

            <!--================ Banner Area =================-->
            <PageBanner parent_page="Home" page="Devices" />

            <!--================ Devices Area =================-->
            <section class="procedure_category section_gap">
                <div class="container">
                    <div class="row justify-content-center section-title-wrap">
                        <div class="col-lg-12">
                            <h1>My Devices</h1>
                            <p>
                                Currently you have X devices linked to your account. 
                                If you wish, you may add new devices or manage the existing ones.
                                Remember that it is only possible to link one home device.
                            </p>
                        </div>
                    </div>
                    <DeviceList :devices="loadedDevices" />
                </div>
            </section>
            
            <!--================ Footer Area =================-->
            <PageFooter />
            
        </body>
        <nuxt/>
    </div>
</template>

<script>
import DeviceList from '@/components//boxes/DeviceList.vue'
import HeaderHTML from '@/components/headers/HeaderHTML.vue'
import HeaderMenu from '@/components/headers/HeaderMenu.vue'
import PageBanner from '@/components/banners/PageBanner.vue'
import PageFooter from '@/components/footers/PageFooter.vue'

export default {
    components: {
        DeviceList,
        HeaderHTML,
        HeaderMenu,
        PageBanner,
        PageFooter
    },
    data() {
        return {
            loadedDevices: [
                {name: "Fitbit Charge 3", photo: "https://ss7.vzw.com/is/image/VerizonWireless/fitbit-charge3-graphite-black-fb409gmbk-a?$png8alpha256$&hei=410"},
                {name: "Add Device", photo: "http://www.clker.com/cliparts/A/P/L/b/V/G/blue-plus-sign-hi.png"}
            ]
        }
    }
    /*
    asyncData(context, callback) {
        callback(new Error(), {
            loadedDevices: [
                {name: "Fitbit Charge 3", photo: "https://ss7.vzw.com/is/image/VerizonWireless/fitbit-charge3-graphite-black-fb409gmbk-a?$png8alpha256$&hei=410"},
                {name: "Add Device", photo: "http://www.clker.com/cliparts/A/P/L/b/V/G/blue-plus-sign-hi.png"}
            ]
        });
    },
    created() {
        this.$store.dispatch("setDevices", this.loadedDevices)
    } */
}
</script>

<style scoped>

</style>