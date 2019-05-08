<template>
    <div v-if="this.$store.getters.isLoggedIn">
        <div v-if="this.$store.getters.isMedic">
            <HeaderMenuMedic :activePage="activePage" />
            
        </div>
        <div v-else>
            <HeaderMenuClient :activePage="activePage" />
        </div>
    </div>
    <div v-else>
        <HeaderMenuDefault :activePage="activePage" />
    </div>
</template>

<script>
import HeaderInfo from '@/components/headers/HeaderInfo.vue'
import HeaderMenuDefault from '@/components/headers/HeaderMenuDefault.vue'
import HeaderMenuClient from '@/components/headers/HeaderMenuClient.vue'
import HeaderMenuMedic from '@/components/headers/HeaderMenuMedic.vue'

export default {
    name: 'HeaderMenu',
    props: {
        activePage: {
			type: String,
			required: true
		},
    },
    components: {
        HeaderMenuDefault,
        HeaderMenuClient,
        HeaderMenuMedic,
    },
    methods: {
    }
}
</script>

<style>

</style>
