<template>
    <modal 
        :name="getName(device)"
        transition="nice-modal-fade"
        :min-width="200"
        :min-height="200"
        height="auto"
        :delay="100"
        :adaptive="true"
        :pivot-y="0.5"
        :scrollable="true">
        <form class="size-modal-content" @submit.prevent="">
            <!-- Info -->
            <h3 class="title_color text-center" >{{ device.type }}</h3>
            <div v-if="device.type=='Add Device'" class="mt-10">
                <h5>Type:</h5>
                <div class="form-select" id="service-select">
                    <select v-if="device.type=='Add Device'" @change="activateChosenType($event)" v-bind="$attrs" v-on="$listeners" v-model="type" class="nice-select list">
                        <option class="option" value="" selected>Choose Type</option>
                        <option class="option" v-for="option in allOptions" :key="option.id" :value="option">{{ option }}</option> <!-- inactive if(device.type!='Add Device' && ) -->
                    </select>
                    <select v-else class="nice-select list">
                        <option class="option" :value="device.type" selected>{{ device.type }}</option>
                    </select>
                </div>
            </div>
            <div v-if="device.type!='Add Device'">
                <div class="mt-10" v-for="field in Object.keys(device)" :key="field.id" :field="field"> 
                    <h5 v-if="field != 'photo' && field != 'type' && field != 'id'">{{ field }}:</h5>
                    <input v-if="field != 'photo' && field != 'type' && field != 'id'" type="text" :value="device[field]" :placeholder="device[field]" :name="field" class="single-input"> 
                </div>
            </div>
            <div v-else>
                <div class="mt-10" v-for="field in chosenDeviceFields" :key="field.id" :field="field"> 
                    <h5 >{{ field }}:</h5>
                    <input required type="text" placeholder="" :name="field" class="single-input"> 
                </div>
            </div>
            <div class="mt-10 row justify-content-center d-flex align-items-center">
                <div class="col-lg-6 col-md-6 row justify-content-center">
                </div>
                <div class="col-lg-3 col-md-3 row justify-content-right">
                    <button v-if="device.type!='Add Device'" class="genric-btn primary radius text-uppercase" @click="onRemove" type="submit" >Remove</button>
                </div>
                <div class="col-lg-3 col-md-3 row justify-content-right">
                    <button v-if="device.type!='Add Device'" class="genric-btn info radius text-uppercase" @click="onUpdate" type="submit" >Update</button>
                    <button v-else                           class="genric-btn info radius text-uppercase" @click="onAdd" type="submit" >Add</button>
                </div>
            </div>
        </form>
    </modal>
</template>

<script>
import Vue from 'vue'
import VModal from 'vue-js-modal'
import Toasted from 'vue-toasted'
Vue.component('vmodal', VModal)
Vue.use(VModal)
Vue.use(Toasted)

export default {
    name: 'DeviceModal',
    props: {
		device: {
            type: Object,
            required: true
        }
	},
    data() {
        var allOptions = ["FitBit Charge 3", "Foobot "];
        var chosenDeviceFields = [];
        var type = "";

        return {
            allOptions,
            chosenDeviceFields,
            type,
        }
    },
    methods: {
        getName(d) {
            return "device-modal-" + d.id;
        },
        activateChosenType(event) {
            if(event.target.value==this.allOptions[0]) {
                this.chosenDeviceFields = ["token","refresh_token"];
            } else if(event.target.value==this.allOptions[1]) {
                this.chosenDeviceFields = ["token","uuid","latitude","longitude"];
            } else {
                // this should never happen ...
            }
        },
        async onAdd() {
            /* Fields Validation */
            if(this.type == "") {
                this.showToast("Please choose a device type before submiting changes.", 2500);
                return;
            }
            var data = this.getData(this.type);
            if(this.validateFields(data) != 0) {

                return;
            }
            
            /* Server Validation */
            
            var result = await this.sendDevice(data, this.$store.getters.sessionToken);
            if(result) {
                if(result.status==0){ // device info retrieval successful
                    if(process.client) {
                        window.location.reload(true);
                    }
                } else {
                    this.showToast("Submission was invalid. Please make sure you fill in the fields correctly.", 5000);
                    return;
                }
            } else {
                // deal with error
                return;
            } 
        },
        async onUpdate() {
            /* Fields Validation */
            var data = this.getData(this.device.type);
            if(this.validateFields(data) != 0) {
                return;
            }
            
            /* Server Validation */
            var result = await this.updateDevice(data, this.$store.getters.sessionToken);
            if(result) {
                if(result.status==0){ // device info retrieval successful
                    if(process.client) {
                        window.location.reload(true);
                    }
                } else {
                    this.showToast("Submission was invalid. Please make sure you fill in the fields correctly.", 5000);
                    return;
                }
            } else {
                // deal with error
                return;
            } 
        },
        async onRemove() {
            /* Server Validation */
            var data = {'id': this.device.id};
            var result = await this.removeDevice(data, this.$store.getters.sessionToken);
            if(result) {
                if(result.status==0){ // device removal successful
                    if(process.client) {
                        window.location.reload(true);
                    }
                } else {
                    this.showToast("Error while completing the operation. Please check if the device has been removed, if not try again.", 5000);
                    return;
                }
            } else {
                // deal with error
                return;
            } 
        },
        async sendDevice(data,AuthToken) {
            
            const config = {
                headers: {'AuthToken': AuthToken},
            }
            return await this.$axios.$post("/devices", data, config)
                        .then(res => {
                            if(res.status != 0) {
                                if(res.status == 1) { 
                                    this.showToast(res.msg, 5000);
                                } else if(res.status == 4) {
                                    this.$toasted.show(res.msg, {position: 'bottom-center', duration: 7500});
                                    this.$disconnect()
                                    this.$nextTick(() => { 
                                        this.$store.dispatch('logout'),
                                        this.$router.push("/login")
                                    });
                                } else {
                                    this.showToast("Something went wrong while adding your device. Please try again later.", 5000);
                                }
                                console.log(res);
                                return null;
                            }
                            return res;
                        })
                        .catch(e => {
                            console.log(e);
                            this.showToast("Something went wrong while adding your device. The server might be down at the moment. Please try again later.", 7500);
                            return null;
                        });
        },
        async updateDevice(data,AuthToken) {
            const config = {
                headers: {'AuthToken': AuthToken},
            }
            return await this.$axios.$put("/devices", data, config)
                        .then(res => {
                            if(res.status != 0) {
                                console.log(res);
                                if(res.status == 4) {
                                    this.$toasted.show(res.msg, {position: 'bottom-center', duration: 7500});
                                    this.$disconnect()
                                    this.$nextTick(() => { 
                                        this.$store.dispatch('logout'),
                                        this.$router.push("/login")
                                    });
                                }
                                this.showToast("Something went wrong while updating your device. Please try again later.", 5000);
                                return null;
                            }
                            return res;
                        })
                        .catch(e => {
                            console.log(e);
                            this.showToast("Something went wrong while updating your device. The server might be down at the moment. Please try again later.", 7500);
                            return null;
                        });
        },
        async removeDevice(data,AuthToken) {
            const config = {
                headers: {'AuthToken': AuthToken, "Content-Type":"application/json"},
                data: data,
            }
            return await this.$axios.$delete("/devices", config)
                        .then(res => {
                            if(res.status != 0) {
                                console.log(res);
                                if(res.status == 4) {
                                    this.$toasted.show(res.msg, {position: 'bottom-center', duration: 7500});
                                    this.$disconnect()
                                    this.$nextTick(() => { 
                                        this.$store.dispatch('logout'),
                                        this.$router.push("/login")
                                    });
                                }
                                this.showToast("Something went wrong while removing your device. Please try again later.", 5000);
                                return null;
                            }
                            return res;
                        })
                        .catch(e => {
                            console.log(e);
                            this.showToast("Something went wrong while removing your device. The server might be down at the moment. Please try again later.", 7500);
                            return null;
                        });
        },
        getData(type) {
            var data = {};
            if(type == this.allOptions[0]) {
                data = {
                    'id': this.device.id,
                    'type': type,
                    'authentication_fields': {
                        'token': document.querySelector("input[name=token]").value, 
                        'refresh_token': document.querySelector("input[name=refresh_token]").value },
                }
            } else if (type == this.allOptions[1]) {
                 data = {
                    'id': this.device.id,
                    'type': type,
                    'authentication_fields': {
                        'uuid': document.querySelector("input[name=uuid]").value,
                        'token': document.querySelector("input[name=token]").value},
                    'latitude': document.querySelector("input[name=latitude]").value,
                    'longitude': document.querySelector("input[name=longitude]").value
                }
            } else {
                // this should never happen ...
            }
            return data;
        },
        validateFields(data) {
            // check if values are not empty
            var data_values = Object.values(data);
            for(var i=0; i<data_values.length; i++) {
                if(data_values[i] == null || data_values[i] == "") {
                    this.showToast("Please fill in the fields correctly.", 2500);
                    return -1;
                }
            }
            if(data.authentication_fields) {
                var data_auth_values = Object.values(data.authentication_fields);
                for(var i=0; i<data_auth_values.length; i++) {
                    if(data_auth_values[i] == null || data_auth_values[i] == "") {
                        this.showToast("Please fill in the fields correctly.", 2500);
                        return -1;
                    }
                }
            }
            // check if values are in the correct format
            if(data.latitude) {
                if(parseFloat(data.latitude)<-90 || parseFloat(data.latitude)>90) {
                    this.showToast("Latitude must follow the correct format!\n(ranges from -90.0 to 90.0)",2500);
                    return -2;
                }
                if(parseFloat(data.longitude)<-180 || parseFloat(data.longitude)>180) {
                    this.showToast("Longitude must follow the correct format!\n(ranges from -180.0 to 180.0)", 2500);
                    return -2;
                }
            }
            if(data.authentication_fields && data.authentication_fields.refresh_token) {
                if(data.authentication_fields.token == data.authentication_fields.refresh_token) {
                    this.showToast('Refresh Token must be different from the Token!', 2500);
                    return -3;
                }
            }
            return 0;
        },
        showToast(message, duration) {
            this.$toasted.show(message, {position: 'bottom-center', duration: duration});
        }
    },
}
</script>

<style>
    .size-modal-content {
        padding: 20px 20px 10px 20px;
        font-style: 13px;
    }
</style>
