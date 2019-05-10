<template>
    <b-container class="mb-20 mt-10">
        <b-row>
            <!-- =============================== Modal =======================-->
            <b-modal ref="request_grant_permission_modal" hide-footer hide-header>
                <div v-if="user_type === 'medic'">
                    <h3  class="title_color text-center" >Request Permission</h3>
                    <h5>Patient Username:</h5>
                    <div class="form-inline">
                        <input @click="on_request_option_change(true)" type="radio" class="col-md-1" name="request_option" />
                        <b-input v-model="client_username" ref="client_username_input" class="single-input col-md-11" :disabled="!request_by_username"></b-input>
                    </div>
                    <h5>Patient Health Number:</h5>
                    <div class="form-inline">
                        <input @click="on_request_option_change(false)" type="radio" class="col-md-1" name="request_option" checked />
                        <b-input v-model="health_number" ref="health_number_input" class="single-input col-md-11" :disabled="request_by_username"></b-input> 
                    </div>
                </div>
                <div v-else-if="user_type === 'client'">
                    <h3  class="title_color text-center" >Grant Permission</h3>
                    <div class="mt-10"> 
                        <h5>Medic Username:</h5>
                        <input ref="medic_username_input" type="text" class="single-input"> 
                    </div>
                </div>
                <h5>Duration:</h5>
                <input ref="duration_input" class="single-input">
                <div class="mt-10 row justify-content-center d-flex align-items-center">
                    <div class="row">
                        <button @click="close_modal" data-dismiss="modal" class="genric-btn primary radius text-uppercase ml-10 mr-10" type="button" >Cancel</button>
                        <button v-if="user_type === 'medic'" @click="request_permission" class="genric-btn info radius text-uppercase ml-10 mr-10" type="button" >Add</button>
                        <button v-else-if="user_type === 'client'" @click="grant_permission" class="genric-btn info radius text-uppercase ml-10 mr-10" type="button" >Add</button>
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
                        <PermissionsTable title="pending" :user_type="user_type" :permissions="permissions.pending" v-on:ola="accept_permission" />
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
            user_type: this.$store.getters.userType,
            permissions: {
                "pending":[],
                "accepted":[],
                "active":[]
            },
            requests_header: {
                headers: {AuthToken: this.$store.getters.sessionToken},
            },
            request_by_username: false,
            health_number: "",
            client_username: ""
        }
    },
    async mounted() {

        this.permissions = await this.$axios.$get("/permission", this.requests_header)
        .then(res => {
            if(res.status == 0)
                return res.data;
            else if (res.status == 1)
                this.$toasted.show(
                    res.msg,
                    {
                        position: 'bottom-center',
                        duration: 7500
                    }
                );
            else {
                console.log("status code : " + res.status);
                console.log("message : " + res.msg);
                this.$toasted.show(
                    'Error retrieving permissions.', 
                    {
                        position: 'bottom-center',
                        duration: 7500
                    }
                );
            }
            return {
                pending: [],
                accepted: [],
                active: []
            };
        })
        .catch(e => {
            console.log(e);
            this.$toasted.show(
                'Error retrieving permissions.', 
                {
                    position: 'bottom-center',
                    duration: 7500
                }
            );
            return {
                pending: [],
                accepted: [],
                active: []
            };
        });
    },
    methods: {
        /**
         * 
         */
        async request_permission() {
            let username = this.$refs.client_username_input.value;
            let health_number = this.$refs.health_number_input.value;
            let duration = this.$refs.duration_input.value;

            if (this.request_by_username) {
                if (username == "") {
                    this.$toasted.show(
                        'Insert a username.', 
                        {
                            position: 'bottom-center',
                            duration: 7500
                        }
                    );
                    return;
                }

                health_number = null;
            }
            else {
                if (health_number == "") {
                    this.$toasted.show(
                        'Insert a health number.', 
                        {
                            position: 'bottom-center',
                            duration: 7500
                        }
                    );
                    return;
                }
                else if (! /^\d+$/.test(health_number)) {
                    this.$toasted.show(
                        'Invalid health number.', 
                        {
                            position: 'bottom-center',
                            duration: 7500
                        }
                    );
                    return;
                }

                username = null;
            }

            if (! /^\d+$/.test(duration)) {
                this.$toasted.show(
                    'Invalid duration.', 
                    {
                        position: 'bottom-center',
                        duration: 7500
                    }
                );
                return;
            }

            this.close_modal();

            await this.$axios.$post("/permission", {
                username: username,
                health_number: health_number,
                duration: duration
            }, this.requests_header)
            .then(res => {
                if (res.status == 0) {
                    this.$toasted.show(
                        'Permission requested.', 
                        {
                            position: 'bottom-center',
                            duration: 7500
                        }
                    );
                    this.permissions.pending.push(
                        {
                            username: res.data.username,
                            name: res.data.name,
                            email: res.data.email,
                            health_number: res.data.health_number,
                            duration: duration
                        }
                    )
                    res.data
                }
                else if (res.status == 1) {
                    this.$toasted.show(
                        res.msg,
                        {
                            position: 'bottom-center',
                            duration: 7500
                        }
                    );
                }
                else {
                    console.log("status code : " + res.status);
                    console.log("message : " + res.msg);
                    this.$toasted.show(
                        'Error granting permission. Try again later.', 
                        {
                            position: 'bottom-center',
                            duration: 7500
                        }
                    );
                }
            })
            .catch(e => {
                console.log(e);
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
                if (res.status == 0) {
                    this.$toasted.show(
                        'Permission granted.', 
                        {
                            position: 'bottom-center',
                            duration: 7500
                        }
                    );
                    this.permissions.accepted.push(
                        {
                            username: username,
                            name: res.data.name,
                            email: res.data.email,
                            company: res.data.company,
                            duration: duration
                        }
                    )
                }
                else if (res.status == 1)
                    this.$toasted.show(
                        res.msg,
                        {
                            position: 'bottom-center',
                            duration: 7500
                        }
                    );
                else {
                    console.log("status code: " + res.status)
                    console.log("error msg: " + res.msg)
                    this.$toasted.show(
                        "Error granting permission. Try again later.",
                        {
                            position: 'bottom-center',
                            duration: 7500
                        }
                    );
                }
            })
            .catch(e => {
                console.log(e);
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
        },

        on_request_option_change(change_to_username) {
            if (this.request_by_username == change_to_username)
                return;

            if (this.request_by_username)
                this.client_username = "";
            else
                this.health_number = "";
            
            this.request_by_username = change_to_username;

        },

        /**
         * 
         */
        async accept_permission(idx, medic_username) {
            return await this.$axios.$get("/permission/" + medic_username + "/accept", this.requests_header)
            .then(res => {
                if (res.status == 0) {
                    this.$toasted.show(
                        'Permission accepted', 
                        {
                            position: 'bottom-center',
                            duration: 7500
                        }
                    );
                    this.permissions.accepted.push(
                        this.permissions.pending[idx]
                    );
                    this.permissions.pending.splice(idx, 1);
                }
                else if (res.status == 1) {
                    this.$toasted.show(
                        res.msg,
                        {
                            position: 'bottom-center',
                            duration: 7500
                        }
                    );
                }
                else {
                    console.log("status code: " + res.status);
                    console.log("error msg: " + res.msg);
                    this.$toasted.show(
                        "Error accepting permission. Try again later.",
                        {
                            position: 'bottom-center',
                            duration: 7500
                        }
                    );
                }
            })
            .catch(e => {
                console.log(e);
                this.$toasted.show(
                    "Error accepting permission. Try again later.",
                    {
                        position: 'bottom-center',
                        duration: 7500
                    }
                );
            })
        },

    }
}
</script>

<style>
</style>
