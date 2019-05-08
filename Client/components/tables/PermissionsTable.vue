<template>
    <table class="w-100">
        <thead>
            <tr>
                <th>Username</th>
                <th>Full Name</th>
                <th v-if="user_type === 'medic'">Health Number</th>
                <th v-if="user_type === 'client'">Company</th>
                <th v-if="title === 'pending'">Duration</th>
                <th v-else-if="title === 'accepted' || title === 'active'">Time Left</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="(permission, index) in permissions" :key="permission.username">
                <td>{{ permission.username }}</td>
                <td>{{ permission.full_name }}</td>
                <td v-if="user_type === 'medic'">{{ permission.health_number }}</td>
                <td v-if="user_type === 'client'">{{ permission.company }}</td>
                <td>{{ permission.duration }}</td>

                <td>
                    <div v-if="title === 'pending'">
                        <div v-if="user_type === 'medic'">
                            <button @click="remove_pending(index, permission.username)" class="genric-btn primary radius"><i class="fa fa-trash" aria-hidden="true"></i></button>
                        </div>
                        <div v-if="user_type === 'client'">
                            <button @click="accept_permission(index, permission.username)" class="genric-btn info radius">
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
                            <button @click="pause_active(index, permission.username)" class="genric-btn success radius"><i class="fa fa-pause"></i></button>
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
    methods: {
        /**
         * 
         */
        async accept_permission(idx, medic_username) {
            this.permissions.splice(idx, 1);

            return await this.$axios.$post("/permission/accept", {

            })
            .then(res => {

            })
            .catch(e => {

            })
        },

        /**
         * 
         */
        async reject_permission(idx, medic_username) {
            this.permissions.splice(idx, 1);

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
        async remove_pending(idx, client_username) {
            this.permissions.splice(idx, 1);

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
        async remove_accepted(idx, medic_username) {
            this.permissions.splice(idx, 1);

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
        async remove_active(idx, medic_username) {
            this.permissions.splice(idx, 1);

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
        async pause_active(idx, client_username) {
            this.permissions.splice(idx, 1);

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
