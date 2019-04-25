<template>
    <div>
        <body>
            <!--================ Header Menu Area =================-->
            <HeaderMenu activePage="About" />

            <!--================ Banner Area =================-->
            <PageBanner page="About" parent_page="Home" />

            <!--================ Content Area =================-->
            <section class="sample-text-area">
                <div class="container">
                    <h1 class="text-heading title_color">About ContinuousCare</h1>
                    <p class="sample-text">This is a project for the 'Projeto em Informática' subject of the 3rd year of LEI (2018/19).</p>
                    <p class="sample-text">The main purpose of this project is to develop a web information system that allows the integrated collecting and visualization of clinical and environmental data sources related to the daily life of a citizen.</p>
                    <p class="sample-text">The solution must be capable of automatically collecting several types of data, such as weather conditions, air quality indicators, vital signals, geolocalization, etc. On the other side, the application must allow the simplified registration of basic physical and mental health states of a person, such as local pains, depression, anxiety, fatigue, etc.</p>
                </div>
            </section>

            <section class="team-area section_gap">
                <div class="container">
                     <h1 class="text-heading title_color">Our Team</h1>
                    <div class="row justify-content-center d-flex align-items-center">
                        <TeamMemberBox name="André Pedrosa" description="Back-End Developer" image="andre" slack_profile="https://slack.com/" git_profile="https://github.com/" />
                        <TeamMemberBox name="Filipe Pires" description="Front-End Developer" image="filipe" slack_profile="https://slack.com/" git_profile="https://github.com/" />
                        <TeamMemberBox name="João Alegria" description="Back-End Developer" image="joao" slack_profile="https://slack.com/" git_profile="https://github.com/" />
                    </div>
                </div>
            </section>

            <!--================ Footer Area =================-->
            <PageFooter />
            
        </body>
        <nuxt/>
    </div>
</template>

<script>
import TeamMemberBox from '@/components/boxes/TeamMemberBox.vue'

export default {
    components: {
        TeamMemberBox,
    },
    head: {
        title: "About"
    }
}
</script>

<style scoped>
    h1 { font-size: 36px; }
</style>
