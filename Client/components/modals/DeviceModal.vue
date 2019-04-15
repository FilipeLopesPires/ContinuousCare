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
        <form class="size-modal-content" >
            <!-- Info -->
            <h3 class="title_color text-center" >{{ device.type }}</h3>
            <div v-if="device.type=='Add Device'" class="mt-10">
                <h5>Type:</h5>
                <div class="form-select" id="service-select">
                    <select @change="activateChosenType($event)" v-bind="$attrs" v-on="$listeners" v-model="type" class="nice-select list">
                        <option class="option" value="" selected>Choose Type</option>
                        <option class="option" v-for="option in allOptions" :key="option.id" :value="option">{{ option }}</option>
                    </select>
                </div>
            </div>
            <div v-if="device.type!='Add Device'">
                <div class="mt-10" v-for="field in Object.keys(device)" :key="field.id" :field="field"> 
                    <h5 v-if="field != 'photo' && field != 'type' && field != 'id'">{{ field }}:</h5>
                    <input v-if="field != 'photo' && field != 'type' && field != 'id'" type="text" :value="device[field]" :placeholder="device[field]" class="single-input"> 
                </div>
            </div>
            <div v-else>
                <div class="mt-10" v-for="field in chosenDeviceFields" :key="field.id" :field="field"> 
                    <h5 >{{ field }}:</h5>
                    <input type="text" placeholder="" :name="field" class="single-input"> 
                </div>
            </div>
            <div class="mt-10 row justify-content-center d-flex align-items-center">
                <div class="col-lg-6 col-md-6 row justify-content-center">
                </div>
                <div class="col-lg-3 col-md-3 row justify-content-right">
                    <button v-if="device.type!='Add Device'" class="genric-btn primary radius text-uppercase" @click="onRemove" type="button" >Remove</button>
                </div>
                <div class="col-lg-3 col-md-3 row justify-content-right">
                    <button v-if="device.type!='Add Device'" class="genric-btn info radius text-uppercase" @click="onUpdate" type="button" >Update</button>
                    <button v-else class="genric-btn info radius text-uppercase" @click="onAdd" type="button" >Add</button>
                </div>
            </div>
        </form>
    </modal>
</template>

<script>
/* 
import VModal from 'vue-js-modal'
Vue.component('vmodal', VModal)
Vue.use(VModal) */
import Vue from 'vue'
import VModal from 'vue-js-modal'
Vue.component('vmodal', VModal)
Vue.use(VModal)

import BasicTable from '@/components/tables/BasicTable.vue'

export default {
    name: 'DeviceModal',
    components: {
        BasicTable,
    },
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
            return "device-modal-" + d.token;
        },
        activateChosenType(event) {
            //console.log(event.target.value)
            if(event.target.value==this.allOptions[0]) {
                this.chosenDeviceFields = ["token","refresh_token"];
            } else if(event.target.value==this.allOptions[1]) {
                this.chosenDeviceFields = ["token","uuid","latitude","longitude"];
            } else {
                // error ...
            }
        },
        async onAdd() {
            /* Fields Validation */
            // do something ...

            /* Server Validation */
            var result = await this.sendDevice(this.type, this.$store.getters.sessionToken);
            if(result.status==0){
                console.log("success");
                this.$router.push("/devices");
            } else {
                // error ... warn that device fields are invalid
            }
        },
        onUpdate() {
            // to do ...
        },
        onRemove() {
            // to do ...
        },
        async sendDevice(type,AuthToken) {
            const config = {
                headers: {'AuthToken': AuthToken},
            }
            var data = {}
            if(type == this.allOptions[0]) {
                data = {
                    'type': type,
                    'authentication_fields': {
                        'token': document.querySelector("input[name=token]").value, 
                        'refresh_token': document.querySelector("input[name=refresh_token]").value },
                }
            } else if (type == this.allOptions[1]) {
                 data = {
                    'type': type,
                    'authentication_fields': {
                        'uuid': document.querySelector("input[name=uuid]").value,
                        'token': document.querySelector("input[name=token]").value},
                    'latitude': parseFloat(document.querySelector("input[name=latitude]").value),
                    'longitude': parseFloat(document.querySelector("input[name=longitude]").value)
                }
            } else {
                // error ...
            }
            console.log(data);
            return await this.$axios.$post("/devices", data, config)
                        .then(res => {
                            console.log(res)
                            return res;
                        })
                        .catch(e => {
                            // error ...
                        });
        },
    },
}
</script>

<style>
    .size-modal-content {
        padding: 20px 20px 10px 20px;
        font-style: 13px;
    }
</style>
