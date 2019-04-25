import Vuex from "vuex";
import Cookie from "js-cookie";

const createStore = () => {
    return new Vuex.Store({
        state: {            /* ========== state ========== */
            sessionToken: null,
            userType: null,
            profile: {
                client_id: null,
                full_name: null,
                email: null,
                health_number: null,
                birth_date: null,
                weight: null,
                height: null
            },
            loadedDevices: [],
            supportedDevices: [],
        },
        mutations: {        /* ========== mutations ========== */
            setSessionToken(state, new_token) {
                if(new_token == "null") {
                    state.sessionToken = null;
                    return;
                }
                state.sessionToken = new_token;
            },
            setUserType(state, new_user_type) {
                state.userType = new_user_type;
            },
            setProfile(state, new_profile) {
                state.profile = new_profile;
            },
            setDevices(state, devices) {
                state.loadedDevices = devices
            },
            setSupportedDevices(state, devices) {
                state.supportedDevices = devices
            },
            clearSession(state) {
                state.sessionToken = null;
                state.userType = null;
                state.profile = {
                    client_id: null,
                    full_name: null,
                    email: null,
                    health_number: null,
                    birth_date: null,
                    weight: null,
                    height: null
                };
                state.loadedDevices = [];
                state.supportedDevices = [];
            }
        },
        actions: {          /* ========== actions ========== */
            setSessionToken(vuexContext, new_token) {
                vuexContext.commit("setSessionToken", new_token);
                if(process.client) {
                    localStorage.setItem("session_token", new_token);
                    localStorage.setItem("session_token_expiration", new Date().getTime() + 1000*60*60*24);
                }
                Cookie.set("session_token", new_token);
                Cookie.set("session_token_expiration", new Date().getTime() + 1000*60*60*24);
            },
            setUserType(vuexContext, new_user_type) {
                vuexContext.commit("setUserType", new_user_type);
                if(process.client) {
                    localStorage.setItem("session_user_type", new_user_type);
                }
                Cookie.set("session_user_type", new_user_type);
            },
            setProfile(vuexContext, new_profile) {
                vuexContext.commit("setProfile", new_profile);
                if(process.client) {
                    localStorage.setItem("session_profile", new_profile);
                }
                Cookie.set("session_profile", new_profile);
            },
            setDevices(vuexContext, devices) {
                vuexContext.commit("setDevices", devices); 
                if(process.client) {
                    localStorage.setItem("session_loaded_devices", devices);
                }
                Cookie.set("session_loaded_devices", devices);
            },
            setSupportedDevices(vuexContext, devices) {
                vuexContext.commit("setSupportedDevices", devices); 
                if(process.client) {
                    localStorage.setItem("session_supported_devices", devices);
                }
                Cookie.set("session_supported_devices", devices);
            },
            logout(vuexContext) {
                vuexContext.commit("clearSession");
                Cookie.remove("session_token");
                Cookie.remove("session_token_expiration");
                Cookie.remove("session_user_type");
                Cookie.remove("session_profile");
                Cookie.remove("session_loaded_devices");
                Cookie.remove("session_supported_devices");
                if(process.client) {
                    localStorage.removeItem("session_token");
                    localStorage.removeItem("session_token_expiration");
                    localStorage.removeItem("session_user_type");
                    localStorage.removeItem("session_profile");
                    localStorage.removeItem("session_loaded_devices");
                    localStorage.removeItem("session_supported_devices");
                }
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
                } else if(process.client) {
                    token = localStorage.getItem("session_token");
                    expiration_date = localStorage.getItem("session_token_expiration");
                } 
                if(new Date().getTime() > +expiration_date || !token) {
                    vuexContext.dispatch("logout");
                    return;
                }
                vuexContext.commit("setSessionToken", token);
            }
        },
        getters: {          /* ========== getters ========== */
            sessionToken(state) {
                return state.sessionToken;
            },
            isLoggedIn(state) {
                return state.sessionToken != null;
            },
            userType(state) {
                return state.userType;
            },
            profile(state) {
                return state.profile;
            },
            loadedDevices(state) {
                return state.loadedDevices;
            },
            supportedDevices(state) {
                return state.supportedDevices;
            }
        },
    })
}

export default createStore 