// import Vue from "vue";
import {
  ScenarioService
} from "@/common/api.service";
import {
  SCENARIO_UPDATE_PROP,
  SCENARIO_UPDATE,
  SCENARIO_FETCH,
} from "./actions.type";
import {
  SET_ACTIVE_SCENARIO,
  CLEAR_ACTIVE_SCENARIO,
  SET_ACTIVE_SCENARIO_PROP
} from "./mutations.type";

const initialState = {
  activeScenario: {},
};

export const state = { ...initialState };

export const actions = {
  [SCENARIO_UPDATE_PROP](context, payload) {
    context.commit(SET_ACTIVE_SCENARIO_PROP, payload);
    context.dispatch(SCENARIO_UPDATE);
  },
  [SCENARIO_UPDATE](context) {
    return ScenarioService.update(context.getters.activeScenario).then(data => {
      context.commit(SET_ACTIVE_SCENARIO, data)
    });
  },
  [SCENARIO_FETCH](context, payload) {
    return ScenarioService.get(payload).then(data => {
      context.commit(SET_ACTIVE_SCENARIO, data)
    })
  }
  // async [COMMENT_CREATE](context, payload) {
  //   await CommentsService.post(payload.slug, payload.comment);
  //   context.dispatch(FETCH_COMMENTS, payload.slug);
  // },
  // async [COMMENT_DESTROY](context, payload) {
  //   await CommentsService.destroy(payload.slug, payload.commentId);
  //   context.dispatch(FETCH_COMMENTS, payload.slug);
  // },
  // [ARTICLE_PUBLISH]({ state }) {
  //   return ArticlesService.create(state.article);
  // },
  // [ARTICLE_DELETE](context, slug) {
  //   return ArticlesService.destroy(slug);
  // },
  // [ARTICLE_EDIT]({ state }) {
  //   return ArticlesService.update(state.article.slug, state.article);
  // },
  // [ARTICLE_RESET_STATE]({ commit }) {
  //   commit(RESET_STATE);
  // }
};

/* eslint no-param-reassign: ["error", { "props": false }] */
export const mutations = {
  [SET_ACTIVE_SCENARIO](state, scenario) {
    state.activeScenario = scenario;
  },
  [CLEAR_ACTIVE_SCENARIO](state) {
    state.activeScenario = initialState.activeScenario;
  },
  [SET_ACTIVE_SCENARIO_PROP](state, {prop, value}) {
    state.activeScenario[prop] = value;
  },
  // [SET_COMMENTS](state, comments) {
  //   state.comments = comments;
  // },
  // [TAG_ADD](state, tag) {
  //   state.article.tagList = state.article.tagList.concat([tag]);
  // },
  // [TAG_REMOVE](state, tag) {
  //   state.article.tagList = state.article.tagList.filter(t => t !== tag);
  // },
  // [RESET_STATE]() {
  //   for (let f in state) {
  //     Vue.set(state, f, initialState[f]);
  //   }
  // }
};

const getters = {
  activeScenario(state) {
    return state.activeScenario;
  },
};

export default {
  state,
  actions,
  mutations,
  getters
};
