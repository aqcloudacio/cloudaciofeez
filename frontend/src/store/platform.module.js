// import Vue from "vue";
import {
  PlatformService,
  PlatformAAService,
  PlatformNameService,
} from "@/common/api.service";
import {
  PLATFORM_UPDATE_PROP,
  PLATFORM_UPDATE,
  PLATFORM_FETCH,
  PLATFORM_AA_FETCH,
  PLATFORMNAME_ALL,
} from "./actions.type";
import {
  SET_ACTIVE_PLATFORM,
  CLEAR_ACTIVE_PLATFORM,
  SET_ACTIVE_PLATFORM_PROP,
  SET_ACTIVE_PLATFORM_AA,
  CLEAR_ACTIVE_PLATFORM_AA,
  SET_PLATFORMNAMES,
} from "./mutations.type";

const initialState = {
  activePlatform: {},
  activePlatformAA: [],
  platformNames: [],
};

export const state = { ...initialState };

export const actions = {
  [PLATFORM_UPDATE_PROP](context, payload) {
    context.commit(SET_ACTIVE_PLATFORM_PROP, payload);
    context.dispatch(PLATFORM_UPDATE);
  },
  [PLATFORM_UPDATE]({state, commit, rootState}) {
    return PlatformService.update(state, rootState).then(data => {
      commit(SET_ACTIVE_PLATFORM, data)
    });
  },
  [PLATFORM_FETCH](context, payload) {
    return PlatformService.get(payload).then(data => {
      context.commit(SET_ACTIVE_PLATFORM, data)
    })
  },
  [PLATFORM_AA_FETCH](context, payload) {
    return PlatformAAService.list(payload).then(data => {
      context.commit(SET_ACTIVE_PLATFORM_AA, data.results)
    })
  },
  [PLATFORMNAME_ALL](context, next) {
    let endpoint = null;
    if (next) {
      endpoint = next
    }
    return PlatformNameService.list(endpoint).then(data => {
      context.commit(SET_PLATFORMNAMES, data.results)
      if (data.next) {
        context.dispatch(PLATFORMNAME_ALL, data.next);
      }
    })
  }
};

/* eslint no-param-reassign: ["error", { "props": false }] */
export const mutations = {
  [SET_ACTIVE_PLATFORM](state, platform) {
    state.activePlatform = platform;
  },
  [CLEAR_ACTIVE_PLATFORM](state) {
    state.activePlatform = initialState.activePlatform;
  },
  [SET_ACTIVE_PLATFORM_PROP](state, {prop, value}) {
    state.activePlatform[prop] = value;
  },
  [SET_ACTIVE_PLATFORM_AA](state, platformAA) {
    state.activePlatformAA = platformAA;
  },
  [CLEAR_ACTIVE_PLATFORM_AA](state) {
    state.activePlatformAA = initialState.activePlatformAA;
  },
  [SET_PLATFORMNAMES](state, platformNames) {
    state.platformNames.push(...platformNames);
  },
};

const getters = {
  activePlatform(state) {
    return state.activePlatform;
  },
  activePlatformAA(state) {
    return state.activePlatformAA;
  },
  platformNames(state) {
    return state.platformNames;
  }
};

export default {
  state,
  actions,
  mutations,
  getters
};
