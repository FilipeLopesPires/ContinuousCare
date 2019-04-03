<template>
    <div class=""><!-- placeholder="Date of Birth *" -->
        <datepicker value="birthdate" :readonly="false" format="DD-MM-YYYY" name="birthdate" placeholder="Date of Birth *"></datepicker>
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
