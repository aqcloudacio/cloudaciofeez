// import Vue from "vue";
import jwt_decode from "jwt-decode";
import router from '../router/index.js'

import {
  UserService
} from "@/common/api.service";
import {
  USER_FETCH,
  USER_UPDATE,
  PRACTICE_INVITE_ACCEPT,
  USER_LOGIN,
  USER_LOGOUT,
  USER_REGISTER,
  USER_REGISTER_DETAILS,
  USER_RESET_PASSWORD,
  USER_CHANGE_PASSWORD,
  USER_VERIFY,
  USER_RESEND_VERIFICATION_TOKEN,
  USER_CHECK_CREDENTIALS,
  REFRESH_ACCESS_TOKEN,
  AUTO_REFRESH_TIMER,
  UPDATE_LOCAL_STORAGE,
} from "./actions.type";
import {
  SET_ACTIVE_USER,
  REMOVE_ACTIVE_USER_FROM_PRACTICE,
  ADD_ACTIVE_USER_TO_PRACTICE,
  SET_ACTIVE_USER_PROP,
  UPDATE_ACCESS_TOKEN,
  DESTROY_TOKENS,
  CLEAR_ACTIVE_USER,
} from "./mutations.type";

const initialState = {
  activeUser: {},
  accessToken: localStorage.getItem('access_token') || null,
  refreshToken: localStorage.getItem('refresh_token') || null,
};

export const state = { ...initialState };

export const actions = {
  [USER_FETCH](context) {
    if (context.getters.refreshTokenIsValid) {
      return UserService.get().then(data => {
        context.commit(SET_ACTIVE_USER, data.results[0])
      }).catch(err => {
        console.log(err);
      });
    } else {
      context.dispatch(USER_LOGOUT);
    }
  },
  [PRACTICE_INVITE_ACCEPT](context, notification) {
    context.commit(ADD_ACTIVE_USER_TO_PRACTICE, {
      'type': 'practice',
      'practice': notification.practice
    });
    context.commit(REMOVE_ACTIVE_USER_FROM_PRACTICE, {
      'type': 'pending',
      'practice': notification.practice
    });
    if (notification.active_practice) {
      context.commit(SET_ACTIVE_USER_PROP, {
        'prop': 'active_practice',
        'value': notification.practice
      });
    };
    context.dispatch(USER_UPDATE);
  },
  [USER_UPDATE](context) {
    return UserService.update(context.getters.activeUser).then(data => {
      context.commit(SET_ACTIVE_USER, data)
    });
  },
  [USER_REGISTER](context, payload){
    return UserService.register(payload)
  },
  [USER_REGISTER_DETAILS](context, payload) {
    return UserService.registerDetails(payload)
  },
  [USER_VERIFY](context, payload){
    return UserService.verify(payload)
  },
  [USER_RESEND_VERIFICATION_TOKEN](context, user){
    return UserService.resendVerificationToken(user).then(data => {
      console.log(data);
    })
  },
  [USER_RESET_PASSWORD](context, payload){
    return UserService.resetPassword(payload).then(data => {
      console.log(data);
    })
  },
  [USER_CHANGE_PASSWORD](context, payload){
    return UserService.changePassword(payload).then(data => {
      console.log(data);
    })
  },
  [USER_LOGIN](context, credentials){
    return UserService.login(credentials).then(data => {
      // Stores the access and refresh tokens in localstorage
      context.dispatch(UPDATE_LOCAL_STORAGE, {
        access: data.access,
        refresh: data.refresh
      }).then(() => {
        context.dispatch(USER_FETCH);
        context.dispatch(AUTO_REFRESH_TIMER, data.access);
      }).catch(error => {
        return Promise.reject(error);
      })
    }).catch(error => {
      return Promise.reject(error);
    })
  },
  [USER_CHECK_CREDENTIALS](context, credentials) {
    return UserService.login(credentials).then(data => {
      console.log(data);
    }).catch((err) => {
      return Promise.reject(err);
    })
  },
  [UPDATE_LOCAL_STORAGE](context, {access, refresh}) {
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
    context.state.accessToken = access;
    context.state.refreshToken = refresh;
  },
  [USER_LOGOUT](context) {
    // NOTE: This function should also optimally blacklist tokens that
    // have been logged out. Havne't implemented this logic yet, don't know if
    // I will.
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    context.commit(CLEAR_ACTIVE_USER);
    context.commit(DESTROY_TOKENS);

    if (router.currentRoute.name != 'login') {
      router.push({ name: 'login' });
    }
  },
  [REFRESH_ACCESS_TOKEN](context){
    // send the stored refresh token to the API
    if (context.getters.refreshTokenIsValid) {
      return UserService.refreshToken({
        'refresh': context.getters.refreshToken
      }).then(data => {
        // if API sends back new access token, update the store
        context.commit(UPDATE_ACCESS_TOKEN, data.access);
        context.dispatch(AUTO_REFRESH_TIMER, data.access);
        return data.access
      }).catch(() => {
        console.log(`Error refreshing access token - logging out`);
        context.dispatch(USER_LOGOUT);
      })
    } else {
      context.dispatch(USER_LOGOUT);
    }
  },
  [AUTO_REFRESH_TIMER](context, accesstoken){
    // get current datetime
    let currentDatetime = new Date();
    // If refresh token is not expired, get a new access token.
    let decodedAccessToken = jwt_decode(accesstoken);
    // get expiry of newly issued JWT
    let accessTokenExpiry = new Date(decodedAccessToken.exp * 1000);
    // get delta less 60 ms
    let timeToExpire = ((accessTokenExpiry-currentDatetime)-60000)

    // Set a timer to fire 60 seconds before token expiry
    let tokenTimer = setTimeout(() => {
      //call funct to refresh token
      context.dispatch(REFRESH_ACCESS_TOKEN).then(()=> {
        clearTimeout(tokenTimer);
      })
      //clear timer
    }, timeToExpire);
  }
};

/* eslint no-param-reassign: ["error", { "props": false }] */
export const mutations = {
  [SET_ACTIVE_USER](state, user) {
    state.activeUser = user;
  },
  [CLEAR_ACTIVE_USER](state) {
    state.activeUser = initialState.activeUser;
  },
  [REMOVE_ACTIVE_USER_FROM_PRACTICE](state, {type, practice}){
    if (type === 'pending') {
      const result = state.activeUser.pending_practices.filter(i => i != practice);
      state.activeUser.pending_practices = result;
    }
  },
  [ADD_ACTIVE_USER_TO_PRACTICE](state, {type, practice}){
    if (type === 'practice') {
      state.activeUser.practices.push(practice)
    }
  },
  [SET_ACTIVE_USER_PROP](state, {prop, value}) {
    if (prop.includes('.')) {
        let splitprop = prop.split('.');
        let obj = splitprop[0];
        let attr = splitprop[1];
        if (!state.activeUser[obj]) {
            state.activeUser[obj] = new Object();
        }
        state.activeUser[obj][attr] = value;
    } else {
    state.activeUser[prop] = value;
    }
  },
  [UPDATE_ACCESS_TOKEN] (state, access) {
    state.accessToken = access;
    localStorage.setItem('access_token', access);
  },
  [DESTROY_TOKENS] (state) {
    state.accessToken = null;
    state.refreshToken = null;
  },
};

const getters = {
  activeUser(state) {
    return state.activeUser;
  },
  accessToken (state) {
    return state.accessToken;
  },
  refreshToken (state) {
    return state.refreshToken;
  },
  loggedIn (state) {
    return state.accessToken != null;
  },
  refreshTokenIsValid (state) {
    if (state.refreshToken) {
      let currentDatetime = new Date();
      //get expiry of refresh token
      let decodedRefreshToken = jwt_decode(state.refreshToken);
      //get expiry of refresh token
      let refreshTokenExpiry = new Date(decodedRefreshToken.exp * 1000);
      return refreshTokenExpiry > currentDatetime
    } else {
      return false
    }
  },
  accessTokenIsValid (state) {
    if (state.accessToken) {
      let currentDatetime = new Date();
      let decodedToken = jwt_decode(state.accessToken);
      //get expiry of refresh token
      let tokenExpiry = new Date(decodedToken.exp * 1000);
      return tokenExpiry > currentDatetime
    } else {
      return false
    }
  }
};

export default {
  state,
  actions,
  mutations,
  getters
};
