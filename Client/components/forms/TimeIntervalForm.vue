<template>
    <div class="appointment-right">
        <form class="form-wrap" @submit.prevent="on_submit">
            <div class="row justify-content-center d-flex align-items-center">
                <div class="mt-10 col-lg-6 col-md-6 col-sm-6 single-team">
                    <date-picker class="single-input" v-model="start" id="date-picker-start" name="start" :config="datetimepicker_options" placeholder="Start Time" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Start Time'"></date-picker>
                </div>
                <div class="mt-10 col-lg-6 col-md-6 col-sm-6 single-team">
                    <date-picker class="single-input" v-model="end" id="date-picker-end" name="end" :config="datetimepicker_options" placeholder="End Time" onfocus="this.placeholder = ''" onblur="this.placeholder = 'End Time'"></date-picker>
                </div>
            </div>
            <div class="row justify-content-center d-flex align-items-center">
                <div class="mt-10 col-lg-6 col-md-6 col-sm-12 col-xs-12 form-inline form-select">
                    <input class="single-input col-lg-7 col-md-7 col-sm-7 col-xs-7 " v-model="interval" type="number" step=1 min=0 name="interval" id="date-picker-interval" placeholder="Time Interval" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Time Interval'" style="font-size:16px">
                    <select class="nice-select list col-lg-5 col-md-5 col-sm-5 col-xs-5 " ref="time_unit_select"> <!-- class="col-md-5 custom-select"  -->
                        <option class="single-input option " :value="null" selected>Unit</option>
                        <option class="option" value="s">seconds</option>
                        <option class="option" value="m">minutes</option>
                        <option class="option" value="h">hours</option>
                        <option class="option" value="d">days</option>
                        <option class="option" value="w">weeks</option>
                    </select>
                </div>
                <div class="mt-10 col-lg-6 col-md-6 col-sm-12 col-xs-12 single-team">
                    <div class="row">
                        <div class="container col-lg-6 col-md-6 col-sm-6 ">
                            <button class="genric-btn primary medium text-uppercase col-lg-12 col-md-12 col-sm-12 " type="button" @click="clearForm">Clear</button>
                        </div>
                        <div class="container col-lg-6 col-md-6 col-sm-6 ">
                            <button class="genric-btn info medium text-uppercase col-lg-12 col-md-12 col-sm-12 " type="submit">Load</button>
                        </div>
                    </div>
                    
                </div>
            </div>
            <!-- <div class="row justify-content-center d-flex align-items-center">
                <div class="mt-10 col-lg-6"><p></p></div>
                <div class="mt-10 col-lg-6">
                    <button class="genric-btn success medium text-uppercase" type="submit">Load Data</button>
                </div>
            </div> -->
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
            if(interval_unit == "") { interval_unit = null; }

            if ((interval_unit !== null) && (this.interval === null || this.interval === '')) {
                this.showToast("Please insert a corret value for the interval.", 2500);
                return;
            }
            if ((this.interval != null && this.interval != 0) && (interval_unit == null)) {
                this.showToast("Please choose an interval unit.", 2500);
                return;
            }
            if(this.interval == null && interval_unit == null) {
                this.$emit('time_interval_submit', this.start, this.end, null);
            } else {
                this.$emit('time_interval_submit', this.start, this.end, this.interval + interval_unit);
            } 
        },
        clearForm() {
            document.getElementById("date-picker-start").value = null;
            document.getElementById("date-picker-end").value = null;
            document.getElementById("date-picker-interval").value = null;
            this.$emit('time_interval_clear');
        },
        showToast(message, duration) {
            this.$toasted.show(message, {position: 'bottom-center', duration: duration});
        }
    }
}
</script>
<style>
</style>
