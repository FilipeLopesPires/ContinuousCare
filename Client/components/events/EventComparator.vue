<template>
    <b-container style="padding-top:90px">
        <h3 v-if="event" class="widget_title"> All {{event}} episodes of the month </h3>
            <b-row class="justify-content-center">
                <b-col lg="3" md="4" sm="6" xs="12" v-for='evt in eventToShow' :key="evt.id" style="margin-bottom: 15px;">
                    <div class="event" style="cursor:pointer;">
                        <p class='event-date' v-html="evt.time"></p>
                        <h3><a v-html="evt.title"></a></h3>
                        <p v-html="evt.content"></p>
                    </div>
                </b-col>
            </b-row>
    </b-container>
</template>

<script>

export default {
    name: 'EventComparator',
    props: [
        "event",
        "startTime",
        "endTime",
    ],
    data() {
      return {
        eventToShow:[],
        height:null,
        width:null,
        healthSate:null,
        envState:null,
      }
    },
    watch:{
        event: function() {
            var health=false
            var env=false

            const config = {
                params: {'start': this.startTime, 'end': this.endTime},
                headers: {'AuthToken': this.$store.getters.sessionToken}
            }


            this.$axios.$get("/healthstatus", config)
            .then(res => {
                if(res.status==0){
                    var output={}
                    var status=res.data
                    if("time" in status){
                        for(var key in status){
                            if(!"time,latitude,longitude".includes(key)){
                                if(status[key][status["time"].length-1]){
                                    output[key]=status[key][status["time"].length-1]
                                }
                            }
                        }
                    }
                    this.healthState=output
                    health=true
                } else if(res.status == 4) {
                    this.$toasted.show(res.msg, {position: 'bottom-center', duration: 7500});
                    this.$router.push("/login");
                } else if(res.status==1){
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
            })


            this.$axios.$get("/environment", config)
            .then(res => {
                if(res.status==0){
                    var output={}
                    var status=res.data
                    if("time" in status){
                        for(var key in status){
                            if(!"time,latitude,longitude".includes(key)){
                                if(status[key][status["time"].length-1]){
                                    output[key]=status[key][status["time"].length-1]
                                }
                            }
                        }
                    }
                    this.envState=output
                    env=true
                } else if(res.status == 4) {
                    this.$toasted.show(res.msg, {position: 'bottom-center', duration: 7500});
                    this.$router.push("/login");
                } else if(res.status==1){
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
            })


            while(!(health && env)){}


            this.$axios.$get("/event", config)
            .then(res => {
                if(res.status==0){
                    var events=res.data
                    if("time" in events){
                        var newEvents=[]
                        for(var i=events["time"].length-1; i>-1; i--){
                            var title = ""
                            var content = ""
                            var evt = JSON.parse(events["events"][i])
                            if(evt){
                                for(var j=0; j<evt["events"].length;j++){
                                    if(evt["events"][j]==this.event){
                                        title+=evt["events"][j]+", "
                                        for(let [key, value] of Object.entries({...this.healthState, ...this.envState})){
                                            if(evt["metrics"].includes(key)){
                                                content+="<font color=\"red\">"+key+": "+value+"</font><br>"
                                            }else{
                                                content+=key+": "+value+"<br>"
                                            }
                                        }
                                    }
                                }
                            }
                            if(title!=""){
                                newEvents.push({
                                "time": events["time"][i],
                                "title": title.slice(0,-2),
                                "content": content,
                                })
                            }
                        }
                        this.eventToShow = newEvents
                    }
                } else if(res.status == 4) {
                    this.$toasted.show(res.msg, {position: 'bottom-center', duration: 7500});
                    this.$router.push("/login");
                } else if(res.status==1){
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
                this.requestError = true;
            })
        }
    },
}

</script>

<style scoped>
.event {
    box-shadow: 3px 5px 10px 2px rgba(0, 0, 0, 0.2);
    border-radius: 5px;
    padding: 10px;
    width: 105%;
}
.event:hover {
    box-shadow: 3px 5px 10px 2px rgba(0, 0, 0, 0.4);
}
.event a {
    color: #006699;
    text-decoration: none;
}
.event .event-date {
    font-weight: 300;
    font-size: 14px;
}
.widget_title {
    font-size: 18px;
    line-height: 25px;
    background: #3face4;
    text-align: center;
    color: #fff;
    padding: 8px 0px;
    margin-bottom: 30px; }
</style>
