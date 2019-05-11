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
                <div class="form-inline">
                    <span class="col-md-3">Hours</span>
                    <input ref="duration_hours_input" class="single-input col-md-3">
                    <span class="col-md-3">Minutes</span>
                    <input ref="duration_minutes_input" class="single-input col-md-3">
                </div>
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
                        <PermissionsTable title="pending" :user_type="user_type" :permissions="permissions.pending" v-on:accept="accept_permission" />
                    </b-tab>
                    <b-tab title="Accepted">
                        <PermissionsTable title="accepted" :user_type="user_type" :permissions="permissions.accepted" v-on:start="start_permission" />
                    </b-tab>
                    <b-tab title="Active">
                        <PermissionsTable title="active" :user_type="user_type" :permissions="permissions.active" v-on:stop="stop_permission" />
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
            client_username: "",
            toast_configs: {
                position: 'bottom-center',
                duration: 7500
            }
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
                    this.toast_configs
                );
            else
                this.display_error_toasts(false, res, "retrieving permissions");
            return {
                pending: [],
                accepted: [],
                active: []
            };
        })
        .catch(e => {
            this.display_error_toasts(true, e, "retrieving permissions");
            return {
                pending: [],
                accepted: [],
                active: []
            };
        });
    },
    methods: {
        /**
         * Function to reduce some code duplication.
         * Prints the error data accordingly if it is an
         *  exception or a status code other than 0 or 1.
         * Also displays a toast, building the massage with the
         *  rest of the message received.
         */
        display_error_toasts(is_exception, error_data, error_message) {
            if (is_exception)
                console.log(error_data);
            else {
                console.log("status code: " + error_data.status);
                console.log("error data: " + error_data.msg);
            }

            this.$toasted.show(
                'Error ' + error_message + ". Try again later or refresh the page.",
                this.toast_configs
            );
        },

        /**
         * Parses both hours and minutes and converts to minutes.
         * Returns -1 in case some of the inputs are not in number
         *  format. Otherwise returns the number of minutes parsed.
         *  It should be checked if this functino returned a number
         *  lower or equal than 0 to abort requests
         */
        parse_duration(hours, minutes) {
            if (! /^\d+$/.test(hours) && hours !== "") {
                this.$toasted.show(
                    'Invalid hours.',
                    this.toast_configs
                );
                return -1;
            }
            if (! /^\d+$/.test(minutes) && minutes !== "") {
                this.$toasted.show(
                    'Invalid minutes.',
                    this.toast_configs
                );
                return -1;
            }

            minutes = minutes === "" ? 0 : parseInt(minutes);
            minutes += hours === "" ? 0 : parseInt(hours);

            if (!(minutes > 0)) {
                this.$toasted.show(
                    'Insert a duration higher than 0',
                    this.toast_configs
                );
                return -1;
            }

            return minutes;
        },

        async request_permission() {
            let username = this.$refs.client_username_input.value;
            let health_number = this.$refs.health_number_input.value;
            let hours = this.$refs.duration_hours_input.value;
            let minutes = this.$refs.duration_minutes_input.value;

            // ARGUMENTS VALIDATION vv
            if (this.request_by_username) {
                if (username == "") {
                    this.$toasted.show(
                        'Insert a username.',
                        this.toast_configs
                    );
                    return;
                }

                health_number = null;
            }
            else {
                if (health_number == "") {
                    this.$toasted.show(
                        'Insert a health number.',
                        this.toast_configs
                    );
                    return;
                }
                else if (! /^\d+$/.test(health_number)) {
                    this.$toasted.show(
                        'Invalid health number.',
                        this.toast_configs
                    );
                    return;
                }

                username = null;
            }

            if ((minutes = this.parse_duration(hours, minutes)) <= 0)
                return;
            // ARGUMENTS VALIDATION ^^

            this.close_modal();

            await this.$axios.$post("/permission", {
                username: username,
                health_number: health_number,
                duration: minutes
            }, this.requests_header)
            .then(res => {
                if (res.status == 0) {
                    this.$toasted.show(
                        'Permission requested.',
                        this.toast_configs
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
                        this.toast_configs
                    );
                }
                else
                    this.display_error_toasts(false, res, "requesting permission");
            })
            .catch(e => this.display_error_toasts(true, e, "requesting permission"))
        },

        async grant_permission() {
            let username = this.$refs.medic_username_input.value;
            let hours = this.$refs.duration_hours_input.value;
            let minutes = this.$refs.duration_minutes_input.value;

            // ARGUMENTS VALIDATION vv
            if (username == "") {
                this.$toasted.show(
                    'Insert a username.',
                    this.toast_configs
                );
                return;
            }

            if ((minutes = this.parse_duration(hours, minutes)) <= 0)
                return;
            // ARGUMENTS VALIDATION ^^

            this.close_modal();

            await this.$axios.$post("/permission", {
                username: username,
                duration: minutes
            }, this.requests_header)
            .then(res => {
                if (res.status == 0) {
                    this.$toasted.show(
                        'Permission granted.',
                        this.toast_configs
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
                        this.toast_configs
                    );
                else
                    this.display_error_toasts(false, res, "granting permission")
            })
            .catch(e => this.display_error_toasts(true, e, "granting permission"))
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

            this.$refs.duration_hours_input.value = "";
            this.$refs.duration_minutes_input.value = "";

            this.$refs.request_grant_permission_modal.hide();
        },

        /**
         * Function called whenever a MEDIC uses the checkbox's
         *  present on the modal to request permission.
         * This checkboxes swtich between requesting permission
         *  using health number or the username
         */
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
         * Merge permissions related to the same user by adding
         *  the duration
         */
        merge_permissions(source, destination, idx, username_of_moved) {
            let permission = destination.find(permission => {
                return permission.username === username_of_moved;
            });

            // If an source permissiosn exists merge the durations with the one on the destination
            if (permission !== undefined) {
                let destination_duration = permission.duration.split(":");
                let destination_hours = parseInt(duration[0]);
                let destination_minutes = parseInt(duration[1]);

                let source_duration = source[idx].duration.split(":");
                let source_hours = parseInt(duration[0]);
                let source_minutes = parseInt(duration[1]);

                if (source_minutes + destination_minutes > 60)
                    permission.duration = (source_hours + destination_hours + 1) + ":" + (source_minutes + source_minutes - 60);
                else
                    permission.duration = (source_hours + destination_hours) + ":" + (source_minutes + source_minutes);
            }
            // Else just move the permission
            else {
                destination.push(
                    source[idx]
                );
            }

            source.splice(idx, 1);
        },

        async accept_permission(idx, medic_username) {
            return await this.$axios.$get("/permission/" + medic_username + "/accept", this.requests_header)
            .then(res => {
                if (res.status == 0) {
                    this.$toasted.show(
                        'Permission accepted',
                        this.toast_configs
                    );

                    merge_permissions(this.permissions.pending, this.permissions.accepted, idx, medic_username);
                }
                else if (res.status == 1) {
                    this.$toasted.show(
                        res.msg,
                        this.toast_configs
                    );
                }
                else
                    this.display_error_toasts(false, res, "accepting permission")
            })
            .catch(e => this.display_error_toasts(true, e, "accepting permission"))
        },

        /**
         * TODO
         */
        async start_permission(idx, client_username) {

            return;

            return await this.$axios.$post("", this.requests_header)
            .then(res => {
                if (res.status == 0) {
                    this.$toasted.show(
                        "Permission started.",
                        this.toast_configs
                    );

                    //merge_permissions(this.permissions.accepted, this.permissions.active, idx, client_username); //maybe some times no
                }
                else if (res.status == 1) {
                    this.$toasted.show(
                        res.msg,
                        this.toast_configs
                    );
                }
                else
                    this.display_error_toasts(false, res, "starting permission")
            })
            .catch(e => this.display_error_toasts(true, e, "starting permission"))
        },

        async stop_permission(idx, client_username) {
            return await this.$axios.$get("/permission/" + client_username + "/stop", this.requests_header)
            .then(res => {
                if (res.status == 0) {
                    this.$toasted.show(
                        "Active permission stopped.",
                        this.toast_configs
                    );

                    merge_permissions(this.permissions.active, this.permissions.accepted, idx, client_username);
                }
                else if (res.status == 1) {
                    this.$toasted.show(
                        res.msg,
                        this.toast_configs
                    );
                }
                else
                    this.display_error_toasts(false, res, "stoping permission")
            })
            .catch(e => this.display_error_toasts(true, e, "stoping permission"))
        }
    }
}
</script>

<style>
</style>
