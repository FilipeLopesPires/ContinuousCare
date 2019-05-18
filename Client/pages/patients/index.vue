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
                    <b-container ref="client_container" class="mb-20" :hidden="!data_loaded">
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
                                                <input @click="on_metric_option_change(true)" type="radio" name="metric_option" id="health_status_radio" checked />
                                                <label for="health_status_radio"> Health Status</label>
                                            </div>
                                            <div class="form-inline mb-20">
                                                <input @click="on_metric_option_change(false)" type="radio" name="metric_option" id="environment_radio" />
                                                <label for="environment_radio"> Environment</label>
                                            </div>
                                        </b-card>
                                    </b-col>

                                    <b-col offset-md="1" md=7>
                                        <TimeIntervalForm @time_interval_submit="time_interval_submit_handler" />
                                    </b-col>
                                </b-row>
                                <b-card v-if="Object.keys(charts_data).length > 0" no-body>
                                    <b-tabs card justified>
                                        <b-tab v-for="(data, metric) in charts_data" :key="metric" :title="metric">
                                            <apexchart width="100%" height="80%" type="line" :options="charts_options" :series="[{data:data}]"></apexchart>
                                        </b-tab>
                                    </b-tabs>
                                </b-card>
                                <div class="text-center" v-else>
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
            }
        }
    },
    methods: {
        /**
         * Used to display the charts
         * No arguments are received because variables on
         *  data are changed before this function is called
         */
        async display_graphics() {
            console.log("call");
            await this.$axios.$get(this.data_source, {
                headers: {
                    AuthToken: this.$store.getters.sessionToken
                },
                params: {
                    patient: this.client_username
                }
            })
            .then(res => {
                if (res.status == 0) {
                    this.charts_options.xaxis.categories = res.data.time;
                    delete res.data.time;
                    this.charts_data = res.data;
                }
                else if (res.status == 1) {

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

                }
            })
            .catch(e => {
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

        async on_metric_option_change(health_status_clicked) {
            let new_data_source = health_status_clicked ? "/healthstatus" : "/environment";

            if (new_data_source === this.data_source)
                return;

            this.data_source = new_data_source;

            this.display_graphics();
        },

        close_charts() {
            this.data_loaded = false;

            this.charts_data = {};

            this.client_name = "";
            this.client_username = "";

            document.getElementById("health_status_radio").checked = true;
            this.data_source = "/healthstatus"
        },

        time_interval_submit_handler(start, end, interval) {
        }
    }
}
</script>

<style>
</style>
