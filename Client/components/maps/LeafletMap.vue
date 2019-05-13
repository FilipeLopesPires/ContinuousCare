<template>
    <div>
        <div class="row justify-content-center d-flex align-items-center col-lg-12 ">
            <div class="blog_right_sidebar">
                <form class="form-wrap" @submit.prevent="onLoadMap">
                    <div class="mt-10">
                        <date-picker class="single-input" v-model="filledform.start" name="start" :config="datetimepicker_options" placeholder="Start Time" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Start Time'"></date-picker>
                    </div>
                    <div class="mt-10">
                        <date-picker class="single-input" v-model="filledform.end" name="end" :config="datetimepicker_options" placeholder="End Time" onfocus="this.placeholder = ''" onblur="this.placeholder = 'End Time'"></date-picker>
                    </div>
                    <div class="mt-10">
                        <input class="single-input" v-model="filledform.interval" type="number" step=1 min=0 name="interval" placeholder="Time Interval" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Time Interval'" style="font-size:16px">
                    </div>
                    <div class="row justify-content-center d-flex align-items-center">
                        <div class="mt-10 col-lg-6"><p></p></div>
                        <div class="mt-10 col-lg-6">
                            <button class="genric-btn success medium text-uppercase" type="submit">Load Data</button>
                        </div>
                    </div>
                </form>
            </div>
        </div>
        <div class="container justify-content-center align-items-center col-lg-9 col-md-9 mt-30">
            <div class="mb-60  leaflet-map" id="map-wrap" ref="worldmap"></div>
        </div>
    </div>
</template>

<script>
import Vue from "vue"
import L from 'leaflet';
import {antPath} from 'leaflet-ant-path';

/* 
https://korigan.github.io/Vue2Leaflet/#/components/
https://github.com/schlunsen/nuxt-leaflet
https://github.com/KoRiGaN/Vue2Leaflet
https://leafletjs.com/examples/quick-start/

// http://jsfiddle.net/sowelie/3JbNY/



*/
var vueComponent;

export default {
    data() {
        return {
            map: null,
            filledform: {
                start: null,
                end: null,
                interval: null,
            },
            datetimepicker_options: {
                format: 'DD/MM/YYYY h:mm:ss',
                useCurrent: false,
                showClear: true,
                showClose: true,
            },
            blueIcon: L.icon({
                iconUrl: 'marker-icon-blue.png',
                iconAnchor:   [12.5, 41],
                iconSize:     [25, 41],
                shadowUrl: 'marker-shadow.png',
                shadowSize:   [41, 41],
                popupAnchor:  [0, -41],
                /* iconSize:     [38, 95], // size of the icon
                shadowSize:   [50, 64], // size of the shadow
                iconAnchor:   [22, 94], // point of the icon which will correspond to marker's location
                shadowAnchor: [4, 62],  // the same for the shadow
                popupAnchor:  [-3, -76] // point from which the popup should open relative to the iconAnchor */
            }),
            greenIcon: L.icon({
                iconUrl: 'marker-icon-green.png',
                iconAnchor:   [12.5, 41],
                iconSize:     [25, 41],
                shadowUrl: 'marker-shadow.png',
                shadowSize:   [41, 41],
                popupAnchor:  [0, -41],
            }),
            redIcon: L.icon({
                iconUrl: 'marker-icon-red.png',
                iconAnchor:   [12.5, 41],
                iconSize:     [25, 41],
                shadowUrl: 'marker-shadow.png',
                shadowSize:   [41, 41],
                popupAnchor:  [0, -41],
            }),
        }
    },
    async mounted() {
        vueComponent = this;
        var path_result = await this.getServerData(this.filledform, this.$store.getters.sessionToken, "/path");
        if(path_result) {
            if(path_result.status==0) {
                this.$nextTick(function () {
                    // prepare data
                    var view = { coords:[path_result.data.latitude[path_result.data.latitude.length-1], path_result.data.longitude[path_result.data.longitude.length-1]], zoom:13 };
                    var userPath = [];
                    for(var i=0; i<path_result.data.latitude.length; i++) {
                        userPath.push([path_result.data.latitude[i], path_result.data.longitude[i]]);
                    }
                    // build map
                    this.createMap(view, 'pk.eyJ1IjoiZmlsaXBlcGlyZXM5OCIsImEiOiJjanYzbmUzODUxNDVlNDNwOTB2M290eXo4In0.VgJ4YV1nGaxXglw-c8I5FA');
                    this.createPath(userPath);
                });
            }
        }
        var events_result = await this.getServerData(this.filledform, this.$store.getters.sessionToken, "/event");
        if(events_result) {
            if(events_result.status==0) {
                this.$nextTick(function () {
                    this.insertMarkers(this.getMarkers(events_result.data));
                });
            }
        }
        var foobot_result = await this.getDevices(this.$store.getters.sessionToken);
        if(foobot_result) {
            if(foobot_result.status==0) {
                this.$nextTick(function () {
                    if(foobot_result.data.length == 0) { return; }
                    var foobots = [];
                    for(var i in foobot_result.data) {
                        if(foobot_result.data[i].type.includes("Foobot")) {
                            foobots.push(foobot_result.data[i]);
                        }
                    }
                    var foobot_markers = [];
                    var marker;
                    for(var i in foobots) {
                        marker = {
                            icon: this.greenIcon,
                            coords: [foobots[i].latitude, foobots[i].longitude],
                            popup: {
                                id: 0,
                                title: "Foobot",
                                time: null,
                                content: "UUID: " + foobots[i].uuid,
                            }
                        }
                        foobot_markers.push(marker);
                    }
                    this.insertMarkers(foobot_markers);
                });
            }
        }
    },
    methods: {
        
        /* ======================== HTTP REQUESTS ======================== */

        async getServerData(filledform, AuthToken, restPath) {
            var config;
            if(filledform.end == null && filledform.interval == null) {
                var params = {};
                var today = new Date();
                params['end'] = today.getTime();
                today.setHours(0,0,0,0);
                params['start'] = today.getTime();
                params['interval'] = null;
                config = {
                    params: params,
                    headers: {'AuthToken': AuthToken}
                }
            } else {
                config = {
                    params: {'start': new Date(filledform.start).getTime(), 'end': new Date(filledform.end).getTime(), 'interval': filledform.interval},
                    headers: {'AuthToken': AuthToken}
                }
            }
            return await this.$axios.$get(restPath, config)
                                .then(res => {
                                    if(res.status != 0) {
                                        console.log(res);
                                        // toast
                                        return null;
                                    }
                                    return res;
                                })
                                .catch(e => {
                                    console.log(e);
                                    // toast
                                    return null;
                                });
        },
        async getDevices(AuthToken) {
            const config = {
                headers: {'AuthToken': AuthToken}
            }
            return await this.$axios.$get("/devices",config)
                                .then(res => {
                                    if(res.status != 0) {
                                        console.log(res)
                                        this.$toasted.show('Something went wrong while trying to retrieve devices locations. The server might be down at the moment. Please try again later.', 
                                            {position: 'bottom-center', duration: 7500});
                                        return null;
                                    }
                                    return res;
                                })
                                .catch(e => {
                                    // Unable to get devices from server
                                    this.$toasted.show('Something went wrong while trying to retrieve devices locations. The server might be down at the moment. Please try again later.', 
                                        {position: 'bottom-center', duration: 7500});
                                    console.log(e);
                                    return null;
                                });
        },

        /* ======================== MAP & PATH ======================== */

        async onLoadMap() {
            // to do
            console.log(this.filledform);
        },
        createMap(view, mapAccessToken) {
            /* 
            // 3D world Map (not working)
            // https://www.wrld3d.com/wrld.js/latest/docs/examples/adding-a-leaflet-marker-with-popup/
            // { src: 'https://cdn-webgl.wrld3d.com/wrldjs/dist/latest/wrld.js'},
            this.map = L.Wrld.map("map-wrap", "mapAccessToken", {
                center: [37.7950, -122.401],
                zoom: 15
            }); */
            this.map = L.map(this.$refs.worldmap).setView(view.coords, view.zoom);
            L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
                id: 'mapbox.streets',
                accessToken: mapAccessToken,
                attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
                maxZoom: 18,
            }).addTo(this.map);
        },
        createPath(path) {
            var options = {
                delay: 400, dashArray: [10,20], weight: 5,
                color: "#0000FF",  pulseColor: "#FFFFFF",
                paused: false, reverse: false, hardwareAccelerated: true
            };
            var userPath = antPath(path, options);
            userPath.addTo(this.map);
            //this.map.addLayer(userPath); // it does the same as the previous line
            //var polyline = L.polyline(path).addTo(this.map); // path version before antPath
        },

        /* ======================== MARKERS ======================== */

        defineMarkerIcon() {
            // to do...
            return this.blueIcon;
        },
        getMarkers(events) {
            var markers = [];
            var marker;
            for(var i=0; i<events.time.length; i++) {
                var title = "";
                var content = "";
                for(var key in events) {
                    if(key != "time" && key != "latitude" && key != "longitude") {
                        if(events[key][i] != null) {
                            title += ", <br>" + key;
                            if(!content.includes(events[key][i])) {
                                content += ", <br>" + events[key][i];
                            }
                        }
                    }
                }
                marker = {
                    icon: this.defineMarkerIcon(),
                    coords: [events.latitude[i], events.longitude[i]],
                    popup: {
                        id: i+1,
                        title: title.substring(2),
                        time: events.time[i],
                        content: content.substring(2),
                        // ...
                    }
                };
                markers.push(marker);
            }
            return markers;
        },
        insertMarkers(markers) {
            if(markers == null || markers.length == 0) {
                return;
            }
            var options = {
                riseOnHover: true,
                // ...
            };
            for(var i=0; i<markers.length; i++) {
                options["icon"] = markers[i].icon;
                var popup_content = "<div id='" + markers[i].popup.id + "'>" 
                                        + "<h5 class='mb--20'>" + markers[i].popup.title + "</h5>";
                if(markers[i].popup.time) {
                    popup_content       += "<p>" + markers[i].popup.time + "</p>";
                }
                    popup_content       += "<p>" + markers[i].popup.content + "</p>"
                                    + "</div>";
                var marker = L.marker(markers[i].coords, options).bindPopup(popup_content).addTo(this.map);
                marker.on('mouseover', function(e) { this.openPopup(); });
                marker.on('mouseout', function(e) { this.closePopup(); });
                marker.on('click', function(e) { vueComponent.clickEvent([e.latlng.lat, e.latlng.lng]) });  
            }
        },
        clickEvent(coords) {
            console.log("Event Clicked! Coordenates: " + coords);
            // to do
        }

        /* ======================== AUX METHODS ======================== */














    },
    name: "LeafletMap"
}
</script>

<style>
.leaflet-map {
    width: 100%;
    height: 500px;
    z-index: 0;
}
</style>
