<template>
    <div class="sleep-box">
        <apexchart id="sleep-box" width="100%" height="100%" type="line" :options="charts_options" :series="series"></apexchart>
    </div>
</template>

<script>
export default {
    data() {
        var series = [{
            name: 'Levels',
            data: [],
        }];
        return {
            series,
            charts_options: {
                chart: {
                    height: 100,
                    type: 'line',
                    shadow: { enabled: false, color: '#bbb', top: 3, left: 2, blur: 3, opacity: 1 },
                },
                title: {
                    text: 'Sleep Pattern',
                    align: 'left',
                    offsetX: 30,
                    style: {
                        fontSize: "32px",
                        color: '#3face4'
                    }
                },
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
                    }
                },
                //series: series,
                xaxis: {
                    type: 'datetime',
                    //min: new Date('01 Mar 2012').getTime(),
                    //tickAmount: 6,
                    title: {
                        text: 'Time',
                    },
                    labels: {
                        format: 'HH',
                    }
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
        var result = await this.getSleep(this.$store.getters.sessionToken);
        if(result) {
            if(result.status==0) {
                console.log("Sleep");
                console.log(result);
                if(result.data &&  result.data.length>0 && result.data[0].data && result.data[0].data.level && result.data[0].data.level.length>0) {
                    // process result.data
                    var sleep_times = [];
                    var t = null;
                    var t_format = null;

                    var sleep_levels = [];
                    var lvl = null;
                    var lvl_code = null;

                    for(var i=0; i<result.data[0].data.level.length; i++) {
                        t = result.data[0].data.time[i];
                        t_format = new Date(t).getTime(); //this.formatDateTime(t);
                        sleep_times.push(t_format);

                        lvl = result.data[0].data.level[i];
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

                        var t_format_next = t_format + result.data[0].data.seconds[i]*1000 - 60*1000;
                        var lvl_code_next = lvl_code + 0;

                        sleep_times.push(t_format_next);
                        sleep_levels.push(lvl_code_next);
                    }

                    // append data to chart
                    for(var i=0; i<sleep_times.length; i++) {
                        this.series[0]["data"].push([sleep_times[i], sleep_levels[i]]);
                    }

                    console.log(this.series[0]);
                    
                }
            }
        }
        if(this.series[0].data.length == 0) {
            this.showToast("Your sleep log is empty. Perhaps you did not sleep with the bracelet today?", 5000);
        }
    },
    methods: {
        async getSleep(AuthToken) {
            const config = {
                headers: {'AuthToken': AuthToken},
                parameters: {
                    'start': 1557964800,    // 1555369200
                    'end': 1558051200,      // 1555455600
                }
            }
            return await this.$axios.$get("/sleep",config)
                                .then(res => {
                                    if(res.status != 0) {
                                        console.log(res);
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
        }
    }
}
</script>

<style>
.sleep-box {
    height: 60vh;
    margin-right: 5vh;
}
</style>
