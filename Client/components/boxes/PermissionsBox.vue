<template>
    <table class="w-100" :id="title.toLowerCase()">
        <thead>
            <tr>
                <th>Username</th>
                <th>Full Name</th>
                <th v-if="user_type === 'medic'">Health Number</th>
                <th v-if="user_type === 'client'">Company</th>
                <th v-if="title === 'Pending'">Duration</th>
                <th v-else-if="title === 'Accepted' || title === 'Active'">Time Left</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="permission in permissions" :key="permission.username">
                <td>{{ permission.username }}</td>
                <td>{{ permission.full_name }}</td>
                <td v-if="user_type === 'medic'">{{ permission.health_number }}</td>
                <td v-if="user_type === 'client'">{{ permission.company }}</td>
                <td>{{ permission.duration }}</td>

                <td>
                    <div v-if="title === 'Pending'">
                        <div v-if="user_type === 'medic'">
                            <a @click="remove_pending(permission.username)" class="genric-btn danger circle"><i class="fa fa-trash" aria-hidden="true"></i></a>
                        </div>
                        <div v-if="user_type === 'client'">
                            <a @click="accept_permission(permission.username)" class="genric-btn success circle">
                                <i class="fa fa-check" aria-hidden="true"></i>
                            </a>
                            <a @click="reject_permission(permission.username)" class="genric-btn danger circle">
                                <i class="fa fa-times" aria-hidden="true"></i>
                            </a>
                        </div>
                    </div>
                    <div v-else-if="title === 'Accepted'">
                        <div v-if="user_type === 'medic'">
                            <a class="genric-btn success circle"><i class="fa fa-play" aria-hidden="true"></i></a>
                        </div>
                        <div v-if="user_type === 'client'">
                            <a @click="remove_accepted(permission.username)" class="genric-btn danger circle"><i class="fa fa-trash"></i></a>
                        </div>
                    </div>
                    <div v-else-if="title === 'Active'">
                        <div v-if="user_type === 'medic'">
                            <a @click="remove_active(permission.username)" class="genric-btn warning circle"><i class="fa fa-pause"></i></a>
                        </div>
                        <div v-if="user_type === 'client'">
                            <a @click="pause_active(permission.username)" class="genric-btn danger circle"><i class="fa fa-trash"></i></a>
                        </div>
                    </div>
                </td>
            </tr>
        </tbody>
    </table>
</template>

<script>

export default {
    name: 'PermissionsBox',
    props: {
        title: {
            type: String,
            required: true
        },
        user_type: {
            type: String,
            required: true
        }
    },
    data() {
        return {
            permissions: [
                {
                    username: "aspedrosa",
                    full_name: "André Pedrosa",
                    company: "Hospital Leiria",
                    health_number: 111111111,
                    duration: 10
                },
                {
                    username: "zonnax",
                    full_name: "Rodrigo Loureiro",
                    company: "Hospital Leiria",
                    health_number: 111111112,
                    duration: 10
                }
            ]
        }
    },
    methods: {
        /**
         * 
         */
        async accept_permission(medic_username) {
            return await this.$axios.$post("", {

            })
            .then(res => {

            })
            .catch(e => {

            })
        },

        /**
         * 
         */
        async reject_permission(medic_username) {
            return await this.$axios.$post("", {

            })
            .then(res => {

            })
            .catch(e => {

            })
        },

        /**
         * 
         */
        async remove_pending(client_username) {
            return await this.$axios.$post("", {

            })
            .then(res => {

            })
            .catch(e => {

            })
        },

        /**
         * 
         */
        async remove_accepted(medic_username) {
            return await this.$axios.$post("", {

            })
            .then(res => {

            })
            .catch(e => {

            })
        },

        /**
         * 
         */
        async remove_active(medic_username) {
            return await this.$axios.$post("", {

            })
            .then(res => {

            })
            .catch(e => {

            })
        },

        /**
         * 
         */
        async pause_active(client_username) {
            return await this.$axios.$post("", {

            })
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
