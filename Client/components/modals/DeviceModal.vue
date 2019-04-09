<template>
    <modal 
        :name="getName(device.authentication_fields)"
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
            <div class="mt-10">
                <h5>Type:</h5>
                <div class="form-select" id="service-select">
                    <select class="nice-select list">
                        <option class="option" value="1" selected>Foobot</option>
                        <option class="option" value="2">Fitbit Charge 3</option>
                    </select>
                </div>
            </div>
            <!-- <div class="mt-10" v-for="af in device.authentication_fields" :key="af.id" :af="af.af"> 
                <h5 v-if="isDevice(device.token)">{{ af[0] }}:</h5>
                <input v-if="isDevice(device.token)" type="text" :name="af[0]" :placeholder="af[1]" onfocus="this.placeholder = ''" onblur="this.placeholder = ''" class="single-input"> 
            </div> -->
            <!-- <div class="mt-10">
                <h5 v-if="isDevice(device.token)">Supported Metrics:</h5>
                <p class="single-input" name="supported_metrics_field"> {{ supported_metrics_toString(device.supported_metrics) }} </p>
            </div> -->
            <!-- Buttons -->
            <div class="mt-10 row justify-content-center d-flex align-items-center">
                <div class="col-lg-6 col-md-6 row justify-content-center">
                </div>
                <div class="col-lg-3 col-md-3 row justify-content-right">
                    <button class="genric-btn primary radius text-uppercase" @click="onRemove" v-if="isDevice(device.token)">Remove</button>
                </div>
                <div class="col-lg-3 col-md-3 row justify-content-right">
                    <button class="genric-btn info radius text-uppercase" @click="onUpdate" v-if="isDevice(device.token)">Update</button>
                    <button class="genric-btn info radius text-uppercase" @click="onAdd" v-if="!isDevice(device.token)">Add</button>
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
    methods: {
        getName(af) {
            return "device-modal-" + af[0];
        },
        onAdd() {
            //this.$emit('add_device',this.)
        },
        onUpdate() {
            
        },
        onRemove() {

        },
        isDevice(af) {
            if (af==['','']) {
                /* console.log(authentication_fields); */
                return false
            } 
            return true
        },
        /* supported_metrics_toString(sm) {
            var result = "";
            if (sm.length>0){
                for(var i=0; i<sm.length; i++) {
                    if(i==sm.length-1) {
                        result = result + sm[i];
                    } else {
                        result = result + sm[i] + ", ";
                    }
                }
            }
            return result;
        } */
    },
    props: {
		device: {
            type: Object,
            required: true
        }
	}
}
</script>

<style>
    .size-modal-content {
        padding: 20px 20px 10px 20px;
        font-style: 13px;
    }
</style>
