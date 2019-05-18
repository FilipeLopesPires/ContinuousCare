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
                                            <div class="form-inline mb-20">
                                                <input @click="on_metric_option_change('/sleep')" type="radio" name="metric_option" id="environment_radio" />
                                                <label for="environment_radio"> Sleep</label>
                                            </div>
                                        </b-card>
                                    </b-col>

                                    <b-col offset-md="1" md=7>
                                        <TimeIntervalForm @time_interval_submit="time_interval_submit_handler" />
                                    </b-col>
                                </b-row>
                                <b-card v-show="valid_data" no-body>
                                    <b-tabs card justified>
                                        <b-tab v-for="(data, metric) in charts_data" :key="metric" :title="metric">
                                            <apexchart width="100%" type="line" :options="charts_options" :series="[{data:data}]"></apexchart>
                                        </b-tab>
                                    </b-tabs>
                                </b-card>
                                <div v-show="!valid_data" class="text-center">
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

export default {
    middleware: ['check-log', 'log', 'medics-only'],
    components: {
        PermissionsDiv,
        TimeIntervalForm
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
            charts_data: {},
            charts_options: {
                xaxis: {
                    type:'seconds',
                    categories: []
                }
            },
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
                    
                    this.charts_options.xaxis.categories = res.data.time;

                    /**
                     * Because some metrics come in lowerCalmelCase, with this
                     *  metric name is transformed readable for "normal people"
                     */
                    for (let key in res.data) {

                        if (key == "latitude" || key == "longitude" || key == "time")
                            delete res.data[key];
                        else {
                            let new_key = key.charAt(0).toUpperCase();

                            for (let j = 1; j < key.length; j++)
                                if (key.charAt(j).match(/[A-Z]/))
                                    new_key += " " + key.charAt(j);
                                else
                                    new_key += key.charAt(j);

                            let tmp = res.data[key];
                            delete res.data[key];
                            res.data[new_key] = tmp;
                        }

                    }

                    this.charts_data = res.data;

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

            this.display_graphics();
        },

        close_charts() {
            this.data_loaded = false;

/*             this.charts_data = {};
            this.charts_options.xaxis.categories = []; */

            this.client_name = "";
            this.client_username = "";

            document.getElementById("health_status_radio").checked = true;
            this.data_source = "/healthstatus"
        },

        time_interval_submit_handler(start, end, interval) {
            this.start = new Date(start).getTime() / 1000;
            this.end = new Date(end).getTime() / 1000;
            this.interval = interval;

            this.display_graphics();
        }
    }
}
</script>

<style>
</style>
