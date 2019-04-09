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
                    <select @change="activateChosenType($event)" v-bind="$attrs" v-on="$listeners" v-model="filledmodal.type" class="nice-select list">
                        <option class="option" value="" selected></option>
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
                    <input type="text" placeholder="" class="single-input"> 
                </div>
            </div>
            <div class="mt-10 row justify-content-center d-flex align-items-center">
                <div class="col-lg-6 col-md-6 row justify-content-center">
                </div>
                <div class="col-lg-3 col-md-3 row justify-content-right">
                    <button v-if="device.type!='Add Device'" class="genric-btn primary radius text-uppercase" @click="onRemove" >Remove</button>
                </div>
                <div class="col-lg-3 col-md-3 row justify-content-right">
                    <button v-if="device.type!='Add Device'" class="genric-btn info radius text-uppercase" @click="onUpdate" >Update</button>
                    <button v-else class="genric-btn info radius text-uppercase" @click="onAdd" >Add</button>
                </div>
            </div>
        </form>

    <!-- 
        Info:
        - Brand
        - Model
        - Token
        - Type
        - Supported Metrics
        Operations:
        - Update
        - Remove
    -->
    <!-- 
        Info:
        - Type (dos disponiveis)
        - Token
        Operations:
        - Add
     -->

    </modal>
</template>

<script>
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

        return {
            allOptions,
            chosenDeviceFields,
            filledmodal: {
                type: "",
                token: "",
                refresh_token: "",
                uuid: "",
                latitude: "",
                longitude: ""
            }
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
            }
        },
        async onAdd() {
            /* Fields Validation */
            // do something ...

            /* Server Validation */
            var result = await this.sendDevice(this.filledmodal, this.$store.getters.sessionToken);
            if(result.status==0){
                console.log("success");
                //this.$router.push("/devices");
            } else {
                // warn that device fields are invalid
            }
        },
        onUpdate() {
            // to do ...
        },
        onRemove() {
            // to do ...
        },
        async sendDevice(filledmodal,AuthToken) {
            console.log(AuthToken)
            const config = {
                headers: {'AuthToken': AuthToken},
                'type': filledmodal.type,
                'authentication_fields': {'token': filledmodal.token, 'refresh_token': filledmodal.refresh_token, 'uuid': filledmodal.uuid},
                'latitude': filledmodal.latitude,
                'longitude': filledmodal.longitude
            }
            return await this.$axios.$post("/devices",config)
                        .then(res => {
                            console.log(res)
                            return res;
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
