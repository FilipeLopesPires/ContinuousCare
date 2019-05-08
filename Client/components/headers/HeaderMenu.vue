<template>
    <div v-if="loggedIn()">
        <div v-if="regularAccount()">
            <HeaderMenuClient :activePage="activePage" />
        </div>
        <div v-else>
            <HeaderMenuMedic :activePage="activePage" />
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
        loggedIn() {
            if(this.$store.getters.isLoggedIn) {
                this.$nextTick(() => { this.$store.dispatch('setSessionToken', this.$store.getters.sessionToken) });
                return true
            }
            this.$nextTick(() => { this.$store.dispatch('setSessionToken', this.$store.getters.sessionToken) });
            return false
        },
        regularAccount() {
            var retval = false;
            this.$nextTick(() => { 
                if(this.$store.getters.userType == "client") {
                    retval = true;
                }
            });
            return retval;
        }
    }
}
</script>

<style>

</style>
