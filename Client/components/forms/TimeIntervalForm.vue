<template>
    <div class="appointment-right">
        <form class="form-wrap" @submit.prevent="on_submit">
            <div class="mt-10">
                <date-picker class="single-input" v-model="start" name="start" :config="datetimepicker_options" placeholder="Start Time" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Start Time'"></date-picker>
            </div>
            <div class="mt-10">
                <date-picker class="single-input" v-model="end" name="end" :config="datetimepicker_options" placeholder="End Time" onfocus="this.placeholder = ''" onblur="this.placeholder = 'End Time'"></date-picker>
            </div>
            <div class="mt-10 form-inline">
                <input class="single-input col-md-7" v-model="interval" type="number" step=1 min=0 name="interval" placeholder="Time Interval" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Time Interval'" style="font-size:16px">
                <select ref="time_unit_select" class="col-md-5 custom-select">
                    <option :value="null">Time unit</option>
                    <option value="s">seconds</option>
                    <option value="m">minutes</option>
                    <option value="h">hours</option>
                    <option value="d">days</option>
                    <option value="w">weeks</option>
                </select>
            </div>
            <div class="row justify-content-center d-flex align-items-center">
                <div class="mt-10 col-lg-6"><p></p></div>
                <div class="mt-10 col-lg-6">
                    <button class="genric-btn success medium text-uppercase" type="submit">Load Data</button>
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
                format: 'MMMM DD, YYYY h:mm:ss',
                useCurrent: false,
                showClear: true,
                showClose: true,
            },
            start: null,
            end: null,
            interval: null
        }
    },
     methods: {
        on_submit() {
            let interval_unit = this.$refs.time_unit_select.value;
            if ((interval_unit !== null && interval_unit !== "") && (this.interval === null || this.interval === '')) {
                this.showToast("Please insert a corret value for the interval.", 2500);
                return;
            }
            if ((this.interval !== null && this.interval !== '') && (interval_unit === null || interval_unit === "")) {
                this.showToast("Please choose an interval unit.", 2500);
                return;
            }
            this.$emit('time_interval_submit', this.start, this.end, this.interval + interval_unit);
        },
        showToast(message, duration) {
            this.$toasted.show(message, {position: 'bottom-center', duration: duration});
        }
    }
}
</script>
<style>
</style>