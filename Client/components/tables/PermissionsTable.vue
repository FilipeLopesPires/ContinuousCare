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
                            <button @click="$emit('ola', index, permission.username)" class="genric-btn info radius">
                                <i class="fa fa-check" aria-hidden="true"></i>
                            </button>
                            <button @click="reject_permission(index, permission.username)" class="genric-btn primary radius">
                                <i class="fa fa-times" aria-hidden="true"></i>
                            </button>
                        </div>
                    </div>
                    <div v-else-if="title === 'accepted'">
                        <div v-if="user_type === 'medic'">
                            <button class="genric-btn success radius"><i class="fa fa-play" aria-hidden="true"></i></button>
                        </div>
                        <div v-if="user_type === 'client'">
                            <button @click="remove_accepted(index, permission.username)" class="genric-btn primary radius"><i class="fa fa-trash"></i></button>
                        </div>
                    </div>
                    <div v-else-if="title === 'active'">
                        <div v-if="user_type === 'medic'">
                            <button @click="stop_active(index, permission.username)" class="genric-btn success radius"><i class="fa fa-stop"></i></button>
                        </div>
                        <div v-if="user_type === 'client'">
                            <button @click="remove_active(index, permission.username)" class="genric-btn warning radius"><i class="fa fa-trash"></i></button>
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
        }
    },
    methods: {
        /**
         * 
         */
        async reject_permission(idx, medic_username) {

            return await this.$axios.$get("/permission/" + medic_username + "/reject", this.requests_header)
            .then(res => {
                if (res.status == 0) {
                    this.$toasted.show(
                        'Permission rejected', 
                        {
                            position: 'bottom-center',
                            duration: 7500
                        }
                    );
                    this.permissions.splice(idx, 1);
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
                        "Error rejecting permission. Try again later.", 
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
                    "Error rejecting permission. Try again later.", 
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
        async remove_pending(idx, client_username) {

            return await this.$axios.$delete("/permission/" + client_username + "/pending", this.requests_header)
            .then(res => {
                if (res.status == 0) {
                    this.permissions.splice(idx, 1);
                    this.$toasted.show(
                        "Pending permissiosn deleted.",
                        {
                            position: 'bottom-center',
                            duration: 7500
                        }
                    );
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
                    console.log("status code" + res.status);
                    console.log("error message" + res.msg);
                    this.$toasted.show(
                        "Error deleting pending permission. Try again later.",
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
                    "Error deleting pending permission. Try again later.",
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
        async remove_accepted(idx, medic_username) {
            return await this.$axios.$delete("/permission/" + medic_username + "/accepted", this.requests_header)
            .then(res => {
                if (res.status == 0) {
                    this.permissions.splice(idx, 1);
                    this.$toasted.show(
                        "Accepted permissiosn deleted.",
                        {
                            position: 'bottom-center',
                            duration: 7500
                        }
                    );
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
                        "Error deleting accepted permission. Try again later.",
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
                    "Error deleting accepted permission. Try again later.",
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
        async remove_active(idx, medic_username) {

            return await this.$axios.$delete("/permission/" + medic_username + "/active", this.requests_header)
            .then(res => {
                if (res.status == 0) {
                    this.permissions.splice(idx, 1);
                    this.$toasted.show(
                        "Active permissiosn deleted.",
                        {
                            position: 'bottom-center',
                            duration: 7500
                        }
                    );
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
                        "Error deleting active permission. Try again later.",
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
                    "Error deleting active permission. Try again later.",
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
        async stop_active(idx, client_username) {
            this.permissions.splice(idx, 1);

            return await this.$axios.$post("", this.requests_header)
            .then(res => {

            })
            .catch(e => {

            })
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
