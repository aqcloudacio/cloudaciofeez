// import Vue from "vue";
import {
  InvestmentNameService
} from "@/common/api.service";
import {
  INVESTMENTNAME_ALL,
} from "./actions.type";
import {
  SET_INVESTMENTNAMES,
} from "./mutations.type";

const initialState = {
  investmentNames: [],
};

export const state = { ...initialState };

export const actions = {
  [INVESTMENTNAME_ALL](context) {
    return InvestmentNameService.list().then(data => {
      context.commit(SET_INVESTMENTNAMES, data.results)
    })
  }
};

/* eslint no-param-reassign: ["error", { "props": false }] */
export const mutations = {
  [SET_INVESTMENTNAMES](state, investmentNames) {
    state.investmentNames = investmentNames;
  },
};

const getters = {
  investmentNames(state) {
    return state.investmentNames;
  },
};

export default {
  state,
  actions,
  mutations,
  getters
};
