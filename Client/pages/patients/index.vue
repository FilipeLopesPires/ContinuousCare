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
                            <input ref="client_username_input" type="text" class="single-input"> 
                            <h5>Patient Health Number:</h5>
                            <input ref="health_number_input" type="number" class="single-input"> 
                        </div>
                        <div v-else-if="user_type === 'client'">
                            <h3  class="title_color text-center" >Grant Permission</h3>
                            <div class="mt-10"> 
                                <h5>Medic Username:</h5>
                                <input ref="medic_username_input" type="text" class="single-input"> 
                            </div>
                        </div>
                        <h5>Duration:</h5>
                        <input ref="duration_input" type="number" class="single-input">
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
                                <PermissionsBox title="pending" :user_type="user_type" :permissions="permissions.pending" />
                            </b-tab>
                            <b-tab title="Accepted">
                                <PermissionsBox title="accepted" :user_type="user_type" :permissions="permissions.accepted" />
                            </b-tab>
                            <b-tab title="Active">
                                <PermissionsBox title="active" :user_type="user_type" :permissions="permissions.active" />
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
            user_type: "medic",
            permissions: {
                "pending":[],
                "accepted":[],
                "active":[]
            }
        }
    },
    async mounted() {
        this.permissions = {
            pending: [
                {
                    full_name: "André Pedrosa",
                    username: "aspedrosa",
                    health_number: 111111111,
                    company: "Hospital Leiria"
                },
                {
                    full_name: "André Pedrosa",
                    username: "zonnax",
                    health_number: 111111112,
                    company: "Hospital Leiria"
                }
            ],
            accepted: [
                {
                    full_name: "André Pedrosa",
                    username: "aspedrosa",
                    health_number: 111111113,
                    company: "Hospital Leiria"
                },
                {
                    full_name: "André Pedrosa",
                    username: "zonnax",
                    health_number: 111111114,
                    company: "Hospital Leiria"
                }
            ],
            active: [
                {
                    full_name: "André Pedrosa",
                    username: "aspedrosa",
                    health_number: 111111115,
                    company: "Hospital Leiria"
                },
                {
                    full_name: "André Pedrosa",
                    username: "zonnax",
                    health_number: 111111116,
                    company: "Hospital Leiria"
                }
            ]
        }

        return;

        this.permissions = this.$axios.$get("", {

        })
        .then(res => {
            if(res.status != 0) {
                this.requestError = true;
                return {
                    "pending" : [],
                    "accepted": [],
                    "active": []
                };
            }
            return res.data;
        })
        .catch(e => {

        })
    },
    methods: {
        /**
         * 
         */
        async request_grant_permission() {
            let username, health_number, duration;

            if (this.user_type === "medic") {
                username = this.$refs.client_username_input.value;
                health_number = this.$refs.health_number_input.value;
            } else if (this.user_type === "client")
                username = this.$refs.medic_username_input.value;

            duration = this.$refs.duration_input.value;

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
            if (this.user_type === "medic") {
                this.$refs.client_username_input.value = "";
                this.$refs.health_number_input.value = "";
            }
            else if (this.user_type === "client")
                this.$refs.medic_username_input.value = "";

            this.$refs.duration_input.value = "";

            this.$refs.request_grant_permission_modal.hide();
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
