<template>
  <section class="banner_area">
		<div class="banner_inner d-flex align-items-center">
			<div class="container">
				<div class="banner_content text-left">
					<h2 v-if="name == null">{{ page }}</h2>
					<h2 v-else>Hi {{ name }}!</h2>
					<div class="page_link">
						<nuxt-link to="/">{{ parent_page }}</nuxt-link>
						<nuxt-link to="/">{{ page }}</nuxt-link>
					</div>
				</div>
			</div>
		</div>
	</section>
</template>

<script>
export default {
	name: 'PageBanner',
	props: {
		parent_page: {
			type: String,
			required: true
		},
		page: {
			type: String,
			required: true
		},
		name: {
			type: String,
			required: false
		}
	}
}
</script>

<style>

</style>
