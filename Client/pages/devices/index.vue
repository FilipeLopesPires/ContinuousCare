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
                <div v-if="supported_devices.length > 0">
                    <div class="mb-20 container" v-for="device in supported_devices"
                                                        :key="device.id"
                                                        :device="device">
                        <h3 class="text-heading title_color">{{device.brand}} {{device.model}}</h3>
                        <p class="sample-text">
                            Type: {{formatType(device.type)}}
                        </p>
                        <p class="sample-text">
                            Supported Metrics: {{formatMetrics(device.metrics)}}
                        </p>
                    </div>
                </div>
                <div v-else class="row justify-content-center">
                    <h2>Unable to load supported devices.</h2>
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
import Vue from "vue"
import Toasted from 'vue-toasted'
Vue.use(Toasted)

import DeviceBox from '@/components/boxes/DeviceBox.vue'

export default {
    middleware: ['check-log', 'log', 'clients-only'],
    components: {
        DeviceBox,
    },
    data() {
        var requestError = false;
        var loaded_devices = [{id: 1000, type: "Add Device", token: "", photo: ""}];
        var supported_devices = [];

        return {
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

            requestError,
            loaded_devices,
            supported_devices,
        }
    },
    async mounted() {
        await this.getDevices(this.$store.getters.sessionToken);
        if(!this.requestError) {
            this.$store.dispatch('setDevices', this.loaded_devices);
        }
        await this.getSupportedDevices();
        if(this.supported_devices.length > 0) {
            this.$store.dispatch('setSupportedDevices', this.supported_devices);
        }
    },
    methods: {
        async getSupportedDevices() {
            this.supported_devices = await this.$axios.$get("/supportedDevices")
                                    .then(res => {
                                        if(res.status != 0) {
                                            if(res.status == 4) {
                                                this.$toasted.show(res.msg, {position: 'bottom-center', duration: 7500});
                                                this.$disconnect()
                                                this.$nextTick(() => { 
                                                    this.$store.dispatch('logout'),
                                                    this.$router.push("/login")
                                                });
                                            }
                                            console.log(res)
                                            return [];
                                        } 
                                        return res.data;
                                    })
                                    .catch(e => {
                                        // Unable to get supported devices from server
                                        this.$toasted.show('Something went wrong while trying to retrieve supported devices. The server might be down at the moment. Please try again later.', 
                                            {position: 'bottom-center',
                                            duration: 7500});
                                        return [];
                                    });
            
        },
        async getDevices(AuthToken) {
            const config = {
                headers: {'AuthToken': AuthToken}
            }
            var new_devices = await this.$axios.$get("/devices",config)
                                .then(res => {
                                    if(res.status != 0) {
                                        if(res.status == 4) {
                                            this.$toasted.show(res.msg, {position: 'bottom-center', duration: 7500});
                                            this.$disconnect()
                                            this.$nextTick(() => { 
                                                this.$store.dispatch('logout'),
                                                this.$router.push("/login")
                                            });
                                        }
                                        this.requestError = true;
                                        console.log(res)
                                        return [];
                                    }
                                    return res.data;
                                })
                                .catch(e => {
                                    // Unable to get devices from server
                                    this.$toasted.show('Something went wrong while trying to retrieve devices. The server might be down at the moment. Please try again later.', 
                                        {position: 'bottom-center',
                                        duration: 7500});
                                    this.requestError = true;
                                    return [];
                                });
            if(new_devices.length > 0) {
                this.loaded_devices = new_devices.concat(this.loaded_devices);
            }
        },
        formatType(type) {
            var formatedType;
            if(type == "bracelet") {
                formatedType = "Smart Bracelet";
            } else if(type == "home_device") {
                formatedType = "Home Device";
            } else {
                formatedType = type;
            }
            return formatedType;
        },
        formatMetrics(metrics) {
            var retval = "";
            for(var i=0; i<metrics.length; i++) {
                retval += metrics[i].name + " (in " + metrics[i].unit + ")";
                if(i!=metrics.length-1) {
                    retval += ", ";
                } else {
                    retval += ".";
                }
            }
            return retval;
        }
    },
    head: {
        title: "Devices"
    }
}
</script>

<style scoped>

</style>