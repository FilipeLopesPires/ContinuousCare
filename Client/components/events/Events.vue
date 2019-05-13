<template>
  <div class='mycontainer mt-25'>
    <input v-model='searchQuery' class='single-input mb-20' placeholder='Filter your events...'>
    <VuePerfectScrollbar class="scroll-area container" :settings="settings">
      <div class='timeline' v-if='anyEvent()'>
        <div v-for='(dateWithEvents, date) in searchedEvents' :key="dateWithEvents.id">
          <p v-if='dateWithEvents.length > 0' class='date'>{{ date }}</p>
          <div v-for='event in dateWithEvents' class='event' :key="event.id" @click="info(event.event)" style="cursor:pointer">
            <span class='dot'></span>
            <p class='event-date'>{{ event.time }}</p>
            <h3><a>{{ event.event }}</a></h3>
            <p style="white-space: pre-line">{{ event.metrics }}</p>
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
    data() {
      return {
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
      const config = {
        params: {'start': parseInt(new Date().setHours(0,0,0,0)/1000), 'end': parseInt(new Date().getTime()/1000)},
        headers: {'AuthToken': this.$store.getters.sessionToken}
      }
      await this.$axios.$get("/event", config)
            .then(res => {
              console.log(res)
              var events=res.data
              if("time" in events){
                var today = (new Date()).toLocaleDateString()
                var new_datesEvents = {}
                new_datesEvents[today]=[]
                for(var i=0; i<events["time"].length; i++){
                  var evt = ""
                  var metrics = ""
                  for(var key in events){
                    if(key!="time"){
                      if(events[key][i]){
                        evt+=key+","
                        var met = events[key][i].split(",")
                        console.log(met)
                        if(met.length>1){
                          metrics+=met[0]+": "+met[1]+"\n"
                        }else{
                          metrics+=events[key][i]+"\n"
                        }
                        
                      }
                    }
                  }
                  new_datesEvents[today].push({
                  "time":events["time"][i],
                  "event":evt.slice(0,-1),
                  "metrics":metrics,
                  })
                }
                this.datesEvents = new_datesEvents
                console.log(this.datesEvents)
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
    computed: {
      searchedEvents() {
        var searchRegex = new RegExp(this.searchQuery, 'i');
        var searchedObj = {};
  
        if(this.searchQuery == '') {
           return this.datesEvents;
        }
  
        for(var date in this.datesEvents) {
          searchedObj[date] = this.datesEvents[date].filter((event) => {
            return searchRegex.test(event.title) ||
                   searchRegex.test(event.teaser) ||
                   searchRegex.test(event.published_at) ||
                   searchRegex.test(date);
          });
        }
        return searchedObj;
      }
    },
    methods: {
      myUpdate(){
        this.$forceUpdate
      },
      info(title){
          console.log(title)
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
    }
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
  margin-bottom: 20px;
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
  max-width: 95%;
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
  height: 600px;
}
</style>
