<template>
    <div class="sleep-box">
        <div class="container">
            <div v-if="received_date">
                <p class="sample-text">You slept for {{sleep_time}} hours.</p>
            </div>
            <div v-else>
                <h5 class="text-heading title_color">Last night's review:</h5>
                <p class="sample-text mt--10">You slept for {{sleep_time}} hours.</p>
            </div>
            <p class="sample-text">Check out your pattern bellow.</p>
        </div>
        <apexchart id="sleep-box" width="100%" height="100%" type="line" :options="charts_options" :series="series"></apexchart>
    </div>
</template>

<script>
export default {
    props: {
        patient: {
            type: String,
            required: false,
            default: null
        },
        date: {
            type: Number,
            required: false
        },
    },
    data() {
        var series = [{
            name: 'Levels',
            data: [],
        }];
        return {
            sleep_time: 0,
            series,
            received_date: false,
            charts_options: {
                chart: {
                    height: 100,
                    type: 'line',
                    shadow: { enabled: false, color: '#bbb', top: 3, left: 2, blur: 3, opacity: 1 },
                },
                /* title: {
                    text: 'Sleep Pattern',
                    align: 'left',
                    offsetX: 30,
                    style: {
                        fontSize: "32px",
                        color: '#3face4'
                    }
                }, */
                fill: {
                    type: 'gradient',
                    gradient: {
                        shade: 'dark',
                        gradientToColors: ['#f8b600'],
                        shadeIntensity: 1,
                        type: 'vertical',
                        opacityFrom: 1,
                        opacityTo: 1,
                        stops: [0, 100, 100]
                    },
                },
                stroke: {
                    width: 7,   
                    curve: 'smooth'
                },
                markers: {
                    size: 5,
                    opacity: 1,
                    colors: ["#f8b600"],
                    strokeColor: "#fff",
                    strokeWidth: 2,
                        
                    hover: {
                        size: 7,
                    }
                },
                tooltip: {
                    x: {
                        format: 'dd MMM HH:mm'
                    },
                    y: {
                        formatter: (value) => {
                            if(value==4) {
                                return "Awake";
                            }
                            if(value==3) {
                                return "Light Sleep";
                            }
                            if(value==2) {
                                return "Rem Sleep";
                            }
                            return "Deep Sleep";
                        },
                    }
                },
                xaxis: {
                    type: 'datetime',
                    title: {
                        text: 'Time',
                    },
                    labels: {
                        formatter: value => {
                            var d = new Date(value);
                            return this.format_number(d.getHours()) + ":" + this.format_number(d.getMinutes());
                        },
                        tickPlacement: 'between'
                    },
                    tickAmount: 'dataPoints'
                },
                yaxis: {
                    min: 1,
                    max: 4,
                    tickAmount: 3,
                    title: {
                        text: 'Sleep Levels',
                    },                
                }
            }
        }
    },
    async mounted() {
        this.updateChart(this.date);
    },
    methods: {
        async getSleep(AuthToken, date) {
            let config = {
                headers: {'AuthToken': AuthToken},
                params: {}
            };

            if (this.patient) {
                config.params.patient = this.patient;
            }

            if (!date) {
                this.received_date = false;
                let now = parseInt(Date.now() / 1000);

                /*
                 * Here I assign the same value to both fields because
                 *  1. only the date part is taken into account (seconds and minutes are discarded)
                 *  2. internaly the server does "begin_date_column >= start_date AND end_date_column <= end_date"
                 *      what returns all sleep sessions from the current day
                 */
                config.params.start = now;
                config.params.end = now;
            }
            else {
                this.received_date = true;
                config.params.start = date;
                config.params.end = date;
            }

            return await this.$axios.$get("/sleep",config)
                                .then(res => {
                                    if(res.status != 0) {
                                        if(res.status == 1) {
                                            this.showToast(res.msg, 7500);
                                        } else if(res.status == 4) {
                                            this.$toasted.show(res.msg, {position: 'bottom-center', duration: 7500});
                                            this.$disconnect()
                                            this.$nextTick(() => { 
                                                this.$store.dispatch('logout'),
                                                this.$router.push("/login")
                                            });
                                        } else {
                                            console.log("Error status: ", res.status);
                                            console.log("Message: ", res.msg);
                                            this.showToast("Something went terribly wrong while trying to retrieve your sleep log. Please try again later or contact us through email.", 7500);
                                        }
                                        return null;
                                    }
                                    return res;
                                })
                                .catch(e => {
                                    // Unable to get devices from server
                                    this.showToast("Something went wrong while trying to retrieve your sleep log. The server might be down at the moment. Please try again later.", 7500);
                                    console.log(e);
                                    return null;
                                });
        },

        showToast(message, duration) {
            this.$toasted.show(message, {position: 'bottom-center', duration: duration});
        },

        /**
         * Function used to force the update of the chart
         * Used by
         *  1. mounted()
         *  2. whenever the date is changed. See method sleep_interval_submit_handler of patients page
         */
        async updateChart(date) {
            var result = await this.getSleep(this.$store.getters.sessionToken, date);
            if(result) {
                if(result.status==0) {
                    let sleepSessions = result.data;
                    let mostRecentSleepSession = sleepSessions[sleepSessions.length - 1];
                    if(sleepSessions &&  sleepSessions.length>0 && mostRecentSleepSession.data && mostRecentSleepSession.data.level && mostRecentSleepSession.data.level.length>0) {
                        // process sleep session
                        let h = parseInt(mostRecentSleepSession.info.duration/60/60,10);
                        let m = parseInt((mostRecentSleepSession.info.duration/60/60-h)*60,10);
                        this.sleep_time = h + ":" + this.format_number(m);

                        var sleep_times = [];
                        var t = null;
                        var t_format = null;

                        var sleep_levels = [];
                        var lvl = null;
                        var lvl_code = null;

                        for(var i=0; i<mostRecentSleepSession.data.level.length; i++) {
                            t = mostRecentSleepSession.data.time[i];
                            t_format = new Date(t).getTime(); //this.formatDateTime(t);
                            sleep_times.push(t_format);

                            lvl = mostRecentSleepSession.data.level[i];
                            if(lvl == "wake") {
                                lvl_code = 4;
                            } else if(lvl == "light" || lvl == "awake") { 
                                lvl_code = 3;
                            } else if(lvl == "rem" || lvl == "restless") {
                                lvl_code = 2;
                            } else { // "deep" || "asleep"
                                lvl_code = 1;
                            }
                            sleep_levels.push(lvl_code);

                            var t_format_next = t_format + mostRecentSleepSession.data.seconds[i]*1000 - 60*1000;
                            var lvl_code_next = lvl_code + 0;

                            sleep_times.push(t_format_next);
                            sleep_levels.push(lvl_code_next);
                        }

                        // create new series to chart
                        let newSeriesData = [];
                        for(var i=0; i<sleep_times.length; i++) {
                            newSeriesData.push([sleep_times[i], sleep_levels[i]]);
                        }

                        this.series[0].data = newSeriesData;
                    }
                    else { //if empty results, empty series aswell
                        this.series[0].data = [];
                    }
                }
            }
            if(this.series[0].data.length == 0) {
                this.showToast("Your sleep log is empty. Perhaps you did not sleep with the bracelet today?", 5000);
            }
        },

        /**
         * Formats numbers se they show the same way
         *  they are display when they came from the REST
         */
        format_number(number) {
            if (number >= 10)
                return number;
            return "0" + number;
        },
    }
}
</script>

<style>
.sleep-box {
    height: 60vh;
    margin-right: 5vh;
    margin-bottom: 10vh;
}

</style>
