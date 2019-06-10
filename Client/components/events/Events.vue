<template>
  <div class='mycontainer mt-25'>
    <h3 class="widget_title" id="eventsTitle"></h3>
    <input v-model='searchQuery' class='single-input mb-20' placeholder='Filter your events...'>
    <VuePerfectScrollbar class="scroll-area container" :settings="settings">
      <div class='timeline' v-if='anyEvent()'>
        <div v-for='(dateWithEvents, date) in searchedEvents' :key="dateWithEvents.id">
          <p v-if='dateWithEvents.length > 0' class='date'>{{ date }}</p>
          <div v-for='event in dateWithEvents' class='event' :key="event.id" @click="info(event,eventClickObjective)" style="cursor:pointer">
            <button v-if="!patient" @click="eventClickObjective='close'" type="button" class="close" aria-label="Close" style="font-size:2rem; margin-right:5px;"><span aria-hidden="true">×</span></button>
            <span class='dot'></span>
            <p class='event-date' v-html="event.time"></p>
            <h3><a v-html="event.title"></a></h3>
            <p v-html="event.content"></p>
          </div>
        </div>
      </div>
      <p v-else>No events found.</p>
    </VuePerfectScrollbar>
  </div>
</template>

<script>
import VuePerfectScrollbar from 'vue-perfect-scrollbar'
export default {
    name: 'Events',
    props: [
      "title",
      "startTime",
      "endTime",
      "intervalTime",
      "refresh",
      "patient"
    ],
    data() {
      return {
        eventClickObjective: "show",
        datesEvents: {},
        searchQuery: '',
        settings: {
          maxScrollbarLength: 60,
          suppressScrollX: true,
        }
      }
    },
    components:{VuePerfectScrollbar},
    async mounted(){
      await this.buildEvents()      
    },
    computed: {
      searchedEvents() {
        var searchRegex = new RegExp(this.searchQuery, 'i');
        var searchedObj = {};
  
        if(this.searchQuery == '') {
           return this.datesEvents;
        }
  
        for(var date in this.datesEvents) {
          searchedObj[date] = this.datesEvents[date].filter((event) => {
            return searchRegex.test(event.title);
          });
        }
        return searchedObj;
      }
    },
    methods: {
      async buildEvents(){

        $("#eventsTitle").text(this.title)

        let config = {
          params: {'start': this.startTime, 'end': this.endTime, 'interval': this.intervalTime},
          headers: {'AuthToken': this.$store.getters.sessionToken},
        }
        if(this.patient)
          config.params.patient = this.patient;

        //console.log("before request /event", config);
        await this.$axios.$get("/event", config)
        .then(res => {
            if(res.status==0){
                var events=res.data
                var yesterday
                if("time" in events){
                    var d
                    var today 
                    var new_datesEvents = {}
                    for(var i=events["time"].length-1; i>-1; i--){
                      d = new Date(events["time"][i])
                      today = [(d.getMonth()+1), d.getDate(), d.getFullYear()].join('/')
                      if(!Object.keys(new_datesEvents).includes(today)){
                        new_datesEvents[today]=[]
                      }
                      
                      var title = ""
                      var content = ""
                      var evt = JSON.parse(events["events"][i])
                      if(evt){
                          for(var j=0; j<evt["events"].length;j++){
                            title+=evt["events"][j]+", "
                            //if data is empty the only events are related to personalStatus, else there may be some metrics and events related to personal signals
                            if(Object.keys(evt["data"]).length==0){
                              if(!content.includes(evt["metrics"][j])){
                                content+=evt["metrics"][j]+"<br>"
                              }
                            }else{
                              for (let [key, value] of Object.entries(evt["data"])) {
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
                        new_datesEvents[today].push({
                          "time": this.formatDateTime(events["time"][i]),
                          "title": title.slice(0, -2),
                          "content": content,
                          })
                      }
                  }
                  this.datesEvents = new_datesEvents
              }
          }else if(res.status==1){
              this.$toasted.show(res.msg, 
                          {position: 'bottom-center', duration: 7500});
          }
          else if(res.status == 4) {
              this.$toasted.show(res.msg, {position: 'bottom-center', duration: 7500});
              this.$store.dispatch('logout'),
              this.$router.push("/login")
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
          this.requestError = true;
        });
      },

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
      async info(evt, objective){
        if(objective=="show"){
          this.$emit("clicked", evt.title, event.clientX/window.innerWidth, event.clientY/window.innerHeight, "")
        }else{
          await this.deleteEvent(evt)
        }
        this.eventClickObjective="show"
      },
      async deleteEvent(event){
        const config = {
          headers: {'AuthToken': this.$store.getters.sessionToken},
          data: {"time": parseInt(new Date(event["time"]).getTime()/1000)}
        }
        await this.$axios.$delete("/mood", config)
        .then(res => {
            if(res.status==0){
              for(let date in this.datesEvents){
                for(let ev in this.datesEvents[date]){
                  if(this.datesEvents[date][ev]["time"]==event["time"]){
                    this.$delete(this.datesEvents[date],ev)
                  }
                }
              }
              this.$emit("clicked", null, null, null, "refresh")
            }else if(res.status==1){
                this.$toasted.show(res.msg, 
                  {position: 'bottom-center', duration: 7500});
            }
            else if(res.status == 4) {
                this.$toasted.show(res.msg, {position: 'bottom-center', duration: 7500});
                this.$store.dispatch('logout'),
                this.$router.push("/login")
            }else{
              console.log("Error status: ", res.status);
              console.log("Message: ", res.msg);
              this.$toasted.show('Something went wrong while deleting your event. Please try again, if it still does not work, contact us through email.', 
                          {position: 'bottom-center', duration: 7500});
            }
        })
        .catch(e => {
          // Unable to get devices from server
          console.log(e)
          this.$toasted.show('Something went wrong while trying to delete your event. The server might be down at the moment. Please try again later.', 
              {position: 'bottom-center', duration: 7500});
          this.requestError = true;
        });
      },
      anyEvent() {
        return this.countAllEvents() ? true : false;
      },
      countAllEvents() {
        var count = 0;
        for(var date in this.searchedEvents) {
          count += this.searchedEvents[date].length;
        }
        return count;
      }
    },
    watch: {
      refresh:function(){
        this.buildEvents() 
      }
    },
}


/*
Example of data to pass to component

datesEvents: {
        'September': [
          {
            title: 'Five',
            slug: 'five',
            teaser: 'five',
            published_at: '30.09.2016.'
          },
          {
            title: 'Four',
            slug: 'four',
            teaser: 'four',
            published_at: '15.09.2016.'
          }
        ],
        'April': [
          {
            title: 'Three',
            slug: 'three',
            teaser: 'three',
            published_at: '14.04.2016.'
          },
          {
            title: 'Two and a half',
            slug: 'two-and-a-half',
            teaser: 'two and a half',
            published_at: '02.04.2016.'
          }
        ],
        'December': [
          {
            title: 'Two',
            slug: 'two',
            teaser: 'two',
            published_at: '25.12.2015.'
          },
          {
            title: 'One',
            slug: 'one',
            teaser: 'one',
            published_at: '01.12.2015.'
          }
        ]
      },
*/

</script>

<style scoped>
.mycontainer {
    margin: 0 auto;
    max-width: 80%;
    height: inherit;
}

.mycontainer .search-box {
    padding: 10px;
    margin: 20px 0;
    border: 1px solid black;
    border-radius: 5px;
}

.mycontainer .timeline {
    position: relative;
    border-left: 2px solid black;
}

.mycontainer .timeline .date {
    display: inline-block;
    font-size: 1.5rem;
    padding: 5px;
    position: relative;
    color:#616161;
    font-weight: bold;
    left: 15px;
    margin: 15px 0;
}

.mycontainer .timeline .date:before {
    content: '';
    position: absolute;
    top: 50%;
    left: -16px;
    border: 1px solid black;
    width: 14px;
}

.mycontainer .timeline .event {
    position: relative;
    max-width: 90%;
    left: 20px;
    box-shadow: 1px 5px 10px 1px rgba(0, 0, 0, 0.2);
    border-radius: 5px;
    padding: 10px;
    margin: 10px 0;
}

.mycontainer .timeline .event:hover {
    box-shadow: 0px 5px 10px 0px rgba(0, 0, 0, 0.4);
}

.mycontainer .timeline .event a {
    color: #006699;
    text-decoration: none;
}

.mycontainer .timeline .event .event-date {
    font-weight: 300;
    font-size: 14px;
}

.mycontainer .timeline .event .dot {
    display: block;
    position: absolute;
    width: 15px;
    height: 15px;
    border-radius: 50%;
    background: #006699;
    left: -27.5px;
    top: calc(50% - 5px);
}

.scroll-area {
    position: relative;
    margin: auto;
    width: 100%;
    height: 90%;
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
