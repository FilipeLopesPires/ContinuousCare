<template>
    <div>
        <body>
            <!--================ Header Menu Area =================-->
            <HeaderMenu activePage="History" />

            <!--================ Banner Area =================-->
            <PageBanner parent_page="Home" page="History" />

            <!--================ Graphics Area =================-->
            <!-- <div class="row justify-content-center d-flex align-items-center col-lg-12 ">
                <div class="blog_right_sidebar">
                    <form class="form-wrap" @submit.prevent="onLoadChart">
                        <div class="mt-10">
                            <input class="single-input" v-bind="$attrs" v-on="$listeners" v-model="filledform.start" type="text" name="start" placeholder="Start Time" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Start Time'">
                        </div>
                        <div class="mt-10">
                            <input class="single-input" v-bind="$attrs" v-on="$listeners" v-model="filledform.end" type="text" name="end" placeholder="End Time" onfocus="this.placeholder = ''" onblur="this.placeholder = 'End Time'">
                        </div>
                        <div class="mt-10">
                            <input class="single-input" v-bind="$attrs" v-on="$listeners" v-model="filledform.interval" type="text" name="interval" placeholder="Time Interval" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Time Interval'">
                        </div>
                        <div class="row justify-content-center d-flex align-items-center">
                            <div class="mt-10 col-lg-6">
                                <button class="genric-btn success medium text-uppercase" type="submit">Load Chart</button>
                            </div>
                            <div class="mt-10 col-lg-6">
                                <button class="genric-btn primary medium text-uppercase" type="button" @click="changeChartSource">Change Source</button>
                            </div>
                        </div>
                    </form>
                    <div><p></p></div>
                    <apexchart v-if="showChart" id="apexchart-line" width="700" height="450" type="line" :options="chartOptions" :series="series"></apexchart>
                    <div v-else><h1>Unable to load information.</h1></div>
                </div>
            </div> -->

            <!--================ Map Area =================-->
            <LeafletMap />
            
            <!--================ Footer Area =================-->
            <PageFooter />

        </body>
        <nuxt/>
    </div>
</template>

<script>

// https://uicookies.com/horizontal-timeline/
// https://www.npmjs.com/package/vue-horizontal-timeline

//import PaginationBox from '@/components/boxes/PaginationBox.vue'
import LeafletMap from '@/components/maps/LeafletMap.vue'

export default {
    middleware: ['check-log', 'log', 'clients-only'],
    components: {
        //PaginationBox,
        LeafletMap,
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
        
        var chartSource = "/healthstatus";
        
        var requestError = false;
        var showChart = false;
        var serverData = {};

        const example1 = {
            title: 'Title example 1',
            content: 'Lorem ipsum dolor sit amet.'
        };
        const example2 = {
            title: 'Title example 2',
            content: 'Lorem ipsum dolor sit amet.'
        };
        const example3 = {
            title: 'Title example 3',
            content: 'Lorem ipsum dolor sit amet.'
        };
        const items = [example1, example2, example3];

        return {
            chartSource,

            showChart,
            requestError,
            serverData,

            filledform: {
                start: null,
                end: null,
                interval: null,
            },

            chartOptions: {
                xaxis: {
                    /* type: 'seconds',
                    categories: environment.time, */
                },
            },

            series: [{
                /* name: 'AQI',
                data: environment.aqi, */
            }],

            items,
        }
    },
    async mounted() {
        //this.$axios.$get("https://reqres.in/api/users?page=2")
        this.onLoadChart()
        /* await this.getServerData(this.filledform.start, this.filledform.end, this.filledform.interval, this.$store.getters.sessionToken, "/healthstatus")
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
        } */
    },
    methods: {
        async onLoadChart() {
            await this.getServerData(this.filledform.start, this.filledform.end, this.filledform.interval, this.$store.getters.sessionToken, this.chartSource)
            if(!this.requestError) {
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
        async getServerData(start,end,interval,AuthToken,restPath) {
            const config = {
                params: {'start': start, 'end': end, 'interval': interval},
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
                                    // Unable to get devices from server
                                    this.$toasted.show('Something went wrong while trying to retrieve data. The server might be down at the moment. Please try again later.', 
                                        {position: 'bottom-center', duration: 7500});
                                    this.requestError = true;
                                    return {};
                                });
        },
        changeChartSource() {
            if(this.chartSource == "/healthstatus") {
                this.chartSource = "/environment";
            } else {
                this.chartSource = "/healthstatus";
            }
            this.onLoadChart();
        },
        onClickTimeline(content) {
            console.log(content)
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
.timeline-div {
    height: 300px;
}
.timeline {
    height: 300px;
}
</style>
