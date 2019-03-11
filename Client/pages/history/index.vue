<template>
    <div class="history_page">
        <h1>History Page</h1>
        <p> {{ jsonData }} </p>
    </div>
</template>

<script>
import axios from "axios"

export default {
    data() {
        return {
            //jsonData: this.loadExternalData()
            jsonData: []
        }
    },
    mounted() {
        var self = this;
        //axios.get("https://reqres.in/api/users?page=2")
        axios.get("http://192.168.43.136:5000/pollution/lat=40/long=-8")
        .then( function(response) {
            console.log(response.data.data);
            self.jsonData = response.data.data;
        })
        .catch( function(error) {
            self.jsonData = "An error occurred.\n" + error;
        });
    },
    layout: "client"
}
</script>

<style>
.history_page {
    padding: 30px;
}
</style>
