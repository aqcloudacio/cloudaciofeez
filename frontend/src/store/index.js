import Vue from "vue";
import Vuex from "vuex";
// import createPersistedState from "vuex-persistedstate";

import scenario from "./scenario.module";
import user from "./user.module";
import platform from "./platform.module";
import investment from "./investment.module";
import advert from "./advert.module";


Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    scenario,
    user,
    platform,
    investment,
    advert,
  },
  // plugins: [createPersistedState({
  //   storage: window.sessionStorage,
  // })],
});
