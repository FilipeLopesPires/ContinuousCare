<template>
    <div>
        <notifications group="permissions" style="margin-top:100px"/>
        <div v-if="this.$store.getters.isLoggedIn" >
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
    mounted: function(){
        if(this.$store.getters.getReloadControl==null && this.$store.getters.isLoggedIn){
            this.$store.dispatch("setVue", this)
            //console.log("Connecting to WebSocket");
            //this.$connect('ws://mednat.ieeta.pt:8344', {store:this.$store,reconnectionAttempts: 5,reconnectionDelay: 3000})
        }
    }
}
</script>

<style>

</style>
