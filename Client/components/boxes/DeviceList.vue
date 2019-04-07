<template>
    <div class="row">
        <DeviceBox v-for="device in devices"
        :key="device.id"
        :device="device.device"
        /> 
    </div>
</template>

<script>
import DeviceBox from '@/components//boxes/DeviceBox.vue'

export default {
    components: {
        DeviceBox,
    },
    props: {
        devices: {
            type: Array,
            required: true
        }
    },
}
</script>

<style>

</style>
