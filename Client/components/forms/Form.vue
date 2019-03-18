<template>
    <div class="appointment-right">
        <form class="form-wrap" action="#">
            <h3 class="pb-20 text-center mb-20">Book an Appointment</h3>
            <input type="text" class="form-control" name="name" placeholder="Patient Name" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Patient Name'">
            <input type="text" class="form-control" name="phone" placeholder="Phone " onfocus="this.placeholder = ''" onblur="this.placeholder = 'Phone'">
            <input type="email" class="form-control" name="email" placeholder="Email Address" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Email Address'">
            <input id="datepicker1" name="dop" class="dates form-control" placeholder="Date of Birth" type="text">
            <div class="form-select" id="service-select">
            <select>
                <option data-display="">Disease Type</option>
                <option value="1">Type One</option>
                <option value="2">Type Two</option>
                <option value="3">Type Three</option>
                <option value="4">Type Four</option>
            </select>
            </div>
            <input id="datepicker2" class="dates form-control" placeholder="appointment Date" type="text">
            <textarea name="messege" class="" rows="5" placeholder="Messege" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Messege'"></textarea>
            <div class="text-center confirm_btn_box">
            <button class="main_btn text-uppercase">Confirm Booking</button>
            </div>
        </form>
    </div>
</template>

<script>
export default {

}
</script>

<style>

</style>
