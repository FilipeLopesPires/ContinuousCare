<template>
    <div class="appointment-right">
        <form class="form-wrap" @submit.prevent="on_submit">
            <div class="row justify-content-center d-flex align-items-center">
                <div class="mt-10 col-lg-6 col-md-6 col-sm-6 single-team">
                    <date-picker class="single-input" v-model="date" id="date-picker-date" name="date" :config="datetimepicker_options" placeholder="Desired Date" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Desired Date'"></date-picker>
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
        </form>
    </div>
</template>
<script>
export default {
    name: 'TimeIntervalForm',
    data() {
        return {
            datetimepicker_options: {
                format: 'MMMM DD, YYYY',
                useCurrent: false,
                showClear: true,
                showClose: true,
            },
            date: null,
        }
    },
    methods: {
        on_submit() {
            this.$emit('sleep_interval_submit', this.date);
        },
        clearForm() {
            this.date = null;
            this.$emit('sleep_interval_clear');
        },
        showToast(message, duration) {
            this.$toasted.show(message, {position: 'bottom-center', duration: duration});
        }
    }
}
</script>
<style>
</style>
