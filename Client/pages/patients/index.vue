<template>
    <div style="overflow-x: none;">
        <body>
            <!--================ Header Menu Area =================-->
            <HeaderMenu activePage="Patients" />

            <!--================ Banner Area =================-->
            <PageBanner parent_page="Home" page="Patients" />

            <div class="mb--20">  
                <div class="row d-flex justify-content-center align-items-center">
                    <!--================ Permissions Boxes Area ============-->
                    <div class="col-lg-9 col-md-9">
                        <PermissionsDiv @use="use_permission" />
                    </div>

                    <!--================ Permissions Boxes Area ============-->
                    <div class="col-lg-11 col-md-11">
                        <b-container ref="client_container" class="mb-20" v-if="data_loaded">
                            <b-row >
                                <div class="w-100">
                                    <b-row>
                                        <h1 class="col-md-11 mt-10">{{ client_name }}</h1>
                                        <div class="col-md-1 mt-10">
                                            <button style="background:none; color:black; border:none; font-size:30px" @click="data_loaded = false" class="genric-btn-xtra radius"><i class="fa fa-times"></i></button>
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
                                        <b-card v-if="data_source == '/healthstatus' || data_source == '/environment'" no-body>
                                            <b-tabs card justified>
                                                <b-tab v-for="(chart_build_data, metric) in charts_build_data" :key="metric" :title="metric">
                                                    <apexchart :options="chart_build_data.options" :series="[{name:metric, data:chart_build_data.data}]"></apexchart>
                                                </b-tab>
                                            </b-tabs>
                                        </b-card>
                                        <SleepBox style="margin-bottom:100px" v-else-if="data_source == '/sleep'" :patient="client_username" :date="start" ref="sleep_box" />
                                        <b-row v-else-if="data_source == '/event'" class="mt-25">
                                            <b-col md="6">
                                                <Events style="height:500px;" @clicked="changeEvent" :startTime="start" :endTime="end" :intervalTime="interval" :refresh="refresh" :patient="client_username" />
                                            </b-col>
                                            <b-col md="6">
                                                <EventComparator @clicked="changeEvent" id="comparator" :event="event" :startTime="start" :endTime="end" :intervalTime="interval" :refresh="refresh" :patient="client_username" />
                                            </b-col>
                                            <EventOptions :height="height" :width="width" :options="options" @option="changeEvt"/>
                                        </b-row>
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
            
            </div>
        </body>
        <nuxt/>
    </div>
</template>

<script>
import PermissionsDiv from '@/components/boxes/PermissionsDiv.vue'

import TimeIntervalForm from '@/components/forms/TimeIntervalForm.vue'

import SleepBox from '@/components/boxes/SleepBox.vue'
import SleepIntervalForm from '@/components/forms/SleepIntervalForm.vue'

import Events from '@/components/events/Events.vue'
import EventComparator from '@/components/events/EventComparator.vue'
import EventOptions from '@/components/modals/EventOptions.vue'

export default {
    middleware: ['check-log', 'log', 'medics-only'],
    components: {
        PermissionsDiv,

        TimeIntervalForm,

        SleepBox,
        SleepIntervalForm,

        Events,
        EventComparator,
        EventOptions,
    },
    head: {
        title: "Patients"
    },
    data() {
        return {
            data_loaded: false,

            data_source: "/healthstatus",

            client_name: "",
            client_username: null,

            charts_build_data: {},

            start: null,
            end: null,
            interval: null,

            //if received valid or non empty data from a response
            valid_data: true,

            //events related
            refresh: null,
            width: 0,
            height: 0,
            options: {
                easing: 'ease-in',
                force: true,
                cancelable: true,
                x: false,
                y: true
            },
            event: ""
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
                        formatter: value => {
                            let d = new Date(value);
                            return this.format_number(d.getDay()) + "-" +
                                   this.format_number(d.getMonth()) + "-" +
                                   this.format_number(d.getFullYear()) + " " +
                                   this.format_number(d.getHours()) + ":" +
                                   this.format_number(d.getMinutes());
                        },
                        //rotate: 0
                    },
                    title: {
                        text: "Time"
                    },
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
                chart_options.yaxis.title.text = metric_units;
            
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
                    console.log(res.msg);
                    console.log(res.status);
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
        use_permission(client_name, client_username) {
            this.client_name = client_name;
            this.client_username = client_username;

            this.data_source = "/healthstatus";
            this.start = this.end = this.interval = null;
            this.event = "";

            this.data_loaded = true;

            this.display_graphics();
        },

        async on_metric_option_change(new_data_source) {
            if (new_data_source === this.data_source)
                return;

            this.data_source = new_data_source;

            if (this.data_source == "/healthstatus" || this.data_source == "/environment")
                this.display_graphics();
            else
                this.valid_data = true;
        },

        time_interval_submit_handler(start, end, interval) {
            this.start = start ? new Date(start).getTime() / 1000 : null;
            this.end = end ? new Date(end).getTime() / 1000 : null;
            this.interval = interval;

            if (this.data_source == "/healthstatus" || this.data_source == "/environment")
                this.display_graphics();
            else if (this.data_source == "/event")
                this.refresh = Math.random();
        },

        sleep_interval_submit_handler(date) {
            this.$refs.sleep_box.updateChart(date ? new Date(date).getTime() / 1000 : null);
        },

        changeEvent(eventTitle, w, h, objective){
            if (objective == "refresh") {
                this.event = "refresh";
                this.refresh = eventTitle;
                return;
            }

            if (eventTitle == "Others") {
                return;
            }

            if (eventTitle.split(", ").length > 1) {
                this.width = w;
                this.height = h;
                this.options = eventTitle.split(", ");
                this.$modal.show("eventOptions");
            }
            else
                this.event = eventTitle;
        },
        changeEvt(eventTitle){
            if (eventTitle)
                this.event=eventTitle;
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
</style>
