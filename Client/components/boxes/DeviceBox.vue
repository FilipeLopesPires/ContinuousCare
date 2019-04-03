<template>
    <div class="col-lg-4">
        <div class="categories_post">
        <img :src="photo" alt="Procedure" height="200px" width="200px">
        <div class="categories_details">
            <div class="categories_text">
            <div class="border_line"></div>
            <a href="#">
                <h5>{{ name }}</h5>
            </a>
            <div class="border_line"></div>
            </div>
        </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'DeviceBox',
    props: {
		photo: {
			type: String,
			required: true
		},
		name: {
			type: String,
			required: true
		}
	}
}
</script>

<style>

</style>
