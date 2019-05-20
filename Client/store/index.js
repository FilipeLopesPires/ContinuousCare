import Vuex from "vuex";
import Cookie from "js-cookie";

const createStore = () => {
    return new Vuex.Store({
        state: {            /* ========== state ========== */
            reloadControl: null,
            vue:null,
            
            sessionToken: null,
            userType: null,
            profile: {
                full_name: null,
                email: null,
                health_number: null,
                birth_date: null,
                weight: null,
                height: null,
                additional_info: null,
                company: null,
                specialities: null
            },
            loadedDevices: [],
            supportedDevices: [],
        },
        mutations: {        /* ========== mutations ========== */
            SOCKET_ONOPEN (state,event)  {
                console.log("entrou")
                event.currentTarget.send('{\"token\":\"'+state.sessionToken+'\"}')
            },
            SOCKET_ONCLOSE (state,event)  {
                console.log("fechado")
            },
            SOCKET_ONMESSAGE (state, message)  {
                var jsonData = JSON.parse(message.data.replace(/'/g,"\"").replace(/None/g,"null"));
                for(var permIndex in jsonData){
                    state.vue.$notify({
                        group: 'permissions',
                        title: 'New Permission',
                        text: 'User: '+jsonData[permIndex].name + ((jsonData[permIndex].health_number==null)?'':'<br/>Health Number: '+jsonData[permIndex].health_number) +'<br/>Duration(Hours): '+jsonData[permIndex].duration,
                        duration: 5000,
                        });
                }
            },
            setReloadControl(state, value) {
                state.reloadControl = value;
            },
            setVue(state, vue) {
                state.vue = vue;
            },
            setSessionToken(state, new_token) {
                if(new_token == "null") {
                    new_token = null;
                }
                state.sessionToken = new_token;
            },
            setUserType(state, new_user_type) {
                state.userType = new_user_type;
            },
            setProfileFullName(state, full_name) {
                state.profile.full_name = full_name;
            },
            setProfileEmail(state, email) {
                state.profile.email = email;
            },
            setProfileHealthNumber(state, health_number) {
                state.profile.health_number = health_number;
            },
            setProfileBirthdate(state, birth_date) {
                if(birth_date == "null" || birth_date == "") {
                    birth_date = null;
                }
                state.profile.birth_date = birth_date;
            },
            setProfileWeight(state, weight) {
                if(weight == "null" || weight == "") {
                    weight = null;
                }
                state.profile.weight = weight;
            },
            setProfileHeight(state, height) {
                if(height == "null" || height == "") {
                    height = null;
                }
                state.profile.height = height;
            },
            setProfileAdditionalInfo(state, additional_info) {
                if(additional_info == "null" || additional_info == "") {
                    additional_info = null;
                }
                state.profile.additional_info = additional_info;
            },
            setProfileCompany(state, company) {
                if(company == "null" || company == "") {
                    company = null;
                }
                state.profile.company = company;
            },
            setProfileSpecialities(state, specialities) {
                if(specialities == "null" || specialities == "") {
                    specialities = null;
                }
                state.profile.specialities = specialities;
            },
            setDevices(state, devices) {
                state.loadedDevices = devices;
            },
            setSupportedDevices(state, devices) {
                state.supportedDevices = devices
            },
            clearSession(state) {
                state.sessionToken = null;
                state.userType = null;
                state.profile = {
                    full_name: null,
                    email: null,
                    health_number: null,
                    birth_date: null,
                    weight: null,
                    height: null,
                    additional_info: null,
                    company: null,
                    specialities: null
                };
                state.loadedDevices = [];
                state.supportedDevices = [];
            }
        },
        actions: {          /* ========== actions ========== */
            setReloadControl(vuexContext) {
                vuexContext.commit("setReloadControl", true);
            },
            setVue(vuexContext, vue) {
                vuexContext.commit("setVue", vue);
            },
            setSessionToken(vuexContext, new_token) {
                vuexContext.commit("setSessionToken", new_token);
                if(process.client) {
                    localStorage.setItem("session_token", new_token);
                    localStorage.setItem("session_token_expiration", new Date().getTime() + 1000*60*60*24);
                }
                //Cookie.set("session_token", new_token);
                //Cookie.set("session_token_expiration", new Date().getTime() + 1000*60*60*24);
            },
            setUserType(vuexContext, new_user_type) {
                vuexContext.commit("setUserType", new_user_type);
                if(process.client) {
                    localStorage.setItem("session_user_type", new_user_type);
                }
                //Cookie.set("session_user_type", new_user_type);
            },
            setProfile(vuexContext, new_profile) {
                vuexContext.commit("setProfileFullName", new_profile.full_name);
                vuexContext.commit("setProfileEmail", new_profile.email);
                vuexContext.commit("setProfileHealthNumber", new_profile.health_number);
                vuexContext.commit("setProfileBirthdate", new_profile.birth_date);
                vuexContext.commit("setProfileWeight", new_profile.weight);
                vuexContext.commit("setProfileHeight", new_profile.height);
                vuexContext.commit("setProfileAdditionalInfo", new_profile.additional_info);
                vuexContext.commit("setProfileCompany", new_profile.company);
                vuexContext.commit("setProfileSpecialities", new_profile.specialities);
                if(process.client) {
                    localStorage.setItem("session_profile_full_name", new_profile.full_name);
                    localStorage.setItem("session_profile_email", new_profile.email);
                    localStorage.setItem("session_profile_health_number", new_profile.health_number);
                    localStorage.setItem("session_profile_birth_date", new_profile.birth_date);
                    localStorage.setItem("session_profilappe_weight", new_profile.weight);
                    localStorage.setItem("session_profile_height", new_profile.height);
                    localStorage.setItem("session_profile_additional_info", new_profile.additional_info);
                    localStorage.setItem("session_profile_company", new_profile.company);
                    localStorage.setItem("session_profile_specialities", new_profile.specialities);
                }
                /* Cookie.set("session_profile_full_name", new_profile.full_name);
                Cookie.set("session_profile_email", new_profile.email);
                Cookie.set("session_profile_health_number", new_profile.health_number);
                Cookie.set("session_profile_birth_date", new_profile.birth_date);
                Cookie.set("session_profile_weight", new_profile.weight);
                Cookie.set("session_profile_height", new_profile.height);
                Cookie.set("session_profile_additional_info", new_profile.additional_info);
                Cookie.set("session_profile_company", new_profile.company);
                Cookie.set("session_profile_specialities", new_profile.specialities); */
            },
            setDevices(vuexContext, devices) {
                vuexContext.commit("setDevices", devices); 
                if(process.client) {
                    localStorage.setItem("session_loaded_devices", devices);
                }
                //Cookie.set("session_loaded_devices", devices);
            },
            setSupportedDevices(vuexContext, devices) {
                vuexContext.commit("setSupportedDevices", devices); 
                if(process.client) {
                    localStorage.setItem("session_supported_devices", devices);
                }
                //Cookie.set("session_supported_devices", devices);
            },
            logout(vuexContext) {
                vuexContext.commit("clearSession");
                /* Cookie.remove("session_token");
                Cookie.remove("session_token_expiration");
                Cookie.remove("session_user_type");
                Cookie.remove("session_profile_full_name");
                Cookie.remove("session_profile_email");
                Cookie.remove("session_profile_health_number");
                Cookie.remove("session_profile_birth_date");
                Cookie.remove("session_profile_weight");
                Cookie.remove("session_profile_height");
                Cookie.remove("session_profile_additional_info");
                Cookie.remove("session_profile_company");
                Cookie.remove("session_profile_specialities");
                Cookie.remove("session_loaded_devices");
                Cookie.remove("session_supported_devices"); */
                if(process.client) {
                    localStorage.removeItem("session_token");
                    localStorage.removeItem("session_token_expiration");
                    localStorage.removeItem("session_user_type");
                    localStorage.removeItem("session_profile_full_name");
                    localStorage.removeItem("session_profile_email");
                    localStorage.removeItem("session_profile_health_number");
                    localStorage.removeItem("session_profile_birth_date");
                    localStorage.removeItem("session_profile_weight");
                    localStorage.removeItem("session_profile_height");
                    localStorage.removeItem("session_profile_additional_info");
                    localStorage.removeItem("session_profile_company");
                    localStorage.removeItem("session_profile_specialities");
                    localStorage.removeItem("session_loaded_devices");
                    localStorage.removeItem("session_supported_devices");
                }
            },
            initAuth(vuexContext, req) {
                let token;
                let expiration_date;
                let userType;
                let profile = {
                    full_name: null,
                    email: null,
                    health_number: null,
                    birth_date: null,
                    weight: null,
                    height: null,
                    additional_info: null,
                    company: null,
                    specialities: null
                };
                let loadedDevices;
                let supportedDevices;
                if(req) {
                    /* // only interesting in universal mode
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
                        */
                } else if(process.client) {
                    token = localStorage.getItem("session_token");
                    expiration_date = localStorage.getItem("session_token_expiration");
                    userType = localStorage.getItem("session_user_type");
                    profile.full_name = localStorage.getItem("session_profile_full_name");
                    profile.email = localStorage.getItem("session_profile_email");
                    profile.health_number = localStorage.getItem("session_profile_health_number");
                    profile.birth_date = localStorage.getItem("session_profile_birth_date");
                    profile.weight = localStorage.getItem("session_profile_weight");
                    profile.height = localStorage.getItem("session_profile_height");
                    profile.additional_info = localStorage.getItem("session_profile_additional_info");
                    profile.company = localStorage.getItem("session_profile_company");
                    profile.specialities = localStorage.getItem("session_profile_specialities");
                    loadedDevices = localStorage.getItem("session_loaded_devices");
                    supportedDevices = localStorage.getItem("session_supported_devices");
                } 
                if(new Date().getTime() > +expiration_date || !token) {
                    vuexContext.dispatch("logout");
                    return;
                }
                vuexContext.commit("setSessionToken", token);
                vuexContext.commit("setUserType", userType);
                vuexContext.commit("setProfileFullName", profile.full_name);
                vuexContext.commit("setProfileEmail", profile.email);
                vuexContext.commit("setProfileHealthNumber", profile.health_number);
                vuexContext.commit("setProfileBirthdate", profile.birth_date);
                vuexContext.commit("setProfileWeight", profile.weight);
                vuexContext.commit("setProfileHeight", profile.height);
                vuexContext.commit("setProfileAdditionalInfo", profile.additional_info);
                vuexContext.commit("setProfileCompany", profile.company);
                vuexContext.commit("setProfileSpecialities", profile.specialities);
                vuexContext.commit("setDevices", loadedDevices);
                vuexContext.commit("setSupportedDevices", supportedDevices);
            }
        },
        getters: {          /* ========== getters ========== */
            getReloadControl(state){
                return state.reloadControl;
            },
            getVue(state){
                return state.vue;
            },
            state(state) {
                return state;
            },

            isLoggedIn(state) {
                return state.sessionToken != null;
            },
            isClient(state) {
                if(state.userType == "client") {
                    return true;
                }
                return false;
            },
            isMedic(state) {
                if(state.userType == "medic") {
                    return true;
                }
                return false;
            },

            sessionToken(state) {
                return state.sessionToken;
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
            },
        },
    })
}

export default createStore 