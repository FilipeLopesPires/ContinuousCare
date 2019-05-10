<template>
    <div>
        <div class="container justify-content-center  align-items-center col-lg-9 col-md-9 ">
            <div class="mb-60 leaflet-map" id="map-wrap" ref="worldmap"></div>
        </div>
    </div>
</template>

<script>
import L from 'leaflet';
import {antPath} from 'leaflet-ant-path';

/* 
https://korigan.github.io/Vue2Leaflet/#/components/
https://github.com/schlunsen/nuxt-leaflet
https://github.com/KoRiGaN/Vue2Leaflet
https://leafletjs.com/examples/quick-start/

// http://jsfiddle.net/sowelie/3JbNY/

// https://www.wrld3d.com/wrld.js/latest/docs/examples/adding-a-leaflet-marker-with-popup/

*/

export default {
    data() {
        var map;
        var map_config = {
            id: 'mapbox.streets',
            accessToken: 'pk.eyJ1IjoiZmlsaXBlcGlyZXM5OCIsImEiOiJjanYzbmUzODUxNDVlNDNwOTB2M290eXo4In0.VgJ4YV1nGaxXglw-c8I5FA',
            attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
            zoom: 13,
            maxZoom: 18,
            coords: [38.7223, -9.1393],
        };
        var marker;
        var marker_config = {
            coords: [38.7223, -9.1393],
            options: {
                color: 'red',
            },
        };
        var popup;
        var popup_config = {
            message: "My Message Here",
        };
        var userPath;
        var userPath_config = {
            path: [[38.7323, -9.1493], [38.7223, -9.1493], [38.7223, -9.1393]],
            options: {
                delay: 400,
                dashArray: [10,20],
                weight: 5,
                color: "#0000FF",
                pulseColor: "#FFFFFF",
                paused: false,
                reverse: false,
                hardwareAccelerated: true
            },
        }

        return {
            map,
            map_config,
            marker,
            marker_config,
            popup,
            popup_config,
            userPath,
            userPath_config,
        }
    },
    mounted() {
        this.$nextTick(function () {
            // map
            this.map = L.map(this.$refs.worldmap).setView(this.map_config.coords, this.map_config.zoom);
            L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
                id: this.map_config.id,
                accessToken: this.map_config.accessToken,
                attribution: this.map_config.attribution,
                zoom: this.map_config.zoom,
                maxZoom: this.map_config.maxZoom
            }).addTo(this.map);
            // user path
            /* var polyline = L.polyline(this.userPath_config.path).addTo(this.map);   */
            this.userPath = antPath(this.userPath_config.path, this.userPath_config.options);
            this.map.addLayer(this.userPath);
            // marker 
            this.popup = L.popup().setContent("<div id='info'>" + this.popup_config.message + "</div>");
            this.marker = L.marker(this.marker_config.coords, this.marker_config.options).bindPopup(this.popup).addTo(this.map);
            this.marker.on('mouseover', function (e) { this.openPopup(); });
            this.marker.on('mouseout', function (e) { this.closePopup(); });
        });
    },
    methods: {

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
