<template>
    <div>
        <body>
            <!--================ Header Menu Area =================-->
            <HeaderMenu activePage="Events" />

            <!--================ Banner Area =================-->
            <PageBanner parent_page="Home" page="Events" />

            <div class="justify-content-center d-flex align-items-top">
                <div class="justify-content-center d-flex align-items-top col-lg-11 col-md-11 max-width-1920 row">
                    <div class="col-lg-5 col-md-12 col-sm-12 col-xs-12 mr--30 mt-30 ">
                        <Events style="height:500px;" @clicked="changeEvent" :startTime="startEvents" :endTime="endEvents"/>
                    </div>
                    <div class="col-lg-7 col-md-12 col-sm-12 col-xs-12 ml--30">
                        <div class="col-lg-10 col-md-10 col-sm-10 col-xs-10" style="margin: auto">
                            <apexchart style="margin-top:100px" type=pie width=100% :options="chartOptions" :series="series" />
                        </div>
                    </div>
                </div>
            </div>
            <div id="comparator">
                <EventComparator :event="event" :startTime="startEvents" :endTime="endEvents"/>
            </div>
            <EventOptions :height="height" :width="width" :options="options" @option="changeEvt"/>
            
            <!--================ Footer Area =================-->
            <PageFooter />

        </body>
        <nuxt/>
    </div>
</template>

<script>
import Events from '@/components/events/Events.vue'
import EventComparator from '@/components/events/EventComparator.vue'
import EventOptions from '@/components/modals/EventOptions.vue'

export default {
    middleware: ['check-log', 'log', 'clients-only'],
    components: {
        Events,
        EventComparator,
        EventOptions,
    },
    data() {
        var d = new Date()
        return {
            startEvents:parseInt(d.setMonth(d.getMonth() - 1)/1000),
            endEvents:parseInt(new Date().getTime()/1000),
            event:"",
            width:"",
            height:"",
            options:[],
            series: [],
            chartOptions: {
                labels: [],
                responsive: [{
                    breakpoint: 480,
                    options: {
                        legend: {
                            position: 'bottom'
                        }
                    }
                }]
            },
            options: {
                easing: 'ease-in',
                force: true,
                cancelable: true,
                x: false,
                y: true
            },
        }
    },
    async mounted() {
        const config = {
            params: {'start': this.startEvents, 'end': this.endEvents},
            headers: {'AuthToken': this.$store.getters.sessionToken}
        }
        await this.$axios.$get("/event", config)
        .then(res => {
            if(res.status==0){
                var events=res.data
                console.log(events)
                if("time" in events){
                    for(var i=events["time"].length-1; i>-1; i--){
                        var evt = JSON.parse(events["events"][i])
                        if(evt){
                            for(var j=0; j<evt["events"].length;j++){
                                var title=evt["events"][j]
                                if(this.chartOptions.labels.includes(title)){
                                    this.series[this.chartOptions.labels.indexOf(title)]+=1
                                }else{
                                    this.series.push(1)
                                    this.chartOptions.labels.push(title)
                                }
                            }
                        }
                    }
                }
            }else if(res.status==1){
                this.$toasted.show(res.msg, 
                            {position: 'bottom-center', duration: 7500});
            }else{
                this.$toasted.show('Something went wrong while getting your events. Please try again, if it still does not work, contact us through email.', 
                            {position: 'bottom-center', duration: 7500});
            }
        })
        .catch(e => {
            // Unable to get devices from server
            console.log(e)
            this.$toasted.show('Something went wrong while trying to retrieve data. The server might be down at the moment. Please try again later.', 
                {position: 'bottom-center', duration: 7500});
        });
    },
    methods: {
        changeEvent(eventTitle, w, h){
            if(eventTitle.split(", ").length>1){
                this.width=w
                this.height=h
                this.options=eventTitle.split(", ")
                this.$modal.show("eventOptions")
            }else{
                this.event=eventTitle
                this.$scrollTo("#comparator", 500, this.options)
            }
        },
        changeEvt(eventTitle){
            console.log(eventTitle)
            this.event=eventTitle
            this.$scrollTo("#comparator", 500, this.options)
        },
    },
    head: {
        title: "Events"
    }
}
</script>

<style scoped>

</style>
