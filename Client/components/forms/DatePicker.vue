<template>
    <div class=""><!-- placeholder="Date of Birth *" -->
        <datepicker :readonly="true" format="YYYY-MM-DD" name="birthdate" placeholder="Date of Birth *"></datepicker>
    </div>
</template>

<script>
import datepicker from 'vue-date-picker'

export default {
    components: {
        datepicker
    },
};
</script>

<style>

</style>
