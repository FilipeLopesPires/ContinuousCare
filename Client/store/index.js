import Vuex from "vuex"

import createPersistedState from 'vuex-persistedstate'

const createStore = () => {
    return new Vuex.Store({
        state: {
            loadedDevices: [],
            sessionToken: null
        },
        mutations: {
            setDevices(state, devices) {
                state.loadedDevices = devices
            },
            setSessionToken(state, new_token) {
                state.sessionToken = new_token;
            }
        },
        actions: {
            setDevices(vuexContext, devices) {
                vuexContext.commit("setDevices", devices); 
            },
            setSessionToken(vuexContext, new_token) {
                vuexContext.commit("setSessionToken", new_token);
            }
        },
        getters: {
            loadedDevices(state) {
                return state.loadedDevices
            },
            sessionToken(state) {
                return state.sessionToken;
            }
        },
        plugins: [createPersistedState()],
    })
}

export default createStore 