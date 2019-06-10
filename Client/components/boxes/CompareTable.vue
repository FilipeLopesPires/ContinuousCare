<template>
    <div>
        <h3 class="widget_title" id="eventName" style="visibility:hidden"></h3>
        <b-table responsive hover :items="eventToShow" :fields="fields"></b-table>
    </div>
</template>



<script>

export default {
    name: 'CompareTable',
    props: [
        "event",
        "startTime",
        "intervalTime",
        "endTime",
        "patient",
        "refresh"
    ],
    data() {
      return {
        fields:[],
        oldEvent:"",
        eventToShow:[],
      }
    },
    methods: {
        formatDateTime(datetime) {
            var d = new Date(datetime);

            Number.prototype.padLeft = function(base,chr){
                var len = (String(base || 10).length - String(this).length)+1;
                return len > 0? new Array(len).join(chr || '0')+this : this;
            }

            var retval = [(d.getMonth()+1).padLeft(),
                        d.getDate().padLeft(),
                        d.getFullYear()].join('/') +' ' +
                        [d.getHours().padLeft(),
                        d.getMinutes().padLeft(),
                        d.getSeconds().padLeft()].join(':');
            return retval;
        },


        async getEnvStatus(config){
            var result={}
            await this.$axios.$get("/environment", config)
            .then(res => {
                if(res.status==0){
                    var status=res.data
                    if("time" in status){
                        status["time"].forEach(function(time, i){
                            var output={}
                            for(var key in status){
                                if(!"time,latitude,longitude".includes(key)){
                                    if(status[key][i]){
                                        output[key]=status[key][i]
                                    }
                                }
                            }
                            result[time]=output
                        })
                    }
                } else if(res.status == 4) {
                    this.$toasted.show(res.msg, {position: 'bottom-center', duration: 7500});
                    this.$store.dispatch('logout'),
                    this.$router.push("/login")
                } else if(res.status==1){
                    this.$toasted.show(res.msg, 
                                {position: 'bottom-center', duration: 7500});
                    result={}
                }else{
                    this.$toasted.show('Something went wrong while getting your events. Please try again, if it still does not work, contact us through email.', 
                                {position: 'bottom-center', duration: 7500});
                    result={}
                }
            })
            .catch(e => {
                // Unable to get devices from server
                console.log(e)
                this.$toasted.show('Something went wrong while trying to retrieve data. The server might be down at the moment. Please try again later.', 
                    {position: 'bottom-center', duration: 7500});
                result={}
            })
            return result
        },
        async getHealthStatus(config){
            var result={}
            await this.$axios.$get("/healthstatus", config)
            .then(res => {
                if(res.status==0){
                    var status=res.data
                    if("time" in status){
                        status["time"].forEach(function(time, i){
                            var output={}
                            for(var key in status){
                                if(!"time,latitude,longitude".includes(key)){
                                    if(status[key][i]){
                                        output[key]=status[key][i]
                                    }
                                }
                            }
                            result[time]=output
                        })
                    }
                } else if(res.status == 4) {
                    this.$toasted.show(res.msg, {position: 'bottom-center', duration: 7500});
                    this.$store.dispatch('logout'),
                    this.$router.push("/login")
                } else if(res.status==1){
                    this.$toasted.show(res.msg, 
                                {position: 'bottom-center', duration: 7500});
                    result={}
                }else{
                    this.$toasted.show('Something went wrong while getting your events. Please try again, if it still does not work, contact us through email.', 
                                {position: 'bottom-center', duration: 7500});
                    result={}
                }
            })
            .catch(e => {
                // Unable to get devices from server
                console.log(e)
                this.$toasted.show('Something went wrong while trying to retrieve data. The server might be down at the moment. Please try again later.', 
                    {position: 'bottom-center', duration: 7500});
                result={}
            })
            return result
        },
        async showEvents(config){

            $("#eventName").text(this.event)
            $("#eventName").css("visibility", "visible")

            var healthState = await this.getHealthStatus(config)
            var envState = await this.getEnvStatus(config)
            await this.$axios.$get("/event", config)
            .then(res => {
                if(res.status==0){
                    var events=res.data
                    console.log(events)
                    if("time" in events){
                        var newEvents=[]
                        var myFields=[]
                        for(var i=events["time"].length-1; i>-1; i--){
                            var title = ""
                            var content = ""
                            var evt = JSON.parse(events["events"][i])
                            if(evt){
                                for(var j=0; j<evt["events"].length;j++){
                                    var eventInstance = {}
                                    if(evt["events"][j]==this.event){
                                        if(!("Time" in myFields)){
                                            myFields.push("Time")
                                        }
                                        eventInstance["Time"]=this.formatDateTime(events["time"][i])




                                        var healthKey=""
                                        var healthValue
                                        for(var key in Object.keys(healthState).sort()){
                                            if(Object.keys(healthState).sort()[key]>events["time"][i]){
                                                break;
                                            }
                                            if(Object.keys(healthState).sort()[key]===events["time"][i]){
                                                healthKey=key
                                                healthValue=healthState[Object.keys(healthState).sort()[key]]
                                                break;
                                            }
                                            healthKey=key
                                            healthValue=healthState[Object.keys(healthState).sort()[key]]
                                        }
                                        if(healthKey==""){
                                            healthValue=healthState[Object.keys(healthState).sort()[0]]
                                        }


                                        for(var keySecond in healthValue){
                                            if(evt["metrics"].includes(keySecond)){
                                                if(!("_cellVariants" in eventInstance)){
                                                    eventInstance["_cellVariants"] = {}
                                                }
                                                eventInstance["_cellVariants"][keySecond] = "danger"
                                            }
                                            
                                            if(!(keySecond in myFields)){
                                                myFields.push(keySecond)
                                            }
                                            eventInstance[keySecond] = healthValue[keySecond]
                                        }




                                        var envKey=""
                                        var envValue
                                        for(var key in Object.keys(envState).sort()){
                                            if(Object.keys(envState).sort()[key]>events["time"][i]){
                                                break;
                                            }
                                            if(Object.keys(envState).sort()[key]===events["time"][i]){
                                                envKey=key
                                                envValue=envState[Object.keys(envState).sort()[key]]
                                                break;
                                            }
                                            envKey=key
                                            envValue=envState[Object.keys(envState).sort()[key]]
                                        }
                                        if(envKey==""){
                                            envValue=envState[Object.keys(envState).sort()[0]]
                                        }


                                        for(var keySecond in envValue){
                                            if(evt["metrics"].includes(keySecond)){
                                                if(!("_cellVariants" in eventInstance)){
                                                    eventInstance["_cellVariants"] = {}
                                                }
                                                eventInstance["_cellVariants"][keySecond] = "danger"
                                            }
                                            
                                            if(!(keySecond in myFields)){
                                                myFields.push(keySecond)
                                            }
                                            eventInstance[keySecond] = envValue[keySecond]
                                        }

                                                                            

                                    }

                                    if(Object.keys(eventInstance).length !== 0){
                                        newEvents.push(eventInstance)
                                    }
                                }
                                
                            }
                        }


                        if(newEvents!=[]){
                            this.fields=myFields
                            this.eventToShow = newEvents 
                        }

                    }
                } else if(res.status == 4) {
                    this.$toasted.show(res.msg, {position: 'bottom-center', duration: 7500});
                    this.$store.dispatch('logout'),
                    this.$router.push("/login")
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
    watch:{
        event: function() {
            let config = {
                params: {'start': this.startTime, 'end': this.endTime, 'interval': this.intervalTime},
                headers: {'AuthToken': this.$store.getters.sessionToken},
            }

            if(this.patient)
                config.params.patient = this.patient;
            
            if(this.event=="refresh"){
                this.event=this.oldEvent
            }else{
                this.oldEvent=this.event
                this.showEvents(config)
            }
        },
        refresh: function() {
            let config = {
                params: {'start': this.startTime, 'end': this.endTime, 'interval': this.intervalTime},
                headers: {'AuthToken': this.$store.getters.sessionToken},
            }

            if(this.patient)
                config.params.patient = this.patient;

            this.showEvents(config);
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
