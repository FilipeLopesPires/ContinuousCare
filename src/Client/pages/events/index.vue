<template>
    <div>
        <body>
            <!--================ Header Menu Area =================-->
            <HeaderMenu activePage="Events" />

            <!--================ Banner Area =================-->
            <PageBanner parent_page="Home" page="Events" />

            <div class="justify-content-center d-flex" style="min-height:50vh">
                <div class="justify-content-center d-flex align-items-top col-lg-11 col-md-11 max-width-1920 row">
                    <div class="col-lg-5 col-md-12 col-sm-12 col-xs-12 mr--30 mt-30">
                        <Events style="height:500px;" @clicked="changeEvent" :startTime="startEvents" :endTime="endEvents" :intervalTime="intervalEvents" :refresh="refresh" :title="title"/>
                    </div>
                    <div class="col-lg-7 col-md-12 col-sm-12 col-xs-12 ml--30">
                        <div class="col-lg-10 col-md-10 col-sm-10 col-xs-10" style="margin: auto; margin-top:29px">
                            <h3 class="widget_title"> Your most frequent episodes </h3>
                            <apexchart @click="mapClick" type=pie width=100% :options="chartOptions" :series="series" />
                        </div>
                    </div>
                </div>
            </div>

            <CompareTable @clicked="changeEvent" id="comparator" :event="event" :startTime="startEvents" :endTime="endEvents" :intervalTime="intervalEvents" style="width: 90%; margin:auto; margin-bottom:50px; padding-top:70px; margin-top:-60px;"/>
            
            
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
import CompareTable from '@/components/boxes/CompareTable.vue'

export default {
    middleware: ['check-log', 'log', 'clients-only'],
    components: {
        Events,
        EventComparator,
        EventOptions,
        CompareTable,
    },
    data() {
        var d = new Date()
        return {
            title: "Month's Events",
            refresh:null,
            startEvents:parseInt(d.setMonth(d.getMonth() - 1)/1000),
            endEvents:parseInt(new Date().getTime()/1000),
            intervalEvents:null,
            event:"",
            width:0,
            height:0,
            series: [1],
            chartOptions: {
                labels: ["No Events"],
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
        var params = this.$route.params
        if(Object.keys(params).length>0 && Object.keys(params).includes("event")){
            this.event=params.event
            this.$scrollTo("#comparator", 500, this.options)
        }
        this.updateChart()
    },
    methods: {
        async updateChart(){
            const config = {
                params: {'start': this.startEvents, 'end': this.endEvents},
                headers: {'AuthToken': this.$store.getters.sessionToken},
                validateStatus: function (status) {
                    return (status >= 200 && status < 300) || status == 406 || status == 401;
                },
            }
            await this.$axios.$get("/event", config)
            .then(res => {
                if(res.status==0){
                    var tmp={}
                    var ser=[]
                    var lab={
                        labels: [],
                        responsive: [{
                            breakpoint: 480,
                            options: {
                                legend: {
                                    position: 'bottom'
                                }
                            }
                        }]
                    }
                    var events=res.data
                    if("time" in events){
                        for(var i=events["time"].length-1; i>-1; i--){
                            var evt = JSON.parse(events["events"][i])
                            if(evt){
                                for(var j=0; j<evt["events"].length;j++){
                                    var title=evt["events"][j]
                                    if(Object.keys(tmp).includes(title)){
                                        tmp[title]+=1
                                    }else{
                                        tmp[title]=1
                                    }
                                }
                            }
                        }
                        var orderedValues = Object.values(tmp).sort().reverse()
                        for(let i=0; i<10; i++){
                            for(var key in tmp){
                                if(tmp[key]==orderedValues[i]){
                                    ser.push(tmp[key])
                                    lab.labels.push(key)
                                    this.$delete(tmp, key)
                                    break
                                }
                            }
                        }

                        let sum=0
                        for(let i=10; i<Object.keys(tmp).length; i++){
                            for(var key in tmp){
                                if(tmp[key]==orderedValues[i]){
                                    sum+=tmp[key]
                                    this.$delete(tmp, key)
                                    break
                                }
                            }
                        }
                        if(sum!=0){
                            ser.push(sum)
                            lab.labels.push("Others")
                        }

                        this.series=ser
                        this.chartOptions=lab
                    }
                }else if(res.status==1){
                    this.$toasted.show(res.msg, 
                                {position: 'bottom-center', duration: 7500});
                }else{
                    console.log("Error status: ", res.status);
                    console.log("Message: ", res.msg);
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
        mapClick(event, chartContext, config){
            if(config.globals.labels[config.globals.selectedDataPoints[0]]!="No Events"){
                this.changeEvt(config.globals.labels[config.globals.selectedDataPoints[0]])
            }
        },
        changeEvent(eventTitle, w, h, objective){
            if(objective=="refresh"){
                this.updateChart()
                this.event="refresh"
                this.refresh=eventTitle
                return
            }
            if(eventTitle=="Others"){
                return
            }
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
            if(eventTitle=="Others"){
                return
            }
            if(eventTitle){
                this.event=eventTitle
                this.$scrollTo("#comparator", 500, this.options)
            }
        },
    },
    head: {
        title: "Events"
    }
}
</script>

<style scoped>
.widget_title {
    font-size: 18px;
    line-height: 25px;
    background: #3face4;
    text-align: center;
    color: #fff;
    padding: 8px 0px;
    margin-bottom: 30px; }
</style>
