import Vuex from "vuex";
import Cookie from "js-cookie";
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
            },
            clearSessionToken(state) {
                state.sessionToken = null;
            }
        },
        actions: {
            setDevices(vuexContext, devices) {
                vuexContext.commit("setDevices", devices); 
            },
            setSessionToken(vuexContext, new_token) {
                vuexContext.commit("setSessionToken", new_token);
                //localStorage.setItem("session_token", new_token);
                //localStorage.setItem("session_token_expiration", new Date().getTime() + 1000*60*60*24);
                Cookie.set("session_token", new_token);
                Cookie.set("session_token_expiration", new Date().getTime() + 1000*60*60*24);
                vuexContext.dispatch("setSessionTimer", 1000*60*60*24);
            },
            setSessionTimer(vuexContext, duration) {
                setTimeout(() => {
                    vuexContext.commit('clearSessionToken');
                }, duration)
            },
            initAuth(vueContext, req) {
                if(req) {
                    if (!req.headers.cookie) {
                        return;
                    }
                    const cookie = req.headers.cookie
                        .split(";")
                        .find(c => c.trim().startsWith("session_token="));
                    if(!cookie) {
                        return;
                    }
                    const session_token = cookie.split("=")[1];
                    const session_token_expiration = req.headers.cookie
                        .split(";")
                        .find(c => c.trim().startsWith("session_token_expiration="))
                        .split("=")[1];
                } else {
                    //const token = localStorage.getItem("session_token");
                    //const expiration_date = localStorage.getItem("session_token_expiration");
                    return; //
                }
                if(new Date() > expiration_date || !token) {
                    return;
                }
                vuexContext.commit("setSessionToken", token);
            }
        },
        getters: {
            loadedDevices(state) {
                return state.loadedDevices
            },
            sessionToken(state) {
                return state.sessionToken;
            },
            isLoggedIn(state) {
                return state.sessionToken != null
            }
        },
        /* plugins: [createPersistedState()], */
    })
}

export default createStore 