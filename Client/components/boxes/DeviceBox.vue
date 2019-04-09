<template>
    <div class="col-lg-4 col-md-4 col-sm-6">
        <DeviceModal :device="device" />
        <div class="categories_post">
            <img :src="device.photo" alt="Procedure" height="200px" width="200px" >
            <div class="categories_details" @click="showModal($modal, device.token)">
                <div class="categories_text">
                    <div class="border_line"></div>
                        <h5>{{ device.type }}</h5>
                    <div class="border_line"></div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Vue from 'vue'
import VModal from 'vue-js-modal/dist/ssr.index'
Vue.use(VModal)
import DeviceModal from '@/components/modals/DeviceModal.vue'

export default {
    name: 'DeviceBox',
    components: {
        DeviceModal,
    },
    props: {
        device: {
            type: Object,
            required: true
        },
    },
    methods: {
        showModal($modal, token) {
            var device_modal = "device-modal-" + token;
            $modal.show(device_modal);
        }
    }
}
</script>

<style>

</style>
