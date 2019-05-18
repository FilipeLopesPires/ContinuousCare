<template>
    <div>
        <div class="row justify-content-center d-flex align-items-center col-lg-12 ">
            <div class="blog_right_sidebar">
                <TimeIntervalForm @time_interval_submit="time_interval_submit_handler" @time_interval_clear="time_interval_clear_handler"/>
            </div>
        </div>
        <div class="container justify-content-center align-items-center col-lg-9 col-md-9 mt-30" id="map-div">
            <div class="mb-60 leaflet-map" id="map-wrap" ref="worldmap"></div>
        </div>
    </div>
</template>

<script>
import L from 'leaflet';
import {antPath} from 'leaflet-ant-path';

import TimeIntervalForm from '@/components/forms/TimeIntervalForm.vue'

var vueComponent;

export default {
    components: {
        TimeIntervalForm,
    },
    data() {
        return {
            map: null,
            map_layers: null,
            map_markers: null,
            default_coords: [40.6303, -8.6575],
            filledform: {
                start: null,
                end: null,
                interval: null,
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
        this.map_layers = L.layerGroup();
        await this.onLoadMap(false);
        
    },
    methods: {
        
        /* ======================== HTTP REQUESTS ======================== */

        async getServerData(filledform, AuthToken, restPath) {
            var config;
            if(filledform.end == null && filledform.interval == null) {
                var params = {};
                var today = new Date();
                params['end'] = today.getTime() / 1000;
                today.setHours(0,0,0,0);
                params['start'] = today.getTime() / 1000;
                params['interval'] = null;
                config = {
                    params: params,
                    headers: {'AuthToken': AuthToken}
                }
            } else {
                config = {
                    params: {'start': new Date(filledform.start).getTime() / 1000, 'end': new Date(filledform.end).getTime() / 1000, 'interval': filledform.interval},
                    headers: {'AuthToken': AuthToken}
                }
            }
            console.log("getServerData");
            console.log(config);
            return await this.$axios.$get(restPath, config)
                                .then(res => {
                                    if(res.status != 0) {
                                        console.log(res);
                                        if(res.status == 1) {
                                            this.showToast(res.msg, 7500);
                                        } else if(res.status == 4) {
                                            this.$toasted.show(res.msg, {position: 'bottom-center', duration: 7500});
                                            this.$disconnect()
                                            this.$nextTick(() => { 
                                                this.$store.dispatch('logout'),
                                                this.$router.push("/login")
                                            });
                                        } else {
                                            this.showToast("Something went terribly wrong while trying to retrieve data from the server. Please try again later or contact us through email.", 7500);
                                        }
                                        return null;
                                    }
                                    return res;
                                })
                                .catch(e => {
                                    console.log(e);
                                    this.showToast("Something went wrong while trying to retrieve data from the server. It might be down at the moment. Please try again later.", 7500);
                                    return null;
                                });
        },
        async getDevices(AuthToken) {
            const config = {
                headers: {'AuthToken': AuthToken}
            }
            console.log("getDevices");
            return await this.$axios.$get("/devices",config)
                                .then(res => {
                                    if(res.status != 0) {
                                        console.log(res);
                                        if(res.status == 1) {
                                            this.showToast(res.msg, 7500);
                                        } else if(res.status == 4) {
                                            this.$toasted.show(res.msg, {position: 'bottom-center', duration: 7500});
                                            this.$disconnect()
                                            this.$nextTick(() => { 
                                                this.$store.dispatch('logout'),
                                                this.$router.push("/login")
                                            });
                                        } else {
                                            this.showToast("Something went terribly wrong while trying to retrieve devices locations. Please try again later or contact us through email.", 7500);
                                        }
                                        return null;
                                    }
                                    return res;
                                })
                                .catch(e => {
                                    // Unable to get devices from server
                                    this.showToast("Something went wrong while trying to retrieve devices locations. The server might be down at the moment. Please try again later.", 7500);
                                    console.log(e);
                                    return null;
                                });
        },

        /* ======================== MAP & PATH ======================== */

        async onLoadMap(reload) {
            var isMapCreated = false;
            if(reload) {
                this.map.removeLayer(this.map_layers);
                this.map_layers = L.layerGroup();
                this.map_layers.addTo(this.map);
                this.map.setView(this.default_coords, 13);
                isMapCreated = true;
            }
            var view = null;
            var path_result = await this.getServerData(this.filledform, this.$store.getters.sessionToken, "/path");
            console.log("path_result")
            console.log(path_result)
            if(path_result) {
                if(path_result.status==0) {
                    if(path_result.data.hasOwnProperty('latitude')) {
                        // prepare data
                        view = { coords:[path_result.data.latitude[path_result.data.latitude.length-1], path_result.data.longitude[path_result.data.longitude.length-1]], zoom:13 };
                        var userPath = [];
                        for(var i=0; i<path_result.data.latitude.length; i++) {
                            userPath.push([path_result.data.latitude[i], path_result.data.longitude[i]]);
                        }
                        // build MAP
                        /* 
                        // 3D world Map (not working)
                        // https://www.wrld3d.com/wrld.js/latest/docs/examples/adding-a-leaflet-marker-with-popup/
                        // { src: 'https://cdn-webgl.wrld3d.com/wrldjs/dist/latest/wrld.js'},
                        this.map = L.Wrld.map("map-wrap", "mapAccessToken", {
                            center: [37.7950, -122.401],
                            zoom: 15
                        }); */
                        if(reload) {
                            this.map.setView(view.coords, view.zoom);
                        } else {
                            this.map = L.map(this.$refs.worldmap).setView(view.coords, view.zoom);
                            L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
                                id: 'mapbox.streets',
                                accessToken: 'pk.eyJ1IjoiZmlsaXBlcGlyZXM5OCIsImEiOiJjanYzbmUzODUxNDVlNDNwOTB2M290eXo4In0.VgJ4YV1nGaxXglw-c8I5FA',
                                attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
                                maxZoom: 18,
                            }).addTo(this.map);
                            this.map_layers.addTo(this.map);
                            isMapCreated = true;
                        }
                        // User Path
                        this.createPath(userPath);
                    }
                }
            }
            if(isMapCreated && view != null) {
                // Fitbit Marker
                var options = {
                    riseOnHover: true,
                    icon: this.greenIcon,
                };
                var popup_content = "<div id='0'> <h5 class='mb--20'>Personal Device</h5> <p>Last position tracked.</p> </div>";
                var fitbit_marker = L.marker(view.coords, options).bindPopup(popup_content).addTo(this.map_layers);//.addTo(this.map);
                fitbit_marker.on('mouseover', function(e) { this.openPopup(); });
                fitbit_marker.on('mouseout', function(e) { this.closePopup(); });
                fitbit_marker.on('click', function(e) { vueComponent.clickEvent([e.latlng.lat, e.latlng.lng]) });
            }
            if(isMapCreated) {
                var events_result = await this.getServerData(this.filledform, this.$store.getters.sessionToken, "/event");
                console.log("events_result");
                console.log(events_result);
                if(events_result) {
                    if(events_result.status==0) {
                        if(events_result.data.hasOwnProperty('latitude')) {
                            this.insertMarkers(this.getMarkers(events_result.data));
                        }
                    }
                }
            }
            var foobot_result = await this.getDevices(this.$store.getters.sessionToken);
            console.log("foobot_result");
            console.log(foobot_result);
            if(foobot_result) {
                if(foobot_result.status==0) {
                    if(foobot_result.data.length != 0) { 
                        var foobots = [];
                        for(var i in foobot_result.data) {
                            if(foobot_result.data[i].type.includes("Foobot")) {
                                foobots.push(foobot_result.data[i]);
                            }
                        }
                        if(foobots.length > 0) {
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
                            if(!isMapCreated) {
                                console.log("shouldnt be here")
                                var view = { coords:[foobot_markers[0].coords[0],foobot_markers[0].coords[1]], zoom:13 };
                                
                                this.map = L.map(this.$refs.worldmap).setView(view.coords, view.zoom);
                                L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
                                    id: 'mapbox.streets',
                                    accessToken: 'pk.eyJ1IjoiZmlsaXBlcGlyZXM5OCIsImEiOiJjanYzbmUzODUxNDVlNDNwOTB2M290eXo4In0.VgJ4YV1nGaxXglw-c8I5FA',
                                    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
                                    maxZoom: 18,
                                }).addTo(this.map);
                                this.map_layers.addTo(this.map);
                                isMapCreated = true;
                            }
                            this.insertMarkers(foobot_markers);
                        }
                    }
                }
            }
            if(!isMapCreated) {
                var view = { coords:[40.6303, -8.6575], zoom:13 };
                this.map = L.map(this.$refs.worldmap).setView(view.coords, view.zoom);
                L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
                    id: 'mapbox.streets',
                    accessToken: 'pk.eyJ1IjoiZmlsaXBlcGlyZXM5OCIsImEiOiJjanYzbmUzODUxNDVlNDNwOTB2M290eXo4In0.VgJ4YV1nGaxXglw-c8I5FA',
                    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
                    maxZoom: 18,
                }).addTo(this.map);
                this.map_layers.addTo(this.map);
                
                isMapCreated = true;
                this.showToast("Warning: map was generated but information could not be retrieved. Either there is no data to sync or the server might be down at the moment.", 7500);
            }
        },
        createPath(path) {
            var options = {
                delay: 400, dashArray: [10,20], weight: 5,
                color: "#0000FF",  pulseColor: "#FFFFFF",
                paused: false, reverse: false, hardwareAccelerated: true
            };
            var userPath = antPath(path, options);
            userPath.addTo(this.map_layers);
            //this.map_layers.addLayer(userPath);
        },

        /* ======================== MARKERS ======================== */

        getMarkers(events) {
            var markers = [];
            var marker;
            console.log("events");
            console.log(events);
            for(var i=0; i<events.time.length; i++) {
                if(events.latitude[i]) {
                    var event_obj = JSON.parse(events["events"][i]);
                    var title = "";
                    var content = "";
                    if(event_obj) {
                        var severity = 0;
                        for(var j=0; j<event_obj["events"].length; j++) {
                            title += ", <br>" + event_obj["events"][j];
                            if(!content.includes(event_obj["metrics"][j])) {
                                if(event_obj["metrics"][j] != "PersonalStatus") {
                                    content += ", <br><font color='red'>" + event_obj["metrics"][j];
                                    content += ": " + event_obj["data"][event_obj["metrics"][j]] + "</font>";
                                } else {
                                    content += ", <br>" + event_obj["metrics"][j];
                                }
                            }
                            if(event_obj["metrics"][j] != "PersonalStatus") { severity = 1; }
                        }
                        marker = {
                            icon: (severity > 0) ? this.redIcon : this.blueIcon,
                            coords: [events.latitude[i], events.longitude[i]],
                            popup: {
                                id: i+1,
                                title: title.substring(6),
                                time: this.formatDateTime(events.time[i]),
                                content: content.substring(6),
                                // ...
                            }
                        };
                        markers.push(marker);
                    }
                }
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
                var marker = L.marker(markers[i].coords, options).bindPopup(popup_content).addTo(this.map_layers);//.addTo(this.map);
                marker.on('mouseover', function(e) { this.openPopup(); });
                marker.on('mouseout', function(e) { this.closePopup(); });
                marker.on('click', function(e) { vueComponent.clickEvent([e.latlng.lat, e.latlng.lng]) });
                //this.map_layers.addLayer(marker);
            }
            var center = this.map.getCenter()
            if(center.lat == this.default_coords[0] && center.lng == this.default_coords[1]) {
                this.map.setView(markers[0].coords, 13);
            }
        },
        clickEvent(coords) {
            console.log("Event Clicked! Coordenates: " + coords);
            // to do
        },

        /* ======================== AUX METHODS ======================== */

        time_interval_submit_handler(start, end, interval) {
            this.filledform.start = start;
            this.filledform.end = end;
            this.filledform.interval = interval;
            this.onLoadMap(true);
        },
        time_interval_clear_handler() {
            this.filledform.start = null;
            this.filledform.end = null;
            this.filledform.interval = null;
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
        showToast(message, duration) {
            this.$toasted.show(message, {position: 'bottom-center', duration: duration});
        }

    }
}
</script>

<style>
.leaflet-map {
    width: 100%;
    height: 500px;
    z-index: 0;
}
</style>
