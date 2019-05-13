<template>
    <div class="appointment-right">
        <form class="form-wrap">
            <div class="mt-10">
                <date-picker class="single-input" v-model="start" name="start" :config="datetimepicker_options" placeholder="Start Time" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Start Time'"></date-picker>
            </div>
            <div class="mt-10">
                <date-picker class="single-input" v-model="end" name="end" :config="datetimepicker_options" placeholder="End Time" onfocus="this.placeholder = ''" onblur="this.placeholder = 'End Time'"></date-picker>
            </div>
            <div class="mt-10">
                <input class="single-input" v-model="interval" name="interval" placeholder="Time Interval" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Time Interval'" style="font-size:16px">
            </div>
            <div class="row justify-content-center d-flex align-items-center">
                <div class="mt-10 col-lg-6"><p></p></div>
                <div class="mt-10 col-lg-6">
                    <button @click="$emit('time_interval_submit', start, end, interval)" class="genric-btn success medium text-uppercase" type="button">Load Data</button>
                </div>
            </div>
        </form>
    </div>
</template>

<script>
export default {
    name: 'TimeIntervalForm',
    data() {
        return {
            datetimepicker_options: {
                format: 'DD/MM/YYYY h:mm:ss',
                useCurrent: false,
                showClear: true,
                showClose: true,
            },
            start: null,
            end: null,
            interval: null
        }
    }
}
</script>

<style>

</style>
