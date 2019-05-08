<template>
    <b-container class="mb-20 mt-10">
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
                        <button @click="close_modal" data-dismiss="modal" class="genric-btn primary radius text-uppercase ml-10 mr-10" type="button" >Cancel</button>
                        <button v-if="user_type === 'medic'" @click="request_permission" class="genric-btn info radius text-uppercase ml-10 mr-10" type="submit" >Add</button>
                        <button v-else-if="user_type === 'client'" @click="grant_permission" class="genric-btn info radius text-uppercase ml-10 mr-10" type="submit" >Add</button>
                    </div>
                </div>
            </b-modal>
            <button
                class="genric-btn info radius mb-20"
                @click="$refs.request_grant_permission_modal.show()">
                <span v-if="user_type === 'medic'"><i class="fa fa-plus"></i> Request Permission</span>
                <span v-else-if="user_type === 'client'"><i class="fa fa-plus"></i> Grant Permission</span>
            </button>
        </b-row>
        <b-row>
            <b-card no-body class="w-100">
                <b-tabs card justified>
                    <b-tab title="Pending">
                        <PermissionsTable title="pending" :user_type="user_type" :permissions="permissions.pending" />
                    </b-tab>
                    <b-tab title="Accepted">
                        <PermissionsTable title="accepted" :user_type="user_type" :permissions="permissions.accepted" />
                    </b-tab>
                    <b-tab title="Active">
                        <PermissionsTable title="active" :user_type="user_type" :permissions="permissions.active" />
                    </b-tab>
                </b-tabs>
            </b-card>
        </b-row>
    </b-container>
</template>

<script>
import PermissionsTable from '@/components/tables/PermissionsTable.vue'

export default {
    name: 'PermissionsDiv',
    components: {
        PermissionsTable
    },
    data() {
        return {
            user_type: "client",
            permissions: {
                "pending":[],
                "accepted":[],
                "active":[]
            },
            requests_header: {
                headers: {'AuthToken': this.$store.getters.sessionToken},
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
                    company: "Hospital Leiria",
                    duration: 10
                },
                {
                    full_name: "André Pedrosa",
                    username: "zonnax",
                    health_number: 111111112,
                    company: "Hospital Leiria",
                    duration: 10
                }
            ],
            accepted: [
                {
                    full_name: "André Pedrosa",
                    username: "aspedrosa",
                    health_number: 111111113,
                    company: "Hospital Leiria",
                    duration: 10
                },
                {
                    full_name: "André Pedrosa",
                    username: "zonnax",
                    health_number: 111111114,
                    company: "Hospital Leiria",
                    duration: 10
                }
            ],
            active: [
                {
                    full_name: "André Pedrosa",
                    username: "aspedrosa",
                    health_number: 111111115,
                    company: "Hospital Leiria",
                    duration: 10
                },
                {
                    full_name: "André Pedrosa",
                    username: "zonnax",
                    health_number: 111111116,
                    company: "Hospital Leiria",
                    duration: 10
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
        async request_permission() {
            let username = this.$refs.client_username_input.value;
            let health_number = this.$refs.health_number_input.value;
            let duration = this.$refs.duration_input.value;

            this.close_modal();

            await this.$axios.$post("/permission/request", {
                username: username,
                health_number: health_number,
                duration: duration
            }, this.requests_header)
            .then(res => {
                this.$toasted.show(
                    'Permission requested.', 
                    {
                        position: 'bottom-center',
                        duration: 7500
                    }
                );
            })
            .catch(e => {
                this.$toasted.show(
                    'Error granting permission. Try again later.', 
                    {
                        position: 'bottom-center',
                        duration: 7500
                    }
                );
            })
        },
        /**
         * 
         */
        async grant_permission() {
            let username = this.$refs.medic_username_input.value;
            let duration = this.$refs.duration_input.value;

            this.close_modal();

            await this.$axios.$post("/permission", {
                username: username,
                duration: duration
            }, this.requests_header)
            .then(res => {
                this.$toasted.show(
                    'Permission granted.', 
                    {
                        position: 'bottom-center',
                        duration: 7500
                    }
                );
            })
            .catch(e => {
                this.$toasted.show(
                    'Error granting permission. Try again later.', 
                    {
                        position: 'bottom-center',
                        duration: 7500
                    }
                );
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

<style>
</style>
