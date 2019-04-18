import Vuex from "vuex";
import Cookie from "js-cookie";

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
                if(new_token == "null") {
                    state.sessionToken = null;
                    return;
                }
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
                if(process.client) {
                    localStorage.setItem("session_token", new_token);
                    localStorage.setItem("session_token_expiration", new Date().getTime() + 1000*60*60*24);
                }
                Cookie.set("session_token", new_token);
                Cookie.set("session_token_expiration", new Date().getTime() + 1000*60*60*24);
            },
            initAuth(vuexContext, req) {
                let token;
                let expiration_date;
                if(req) {
                    if (!req.headers.cookie) {
                        return;
                    }
                    var cookie = req.headers.cookie
                        .split(";")
                        .find(c => c.trim().startsWith("session_token="));
                    if(!cookie) {
                        return;
                    }
                    token = cookie.split("=")[1];
                    expiration_date = req.headers.cookie
                        .split(";")
                        .find(c => c.trim().startsWith("session_token_expiration="))
                        .split("=")[1];
                } else {
                    token = localStorage.getItem("session_token");
                    expiration_date = localStorage.getItem("session_token_expiration");
                }
                if(new Date().getTime() > +expiration_date || !token) {
                    vuexContext.dispatch("logout")
                    return;
                }
                vuexContext.commit("setSessionToken", token);
            },
            logout(vuexContext) {
                vuexContext.commit("clearSessionToken");
                Cookie.remove("session_token");
                Cookie.remove("session_token_expiration");
                if(process.client) {
                    localStorage.removeItem("session_token");
                    localStorage.removeItem("session_token_expiration");
                }
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
            },
        },
    })
}

export default createStore 