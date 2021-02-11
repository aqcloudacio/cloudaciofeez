import {
  AdvertService
} from "@/common/api.service";
import {
  ADVERTS_ALL,
} from "./actions.type";
import {
  SET_ADVERTS,
} from "./mutations.type";

const initialState = {
  adverts: [],
};

export const state = { ...initialState };

export const actions = {
  [ADVERTS_ALL](context) {
    return AdvertService.list().then(data => {
      context.commit(SET_ADVERTS, data.results)
    })
  }
};

/* eslint no-param-reassign: ["error", { "props": false }] */
export const mutations = {
  [SET_ADVERTS](state, adverts) {
    state.adverts = adverts;
  },
};

const getters = {
  adverts(state) {
    return state.adverts;
  },
};

export default {
  state,
  actions,
  mutations,
  getters
};
