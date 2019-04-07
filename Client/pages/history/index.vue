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
                        <apexchart width="700" height="450" type="line" :options="chartOptions" :series="series"></apexchart>
                        <button class="genric-btn info" @click="updateChart">Update!</button>
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
        return {
            //jsonData: []
            chartOptions: {
            xaxis: {
                type: 'datetime',
                categories: ['01/01/2003', '02/01/2003','03/01/2003','04/01/2003','05/01/2003','06/01/2003','07/01/2003','08/01/2003'],
                },
            },
            series: [{
                name: 'Series A',
                data: [30, 40, 45, 50, 49, 60, 70, 91]
            }, {
                name: 'Series B',
                data: [23, 43, 54, 12, 44, 52, 32, 11]
            }]
        }
    },
    mounted() {
        /* var self = this;
        axios.get("https://reqres.in/api/users?page=2")
        //axios.get(process.env.base_url + "/pollution/lat=40/long=-8")
        .then( function(response) { 
            console.log(response.data);
            self.jsonData = response.data;
        })
        .catch( function(error) {
            self.jsonData = "An error occurred.\n" + error;
        }); */
    },
    methods: {
        /* onGoBack() {
            this.$router.push("/")
        } */
        generateDayWiseTimeSeries(baseval, count, yrange) {
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
        }
    },
    head: {
        title: "History"
    }
}
</script>

<style scoped>

</style>
