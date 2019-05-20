<template>
    <div style="overflow-x: none;">
        <body>
            <!--================ Header Menu Area =================-->
            <HeaderMenu activePage="Patients" />

            <!--================ Banner Area =================-->
            <PageBanner parent_page="Home" page="Patients" />

            <!--================ Permissions Boxes Area ============-->
            <div class="row justify-content-center align-items-center">
                <div class="col-lg-9 col-md-9">
                    <PermissionsDiv @use="use_permission" />
                </div>
            </div>

            <!--================ Permissions Boxes Area ============-->
            <div class="row justify-content-center align-items-center">
                <div class="col-lg-11 col-md-11">
                    <b-container ref="client_container" class="mb-20" v-show="data_loaded">
                        <b-row>
                            <div class="w-100">
                                <b-row>
                                    <h1 class="col-md-11 mt-10">{{ client_name }}</h1>
                                    <div class="col-md-1 mt-10">
                                        <button @click="close_charts" class="genric-btn-xtra radius"><i class="fa fa-times"></i></button>
                                    </div>
                                </b-row>
                                <b-row>
                                    <b-col md="3">
                                        <b-card style="width:200px">
                                            <h4>Metrics</h4>
                                            <div class="form-inline">
                                                <input @click="on_metric_option_change('/healthstatus')" type="radio" name="metric_option" id="health_status_radio" checked />
                                                <label for="health_status_radio"> Health Status</label>
                                            </div>
                                            <div class="form-inline">
                                                <input @click="on_metric_option_change('/environment')" type="radio" name="metric_option" id="environment_radio" />
                                                <label for="environment_radio"> Environment</label>
                                            </div>
                                            <div class="form-inline">
                                                <input @click="on_metric_option_change('/sleep')" type="radio" name="metric_option" id="sleep_radio" />
                                                <label for="sleep_radio"> Sleep</label>
                                            </div>
                                            <div class="form-inline mb-20">
                                                <input @click="on_metric_option_change('/event')" type="radio" name="metric_option" id="events_radio" />
                                                <label for="events_radio"> Events</label>
                                            </div>
                                        </b-card>
                                    </b-col>

                                    <b-col v-if="data_source != '/sleep'" offset-md="1" md=7>
                                        <TimeIntervalForm @time_interval_submit="time_interval_submit_handler" />
                                    </b-col>
                                    <b-col v-else offset-md="1" md=7>
                                        <SleepIntervalForm @sleep_interval_submit="sleep_interval_submit_handler" />
                                    </b-col>
                                </b-row>
                                <div v-if="valid_data">
                                    <b-card v-if="data_source == '/healthstatus' || data_source == '/environmnet'" no-body>
                                        <b-tabs card justified>
                                            <b-tab v-for="(chart_build_data, metric) in charts_build_data" :key="metric" :title="metric">
                                                <apexchart :options="chart_build_data.options" :series="[{name:metric, data:chart_build_data.data}]"></apexchart>
                                            </b-tab>
                                        </b-tabs>
                                    </b-card>
                                    <SleepBox v-else-if="data_source == '/sleep'" :patient="client_username" :date="start" ref="sleep_box" />
                                    <!--
                                    <div v-else-if="data_source == '/event'" class="justify-content-center d-flex" style="margin-bottom:-50px">
                                        <div class="justify-content-center d-flex align-items-top col-lg-11 col-md-11 max-width-1920 row">
                                            <div class="col-lg-5 col-md-12 col-sm-12 col-xs-12 mr--30 mt-30">
                                                <Events style="height:500px;" @clicked="changeEvent" :startTime="startEvents" :endTime="endEvents" :refresh="refresh"/>
                                            </div>
                                            <div class="col-lg-7 col-md-12 col-sm-12 col-xs-12 ml--30">
                                                <div class="col-lg-10 col-md-10 col-sm-10 col-xs-10" style="margin: auto; margin-top:29px">
                                                    <h3 class="widget_title"> Your most frequent episodes </h3>
                                                    <EventComparator @clicked="changeEvent" id="comparator" :event="event" :startTime="startEvents" :endTime="endEvents"/>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    -->
                                </div>
                                <div v-else class="text-center">
                                    <p>No data for the given patient, interval and metrics option requested.</p>
                                </div>
                            </div>
                        </b-row>
                    </b-container>
                </div>
            </div>
            
            <!--================ Footer Area =================-->
            <PageFooter />
            
        </body>
        <nuxt/>
    </div>
</template>

<script>
import PermissionsDiv from '@/components/boxes/PermissionsDiv.vue'
import TimeIntervalForm from '@/components/forms/TimeIntervalForm.vue'
import SleepBox from '@/components/boxes/SleepBox.vue'
import SleepIntervalForm from '@/components/forms/SleepIntervalForm.vue'

export default {
    middleware: ['check-log', 'log', 'medics-only'],
    components: {
        PermissionsDiv,
        TimeIntervalForm,
        SleepBox,
        SleepIntervalForm
    },
    head: {
        title: "Patients"
    },
    data() {
        return {
            data_loaded: false,
            data_source: "/healthstatus",
            client_name: "",
            client_username: "",
            charts_build_data: {},
            start: null,
            end: null,
            interval: null,
            valid_data: true
        }
    },
    methods: {
        show_toast(message) {
            this.$toasted.show(message, {position: 'bottom-center', duration: 7500});
        },

        /**
         * Used to insert into the options of a specific chart
         *  an upper or lower bound
         * 
         * @param charts_option option of the chart to change
         * @param is_upper_bound if the bound to insert limits
         *  lower or upper values
         * @param y_value y value where the annotation will be placed
         */
        construct_annotation(charts_options, is_upper_bound, y_value) {
            charts_options.annotations.yaxis.push({
                y: y_value,
                borderColor: '#ff0000',
                label: {
                    borderColor: '#ff0000',
                    style: {
                    color: '#fff',
                    background: '#ff0000',
                    },
                    text: (is_upper_bound ? 'Upper' : 'Lower') + ' bound',
                }
            });
        },

        /**
         * Returns an object used as options to use
         *  on all charts. Same as making a copy of
         *  one object returns on data() method
         */
        get_base_chart_option() {
            return {
                zoom: {
                    enable: true,
                    type: 'x'
                },
                xaxis: {
                    type: "datetime",
                    labels: {
                        format: "dd-MMM-yyyy HH:mm",
                        rotate: 0
                    },
                    title: {
                        text: "Time"
                    },
                    tickAmount: 'dataPoints'
                },
                yaxis: {
                    title: {}
                },
                tooltip: {
                    x: {
                        format: "dd-MMM-yyyy HH:mm"
                    }
                },
                annotations: {
                    yaxis: []
                }
            };
        },

        /**
         * Creates customized chart option according to the metric
         *  that the chart will display
         */
        create_chart_options(metric) {
            let lower, upper, metric_units;

            switch(metric) {
                case "Heart Rate":
                    lower = 50;
                    upper = 100;
                    metric = "bpm";
                    break;
                case "Steps":
                    lower = 1000;
                    break;
                case "Aqi":
                    lower = 75;
                    break;
                case "Pm10":
                    lower = 40;
                    metric_units = "µg/m3";
                    break;
                case "Voc":
                    lower = 350;
                    metric_units = "ppm"
                    break;
                case "O3":
                    lower = 130;
                    metric_units = "µm";
                    break;
                case "Pm25":
                    lower = 55;
                    metric_units = "µm";
                    break;
                case "So2":
                    lower = 180;
                    metric_units = "µm";
                    break;
            };

            let chart_options = this.get_base_chart_option();

            if (lower)
                this.construct_annotation(chart_options, false, lower);

            if (upper)
                this.construct_annotation(chart_options, true, upper);

            if (metric_units)
                this.chart_options.yaxis.title.text = metric_units;
            
            return chart_options
        },

        /**
         * Used to display the charts
         * No arguments are received because variables on
         *  data are changed before this function is called
         */
        async display_graphics() {
            await this.$axios.$get(this.data_source, {
                headers: {
                    AuthToken: this.$store.getters.sessionToken
                },
                params: {
                    patient: this.client_username,
                    start: this.start,
                    end: this.end,
                    interval: this.interval
                }
            })
            .then(res => {
                if (res.status == 0) {
                    if (Object.keys(res.data).length == 0) {
                        this.valid_data = false;
                        return;
                    }

                    let time = res.data.time;

                    let new_charts_build_data = {};
                    /**
                     * Because some metrics come in lowerCalmelCase, with this
                     *  metric name is transformed readable for "normal people"
                     */
                    for (let key in res.data) {

                        if (key == "latitude" || key == "longitude" || key == "time")
                            continue;

                        let new_key = key.charAt(0).toUpperCase();
                        for (let j = 1; j < key.length; j++)
                            if (key.charAt(j).match(/[A-Z]/))
                                new_key += " " + key.charAt(j);
                            else
                                new_key += key.charAt(j);


                        let data = res.data[key];
                        for (let i = 0; i < time.length; i++) {
                            let y_value = data[i];
                            let parsed_time = Date.parse(time[i]);
                            data[i] = [parsed_time, y_value];
                        }

                        new_charts_build_data[new_key] = {
                            options: this.create_chart_options(new_key),
                            data: data
                        }
                    }

                    this.charts_build_data = new_charts_build_data;

                    this.valid_data = true;
                }
                else if (res.status == 1) {
                    this.valid_data = false;
                    this.show_toast(res.msg);
                }
                else if(res.status == 4) {
                    this.$toasted.show(res.msg, {position: 'bottom-center', duration: 7500});
                    this.$disconnect()
                    this.$nextTick(() => { 
                        this.$store.dispatch('logout'),
                        this.$router.push("/login")
                    });
                }
                else {
                    this.valid_data = false;
                    this.show_toast("Some error occured when retrieving data.");
                }
            })
            .catch(e => {
                this.valid_data = false;
                console.log(e);
                this.show_toast("Some error occured when retrieving data.");
                        this.received_data = false;
            });
        },

        /**
         * Invoked whenever a medic click on a play button
         */
        async use_permission(client_name, client_username) {
            this.client_name = client_name;
            this.client_username = client_username;
            this.data_loaded = true;

            this.display_graphics();
        },

        async on_metric_option_change(new_data_source) {
            if (new_data_source === this.data_source)
                return;

            this.data_source = new_data_source;

            if (this.data_source == "/healthstatus" || this.data_source == "/environment")
                this.display_graphics();
        },

        close_charts() {
            this.data_loaded = false;

            this.client_name = "";
            this.client_username = "";

            document.getElementById("health_status_radio").checked = true;
            this.data_source = "/healthstatus"
        },

        time_interval_submit_handler(start, end, interval) {
            this.start = start ? new Date(start).getTime() / 1000 : null;
            this.end = end ? new Date(end).getTime() / 1000 : null;
            this.interval = interval;

            if (this.data_source == "/healthstatus" || this.data_source == "/environment")
                this.display_graphics();
        },

        sleep_interval_submit_handler(date) {
            console.log("sleep data update");
            console.log(date);
            this.$refs.sleep_box.updateChart(date ? new Date(date).getTime() / 1000 : null);
        }
    }
}
</script>

<style>
</style>
