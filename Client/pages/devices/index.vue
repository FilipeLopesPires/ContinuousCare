<template>
    <div>
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
                            <h1>Your Devices</h1>
                            <p>
                                Currently you have {{loaded_devices.length-1}} devices linked to your account. 
                                If you wish, you may add new devices or manage the existing ones.
                                Remember that it is only possible to link one personal device (bracelet).
                            </p>
                        </div>
                    </div>
                    <div class="row">
                        <DeviceBox v-for="device in loaded_devices"
                        :key="device.id"
                        :device="device.device"
                        /> 
                    </div>
                </div>
            </section>

            <section >
                <div class="row justify-content-center section-title-wrap">
                    <h1>Our Partners</h1>
                </div>
                <div class="mb-20 container">
                    <h3 class="text-heading title_color">Fitbit Charge 3</h3>
                    <p class="sample-text">
                        ... [ information about the device here ] ...
                    </p>
                </div>
                <div class="mt-10 container">
                    <h3 class="text-heading title_color">Foobot</h3>
                    <p class="sample-text">
                        ... [ information about the device here ] ...
                    </p>
                </div>
                <div class="mb-50"></div>
            </section>
            
            <!--================ Footer Area =================-->
            <PageFooter />
            
        </body>
        <nuxt/>
    </div>
</template>

<script>
import DeviceBox from '@/components//boxes/DeviceBox.vue'

export default {
    components: {
        DeviceBox,
    },
    data() {
        return {
            loaded_devices: [
                {device: {brand: "Fitbit", model: "Charge 3", 
                    type: "bracelet", authentication_fields: [["Token","0001"]],
                    supported_metrics: ["metric1","metric2"],
                    photo: "https://ss7.vzw.com/is/image/VerizonWireless/fitbit-charge3-graphite-black-fb409gmbk-a?$png8alpha256$&hei=410"}},
                {device: {brand: "Foobot", model: "", 
                    type: "home_device", authentication_fields: [["Token","0002"], ["UUID", "0001"]],
                    supported_metrics: ["metric3","metric4"],
                    photo: "https://cdn.shopify.com/s/files/1/0008/7330/0029/products/foobot_x700.jpg?v=1528342886"}},
                {device: {brand: "Add", model:"Device", 
                    type: "", authentication_fields: [["",""]],
                    supported_metrics: [""],
                    photo: "http://www.clker.com/cliparts/A/P/L/b/V/G/blue-plus-sign-hi.png"}}
            ],
        }
    },
    methods: {

    },
    head: {
        title: "Devices"
    }
}
</script>

<style scoped>

</style>