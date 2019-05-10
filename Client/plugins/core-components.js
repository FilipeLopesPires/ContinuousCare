import Vue from 'vue'

import Vuex from 'vuex'
Vue.use(Vuex)

import HeaderMenu from '@/components/headers/HeaderMenu.vue'
import PageBanner from '@/components/banners/PageBanner.vue'
import PageFooter from '@/components/footers/PageFooter.vue'
Vue.component('HeaderMenu', HeaderMenu)
Vue.component('PageBanner', PageBanner)
Vue.component('PageFooter', PageFooter)

import Toasted from 'vue-toasted'
Vue.use(Toasted)

import Notifications from 'vue-notification'
Vue.use(Notifications)

import VueNativeSock from 'vue-native-websocket'
Vue.use(VueNativeSock, 'ws://mednat.ieeta.pt:8344', {connectManually:true, format: 'json'})
