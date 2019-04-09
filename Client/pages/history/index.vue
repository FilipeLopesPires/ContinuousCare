<template>
    <div>
        <body>
            <!--================ Header Menu Area =================-->
            <HeaderMenu activePage="History" />

            <!--================ Banner Area =================-->
            <PageBanner parent_page="Home" page="History" />

            <!--================ Testing Area =================-->
            <!-- <div class="testing">
                <p> {{ jsonData }} </p>
            </div> -->

            <!--================ Graphics Area =================-->
                <div class="row justify-content-center d-flex align-items-center col-lg-12 ">
                    <div class="blog_right_sidebar">
                        <apexchart v-if="showChart" id="apexchart-line" width="700" height="450" type="line" :options="chartOptions" :series="series"></apexchart>
                        <div v-else><h1>Unable to load information.</h1></div>
                        <!-- <button class="genric-btn info" @click="updateChart">Update!</button> -->
                        <PaginationBox />
                    </div>
                </div>

            <!--================ Footer Area =================-->
            <PageFooter />

        </body>
        <nuxt/>
    </div>
</template>

<script>
import Vue from 'vue'
import VueApexCharts from 'vue-apexcharts'
Vue.component('apexchart', VueApexCharts)
Vue.use(VueApexCharts)

import PaginationBox from '@/components/boxes/PaginationBox.vue'

export default {
    components: {
        PaginationBox,
    },
    data() {
        /* var answer = {"status": 0, "error": "Successfull operation.", 
                    "data": { "time":["2019-04-07T20:28:47Z","2019-04-07T20:28:57Z","2019-04-07T20:28:67Z","2019-04-07T20:28:77Z","2019-04-07T20:28:87Z"],  
                            "latitude": [40,40], "longitude": [-8,-8], 
                            "aqi": [16,20,null,21,22], "no2": [4.2,4.2,4.2,4.2,4.2], "o3": [20.8,20.8], "p": [1013.2,1013.2], "pm10": [5,5], "pm25": [7,7], "so2": [1.6,1.6], "t": [10.5,10.5]
                    }}; 
        var environment = answer.data; */

        /* var environment = {"time":[], "latitude": [], "longitude": [], 
                        "aqi": [], "no2": [], "o3": [], "p": [], "pm10": [], "pm25": [], "so2": [], "t": []}; */
        
        var requestError = false;
        var showChart = false;
        var serverData = {}
        return {
            showChart,
            requestError,
            serverData,

            chartOptions: {
                xaxis: {
                    /* type: 'seconds',
                    categories: environment.time, */
                },
            },
            series: [{
                /* name: 'AQI',
                data: environment.aqi, */
            }]
        }
    },
    async mounted() {
        //this.$axios.$get("https://reqres.in/api/users?page=2")

        await this.getServerData('1554745367', this.$store.getters.sessionToken, "/healthstatus")
        if(!this.requestError) {
            console.log("no error")
            this.showChart = true;
            var chartOptions = {
                xaxis: {
                    type: 'seconds',
                    categories: this.serverData.time,
                },
            };
            var series = []
            for(var metric in this.serverData) {
                if(metric!='time' & metric!='latitude' & metric!='longitude') {
                    series.push({
                        name: metric,
                        data: this.serverData[metric],
                    })
                }
            }
            this.chartOptions = chartOptions;
            this.series = series;
        }
    },
    methods: {
        async getServerData(start,AuthToken,restPath) {
            const config = {
                params: {'start': start},
                headers: {'AuthToken': AuthToken}
            }
            //console.log("inside)" + this.showChart);
            this.serverData = await this.$axios.$get(restPath,config)
                                .then(res => {
                                    if(res.status != 0) {
                                        this.requestError = true;
                                        return {};
                                    }
                                    return res.data;
                                })
                                .catch(e => {
                                    this.requestError = true;
                                    return {};
                                });
        }
        /* onGoBack() {
            this.$router.push("/")
        } */
        /* generateDayWiseTimeSeries(baseval, count, yrange) {
            var i = 0;
            var series = [];
            while (i < count) {
            var x = baseval;
            var y = Math.floor(Math.random() * (yrange.max - yrange.min + 1)) + yrange.min;

            series.push([x, y]);
            baseval += 86400000;
            i++;
            }
            return series;
        },
        updateChart() {
            let series = [{
                name: 'South',
                data: this.generateDayWiseTimeSeries(new Date('11 Feb 2017').getTime(), 20, {min: 10, max: 60})
            },
            {
                name: 'North',
                data: this.generateDayWiseTimeSeries(new Date('11 Feb 2017').getTime(), 20, {min: 10, max: 20})
            },
            {
                name: 'Central',
                data: this.generateDayWiseTimeSeries(new Date('11 Feb 2017').getTime(), 20, {min: 10, max: 15})
            }]
            this.series = series
        } */
    },
    head: {
        title: "History"
    }
}
</script>

<style scoped>

</style>
