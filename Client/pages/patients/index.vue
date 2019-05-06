<template>
    <div style="overflow-x: none;">
        <body>
            <!--================ Header Menu Area =================-->
            <HeaderMenu activePage="Patients" />

            <!--================ Banner Area =================-->
            <PageBanner parent_page="Home" page="Patients" />

            <!--================ Permissions Boxes Area ============-->
            <b-container class="padding">
                <b-row>
                    <!-- =============================== Modal =======================-->
                    <b-modal ref="request_grant_permission_modal" hide-footer hide-header>
                        <div v-if="user_type === 'medic'">
                            <h3  class="title_color text-center" >Request Permission</h3>
                            <h5>Patient Username:</h5>
                            <input id="req_gra_client_username" type="text" class="single-input"> 
                            <h5>Patient Health Number:</h5>
                            <input id="req_gra_health_number" type="number" class="single-input"> 
                        </div>
                        <div v-else-if="user_type === 'client'">
                            <h3  class="title_color text-center" >Grant Permission</h3>
                            <div class="mt-10"> 
                                <h5>Medic Username:</h5>
                                <input id="req_gra_medic_username" type="text" class="single-input"> 
                            </div>
                        </div>
                        <h5>Duration:</h5>
                        <input id="req_gra_duration" type="number" class="single-input">
                        <div class="mt-10 row justify-content-center d-flex align-items-center">
                            <div class="row">
                                <button @click="close_modal" data-dismiss="modal" class="genric-btn danger circle text-uppercase ml-10 mr-10" type="button" >Cancel</button>
                                <button @click="request_grant_permission" class="genric-btn info circle text-uppercase ml-10 mr-10" type="submit" >Add</button>
                            </div>
                        </div>
                    </b-modal>
                    <a
                        class="genric-btn success circle custom_button mb-20"
                        @click="$refs['request_grant_permission_modal'].show()">
                        <span v-if="user_type === 'medic'"><i class="fa fa-plus"></i> Request Permission</span>
                        <span v-else-if="user_type === 'client'"><i class="fa fa-plus"></i> Grant Permission</span>
                    </a>
                </b-row>
                <b-row>
                    <b-card no-body class="w-100">
                        <b-tabs card justified>
                            <b-tab title="Pending">
                                <PermissionsBox title="Pending" :user_type="user_type" />
                            </b-tab>
                            <b-tab title="Accepted">
                                <PermissionsBox title="Accepted" :user_type="user_type" />
                            </b-tab>
                            <b-tab title="Active">
                                <PermissionsBox title="Active" :user_type="user_type" />
                            </b-tab>
                        </b-tabs>
                    </b-card>
                </b-row>
            </b-container>
            
            <!--================ Footer Area =================-->
            <PageFooter />
            
        </body>
        <nuxt/>
    </div>
</template>

<script>
import Vue from 'vue'
import VModal from 'vue-js-modal/dist/ssr.index'
Vue.use(VModal)

import PermissionsBox from '@/components/boxes/PermissionsBox.vue'

export default {
    middleware: ['check-log', 'log'],
    components: {
        PermissionsBox
    },
    head: {
        title: "Patients"
    },
    data() {
        return {
            user_type: "client"
        }
    },
    methods: {
        /**
         * 
         */
        async request_grant_permission() {
            let username, health_number, duration;

            if (this.user_type === "medic") {
                username = $("#req_gra_client_username").val();
                health_number = $("#req_gra_health_number").val();
            } else if (this.user_type === "client")
                username = $("#req_gra_medic_username").val();

            duration = $("#req_gra_duration").val();

            return await this.$axios.$post("", {

            })
            .then(res => {

            })
            .catch(e => {

            })
        },

        /**
         * Clears all inputs on the modal and closes it
         */
        close_modal() {
            $("#req_gra_client_username").val("");
            $("#req_gra_health_number").val("");
            $("#req_gra_medic_username").val("");
            $("#req_gra_duration").val("");
            this.$refs["request_grant_permission_modal"].hide();
        }
    }
}
</script>

<style scoped>
.padding {
    margin-top: 10px;
    margin-bottom: 10px;
}

.column_border {
    border-style: solid;
    border-width: 1px;
}

</style>
