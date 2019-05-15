<template>
    <table class="w-100">
        <thead>
            <tr>
                <th>Username</th>
                <th>Full Name</th>
                <th>Email</th>
                <th v-if="user_type === 'medic'">Health Number</th>
                <th v-if="user_type === 'client'">Company</th>
                <th v-if="title === 'pending'">Duration</th>
                <th v-else-if="title === 'accepted' || title === 'active'">Time Left (Hours)</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="(permission, index) in permissions" :key="permission.username">
                <td>{{ permission.username }}</td>
                <td>{{ permission.name }}</td>
                <td>{{ permission.email }}</td>
                <td v-if="user_type === 'medic'">{{ permission.health_number }}</td>
                <td v-else-if="user_type === 'client'">{{ permission.company }}</td>
                <td>{{ permission.duration }}</td>

                <td>
                    <div v-if="title === 'pending'">
                        <div v-if="user_type === 'medic'">
                            <button @click="remove_pending(index, permission.username)" class="genric-btn primary radius"><i class="fa fa-trash" aria-hidden="true"></i></button>
                        </div>
                        <div v-if="user_type === 'client'">
                            <button @click="$emit('accept', index, permission.username)" class="genric-btn info radius">
                                <i class="fa fa-check" aria-hidden="true"></i>
                            </button>
                            <button @click="reject_permission(index, permission.username)" class="genric-btn primary radius">
                                <i class="fa fa-times" aria-hidden="true"></i>
                            </button>
                        </div>
                    </div>
                    <div v-else-if="title === 'accepted'">
                        <div v-if="user_type === 'medic'">
                            <button @click="$emit('use', permission.name, permission.username)" class="genric-btn success radius"><i class="fa fa-play" aria-hidden="true"></i></button>
                        </div>
                        <div v-if="user_type === 'client'">
                            <button @click="remove_accepted(index, permission.username)" class="genric-btn primary radius"><i class="fa fa-trash"></i></button>
                        </div>
                    </div>
                </td>
            </tr>
        </tbody>
    </table>
</template>

<script>

export default {
    name: 'PermissionsTable',
    props: {
        title: {
            type: String,
            required: true
        },
        permissions: {
            type: Array,
            required: true
        },
        user_type: {
            type: String,
            required: true
        }
    },
    data() {
        return {
            requests_header: {
                headers: {AuthToken: this.$store.getters.sessionToken},
            },
            toast_configs: {
                position: 'bottom-center',
                duration: 7500
            }
        }
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

        async reject_permission(idx, medic_username) {

            return await this.$axios.$get("/permission/" + medic_username + "/reject", this.requests_header)
            .then(res => {
                if (res.status == 0) {
                    this.$toasted.show(
                        'Permission rejected',
                        this.toast_configs
                    );
                    this.permissions.splice(idx, 1);
                }
                else if (res.status == 1) {
                    this.$toasted.show(
                        res.msg,
                        this.toast_configs
                    );
                }
                else
                    this.display_error_toasts(false, res, "rejecting permission");
            })
            .catch(e => this.display_error_toasts(true, e, "rejecting permission"));
        },

        async remove_pending(idx, client_username) {

            return await this.$axios.$delete("/permission/" + client_username + "/pending", this.requests_header)
            .then(res => {
                if (res.status == 0) {
                    this.permissions.splice(idx, 1);
                    this.$toasted.show(
                        "Pending permissiosn deleted.",
                        this.toast_configs
                    );
                }
                else if (res.status == 1) {
                    this.$toasted.show(
                        res.msg,
                        this.toast_configs
                    );
                }
                else
                    this.display_error_toasts(false, res, "deleting pending permission")
            })
            .catch(e => this.display_error_toasts(true, e, "deleting pending permission"));
        },

        async remove_accepted(idx, medic_username) {
            return await this.$axios.$delete("/permission/" + medic_username + "/accepted", this.requests_header)
            .then(res => {
                if (res.status == 0) {
                    this.permissions.splice(idx, 1);
                    this.$toasted.show(
                        "Accepted permissiosn deleted.",
                        this.toast_configs
                    );
                }
                else if (res.status == 1) {
                    this.$toasted.show(
                        res.msg,
                        this.toast_configs
                    );
                }
                else
                    this.display_error_toasts(false, res, "deleting accepted permission")
            })
            .catch(e => this.display_error_toasts(true, e, "deleting accepted permission"));
        }
    }
}
</script>

<style scoped>
.custom_button {
    width: 50px;
}
.padding {
    margin-bottom: 10px;
    margin-top: 10px;
}
</style>
