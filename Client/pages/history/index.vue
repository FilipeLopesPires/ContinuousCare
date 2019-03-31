<template>
    <div>
        <!--================ HTML Header =================-->
        <HeaderHTML page="History" />

        <body>
            <!--================ Header Menu Area =================-->
            <HeaderMenu />

            <!--================ Banner Area =================-->
            <PageBanner parent_page="Home" page="History" />

            <!--================ Content Area =================-->
            <div class="testing">
                <p> {{ jsonData }} </p>
            </div>

            <!--================ Footer Area =================-->
            <PageFooter />

        </body>
        <nuxt/>
    </div>
</template>

<script>
import HeaderHTML from '@/components/headers/HeaderHTML.vue'
import HeaderMenu from '@/components/headers/HeaderMenu.vue'
import PageBanner from '@/components/banners/PageBanner.vue'
import PageFooter from '@/components/footers/PageFooter.vue'

import axios from "axios"

export default {
    components: {
        HeaderHTML,
        HeaderMenu,
        PageBanner,
        PageFooter
    },
    data() {
        return {
            jsonData: []
        }
    },
    mounted() {
        var self = this;
        axios.get("https://reqres.in/api/users?page=2")
        //axios.get("http://192.168.43.136:5000/pollution/lat=40/long=-8")
        .then( function(response) { 
            console.log(response.data);
            self.jsonData = response.data;
        })
        .catch( function(error) {
            self.jsonData = "An error occurred.\n" + error;
        });
    },
    methods: {
        onGoBack() {
        this.$router.push("/")
        }
    }
}
</script>

<style scoped>

</style>
