<template>
    <div>
        <div class="container justify-content-center  align-items-center col-lg-9 col-md-9 ">
            <div class="mb-60 leaflet-map" id="map-wrap" ref="worldmap"></div>
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
        var map;
        
        var marker;
        var marker_config = {
            coords: [38.7223, -9.1393],
            options: {
                riseOnHover: true,
            },
        };
        var popup;
        var popup_config = {
            message: "My Message Here",
        };

        return {
            map,
            marker,
            marker_config,
            popup,
            popup_config,
        }
    },
    mounted() {
        vueComponent = this;
        this.$nextTick(function () {
            // prepare data
            var view = {
                coords: [38.7223, -9.1393],
                zoom: 13,
            }
            var userPath = [[38.7423, -9.1593], [38.7323, -9.1493], [38.7223, -9.1493], [38.7223, -9.1393]];

            // build map
            this.createMap(view, 'pk.eyJ1IjoiZmlsaXBlcGlyZXM5OCIsImEiOiJjanYzbmUzODUxNDVlNDNwOTB2M290eXo4In0.VgJ4YV1nGaxXglw-c8I5FA');
            this.createPath(userPath);
            this.insertMarkers();
        });
    },
    methods: {
        createMap(view, mapAccessToken) {
            /* 
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
        // parameters will be different ...
        insertMarkers() {
            // process parameters 
            var tmp_markers = [
                {
                    coords: [38.7323, -9.1493],
                    options: {
                        riseOnHover: true,
                        // ...
                    },
                    popup: {
                        id: 1,
                        title: "First Event",
                        content: "All info in here.",
                        // ...
                    }
                },
                {
                    coords: [38.7223, -9.1393],
                    options: {
                        riseOnHover: true,
                        // ...
                    },
                    popup: {
                        id: 2,
                        title: "Second Event",
                        content: "All info in here.",
                        // ...
                    }
                }
            ];
            // create markers
            for(var i=0; i<tmp_markers.length; i++) {
                var m = tmp_markers[i];
                this.addMarker(m.coords, m.options, m.popup);
            }
        },
        // coords to place the marker, options for the marker options, popup for the event's content
        addMarker(coords, options, popup) {
            var popup_content = "<div id='" + popup.id + "'>" 
                                    + "<h5 class='mb--20'>" + popup.title + "</h5>"
                                    + "<p>" + popup.content + "</p>"
                                + "</div>";
            var marker = L.marker(coords, options).bindPopup(popup_content).addTo(this.map);
            marker.on('mouseover', function(e) { this.openPopup(); });
            marker.on('mouseout', function(e) { this.closePopup(); });
            marker.on('click', function(e) { vueComponent.clickEvent([e.latlng.lat, e.latlng.lng]) });  
        },
        clickEvent(coords) {
            console.log("Event Clicked! Coordenates: " + coords);
            // to do
        }
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
