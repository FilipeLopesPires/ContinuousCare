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
            <b-container ref="client_container" class="mb-20" :hidden="!data_loaded">
                <b-row>
                    <div class="w-100">
                        <h2 class="mt-10">{{ client_name }}</h2>
                        <div class="form-inline">
                            <input @click="on_metric_option_change(true)" type="radio" name="metric_option" id="health_status" checked />
                            <label for="health_status"> Health Status</label>
                        </div>
                        <div class="form-inline mb-20">
                            <input @click="on_metric_option_change(false)" type="radio" name="metric_option" id="environment" />
                            <label for="environmnet"> Environment</label>
                        </div>
                        <b-card no-body>
                            <b-tabs card justified>
                                <b-tab v-for="(data, metric) in charts_data" :key="metric" :title="metric">
                                    <apexchart width="100%" height="80%" type="line" :options="{xaxis:{type:'seconds', categories: data.time}}" :series="[{data:data.values}]"></apexchart>
                                </b-tab>
                            </b-tabs>
                        </b-card>
                    </div>
                </b-row>
            </b-container>
            
            <!--================ Footer Area =================-->
            <PageFooter />
            
        </body>
        <nuxt/>
    </div>
</template>

<script>
import PermissionsDiv from '@/components/boxes/PermissionsDiv.vue'

export default {
    middleware: ['check-log', 'log', 'medics-only'],
    components: {
        PermissionsDiv
    },
    head: {
        title: "Patients"
    },
    data() {
        return {
            data_loaded: false,
            data_source: "/healthstatus",
            client_name: "",
            charts_data: {
                "Hearth Rate": {
                    time: [1,2,3],
                    values: [1,2,3]
                },
                "CO2": {
                    time: [1,2,3],
                    values: [1,2,3]
                },
                "OZONO": {
                    time: [1,2,3],
                    values: [1,2,3]
                }
            },
            requests_header: {
                headers: {AuthToken: this.$store.getters.sessionToken},
            },
        }
    },
    methods: {
        use_permission(client_name, client_health_number) {
            this.client_name = client_name;
            this.data_loaded = true;
        },

        async on_metric_option_change(health_status_clicked) {
            let new_data_source = health_status_clicked ? "/health_status" : "/environmnet";

            if (new_data_source === data_source)
                return;

            await this.$axios.$get("", this.requests_header)
            .then(res => {
                if (res.status == 0) {

                }
                else if (res.status == 1) {

                }
                else {

                }
            })
            .catch(e => {

            });
        }
    }
}
</script>

<style>
</style>
