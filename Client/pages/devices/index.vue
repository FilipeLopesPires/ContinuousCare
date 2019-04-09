<template>
    <div>
        <body style="overflow-x: none;">
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
                        :device="device"
                        /> 
                    </div>
                </div>
            </section>

            <section class="container">
                <div class="row justify-content-center">
                    <h1>Our Partners</h1>
                </div>
                <div class="mb-20 container">
                    <h3 class="text-heading title_color">Fitbit</h3>
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
        /* if(this.$store.getters.loadedDevices.length < 2) { */

            var requestError = false;
            var loaded_devices = [{id: 0, type: "Add Device", token: "", photo: "http://www.clker.com/cliparts/A/P/L/b/V/G/blue-plus-sign-hi.png"}];
            
            return {
                /* loaded_devices: [
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
                ], */

                /* {"status": 0, "msg": "Successfull operation.", 
                    "data": [
                        {"id": 3, "type": "FitBit Charge 3", 
                        "refresh_token": "7d0773d69555ee9a52f3210c662b95db788f4ad3e3b9a8a5ef9bd77f0c90abf8", 
                        "token": "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMkRLMlgiLCJzdWIiOiI3Q05RV1oiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJhY3QgcnNldCBybG9jIHJ3ZWkgcmhyIHJwcm8gcm51dCByc2xlIiwiZXhwIjoxNTU0ODU3NzEzLCJpYXQiOjE1NTQ4Mjg5MTN9.b-EJtKwgcO1beb1es8I6DNSIePGX6KfD03o09UfzPqo"}, 
                        {"id": 4, "type": "Foobot ", 
                        "latitude": 40.0, "longitude": -8.0, 
                        "uuid": "240D676D40002482",
                        "token": "eyJhbGciOiJIUzI1NiJ9.eyJncmFudGVlIjoiam9hby5wQHVhLnB0IiwiaWF0IjoxNTUyMDY2Njc5LCJ2YWxpZGl0eSI6LTEsImp0aSI6IjRiNmY2NzhiLWJjNTYtNDYxNi1hYmMyLTRiNjlkMTNkMjUzOSIsInBlcm1pc3Npb25zIjpbInVzZXI6cmVhZCIsImRldmljZTpyZWFkIl0sInF1b3RhIjoyMDAsInJhdGVMaW1pdCI6NX0.aeLLsrhh1-DVXSwl-Z_qDx1Xbr9oIid1IKsOyGQxwqQ"}
                        ]} */

                /* // AUX:
                this.$store.getters.loadedDevices
                this.$store.dispatch('setDevices', ...); */

                requestError,
                loaded_devices,
            }
        /* } */
    },
    async mounted() {
        console.log("mounted is running")
        await this.getDevices(this.$store.getters.sessionToken)
        if(!this.requestError) {
            console.log("no error");
            //this.insertPhotos();
            console.log(this.loaded_devices)
            this.$store.dispatch('setDevices', this.loaded_devices);
        }
    },
    methods: {
        async getDevices(AuthToken) {
            const config = {
                headers: {'AuthToken': AuthToken}
            }
            var new_devices = await this.$axios.$get("/devices",config)
                                .then(res => {
                                    if(res.status != 0) {
                                        this.requestError = true;
                                        return [];
                                    }
                                    return res.data;
                                })
                                .catch(e => {
                                    this.requestError = true;
                                    return [];
                                });
            if(new_devices.length > 0) {
                this.loaded_devices = new_devices.concat(this.loaded_devices);
            }
        },
        insertPhotos() {
            for(var i=0; i<this.loaded_devices.length-1; i++) {
                if(this.loaded_devices[i].type == "FitBit Charge 3") {
                    this.loaded_devices[i]["photo"] = "\"https://ss7.vzw.com/is/image/VerizonWireless/fitbit-charge3-graphite-black-fb409gmbk-a?$png8alpha256$&hei=410\"";
                } else {
                    this.loaded_devices[i]["photo"] = "\"https://cdn.shopify.com/s/files/1/0008/7330/0029/products/foobot_x700.jpg?v=1528342886\"";
                }
            }
        }
    },
    head: {
        title: "Devices"
    }
}
</script>

<style scoped>

</style>