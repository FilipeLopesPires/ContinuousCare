<template>
    <div v-if="loggedIn()">
        <HeaderMenuClient :activePage="activePage" />
    </div>
    <div v-else>
        <HeaderMenuDefault :activePage="activePage" />
    </div>
</template>

<script>
import HeaderInfo from '@/components/headers/HeaderInfo.vue'
import HeaderMenuDefault from '@/components/headers/HeaderMenuDefault.vue'
import HeaderMenuClient from '@/components/headers/HeaderMenuClient.vue'

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
        //HeaderMenuDoctor,
    },
    methods: {
        loggedIn() {
            //console.log("Token:")
            //console.log(this.$store.getters.sessionToken);
            if(this.$store.getters.isLoggedIn) {
                //console.log("not logged in")
                this.$nextTick(() => { this.$store.dispatch('setSessionToken', this.$store.getters.sessionToken) });
                return true
            }
            //console.log("logged in")
            this.$nextTick(() => { this.$store.dispatch('setSessionToken', this.$store.getters.sessionToken) });
            return false
        },
    }
}
</script>

<style>

</style>
