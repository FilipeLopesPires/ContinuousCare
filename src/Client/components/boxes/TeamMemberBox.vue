<template>
    <div class="col-lg-3 col-md-6 single-team mb-50">
        <div class="thumb">
            <img v-if="image=='andre'" class="img-fluid" src="~/assets/img/team/andre.jpg" alt="">
            <img v-if="image=='filipe'" class="img-fluid" src="~/assets/img/team/filipe.jpg" alt="">
            <img v-if="image=='joao'" class="img-fluid" src="~/assets/img/team/joao.jpg" alt="">
            <div class="align-items-end justify-content-center d-flex">
                <div class="social-links">
                    <a :href="slack_profile">
                        <i class="fa fa-slack"></i>
                    </a>
                    <a :href="git_profile">
                        <i class="fa fa-github"></i>
                    </a>
                </div>
                <p> {{ description }} </p>
                <h4> {{ name }} </h4>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'TeamMemberBox',
    props: {
        slack_profile: {
            type: String,
            required: true
        },
        git_profile: {
            type: String,
            required: true
        },
        image: {
            type: String,
            required: true
        },
        description: {
            type: String,
            required: true
        },
        name: {
            type: String,
            required: true
        },
    }
}
</script>

<style>

</style>
