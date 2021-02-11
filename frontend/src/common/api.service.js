import { CSRF_TOKEN } from "./csrf_token.js";
import axios from 'axios';
import jwt_decode from "jwt-decode";

import user from "../store/user.module";
import store from "../store/index";
import {
  REFRESH_ACCESS_TOKEN,
} from "../store/actions.type";

function apiService(endpoint, method, data) {

  var headers = {
    'Accept': 'application/json',
    "content-type": "application/json",
    "X-CSRFTOKEN": CSRF_TOKEN,
  }

  // Adds header if the access token exists. This is so registrations don't
  // automatically bounce.
  if (user.state.accessToken) {
    headers.Authorization = `Bearer ${user.state.accessToken}`
  }

  const options = {
    url: endpoint,
    method: method || "GET",
    data: data,
    headers: headers
  };

  return axios(options)
  .then(response => {
    return response;
   }).catch(err => {
     console.log('Logging error:');
     console.log(err.response);
     return Promise.reject(err.response);
   })
}

var refreshTokenPromise = null// this holds any in-progress token refresh requests

axios.interceptors.response.use(
  response => {
    return response.data;
  },
  async error => {
    if (error.config && error.response && error.response.status === 401) {
      if (store.getters.accessToken && store.getters.refreshToken) {
        // Have to do the token expiry check here because for some reason the
        // vuex getter does not refresh when called from this script.
        let currentDatetime = new Date();
        let decodedRefreshToken = jwt_decode(store.getters.refreshToken);
        let decodedAccessToken = jwt_decode(store.getters.accessToken);
        let refreshTokenExpiry = new Date(decodedRefreshToken.exp * 1000);
        let accessTokenExpiry = new Date(decodedAccessToken.exp * 1000);

        // only want to attempt a refresh if they have a valid refresh token,
        // and the access token is actually expired.
        if (refreshTokenExpiry > currentDatetime && accessTokenExpiry < currentDatetime ) {
          if (!refreshTokenPromise) {
          // check for an existing in-progress request
          // if nothing is in-progress, start a new refresh token request
            refreshTokenPromise = store.dispatch(REFRESH_ACCESS_TOKEN).then((token) => {
              refreshTokenPromise = null; // clear state
              // console.log("401 caught, new token retrieved.");
              return token // resolve with the new token
            })
          }
          // once the refresh promise has completed, this async will be called
          // for all queued requests their headers changed to new token.
          return await refreshTokenPromise.then(token => {
            error.config.headers['Authorization'] = `Bearer ${token}`
            return axios(error.config)
          })
        } else {
          return Promise.reject(error);
        }
      } else {
        return Promise.reject(error);
      }
    } else {
      return Promise.reject(error);
    }
  });

export { apiService };

export const ScenarioService = {
  // list() {
  //   return apiService(`/api/scenarios/`, "GET");
  // },
  get(scenarioId) {
    return apiService(`/api/scenarios/${scenarioId}/`, "GET");
  },
  create(scenario) {
    return apiService(`/api/scenarios/`, "POST", scenario);
  },
  update(scenario) {
    return apiService(`/api/scenarios/${scenario.id}/`, "PATCH", scenario);
  },
  // destroy(scenarioId) {
  //   return apiService(`/api/scenarios/${scenarioId}/`, "DELETE");
  // }
};

export const AdvertService = {
  list() {
    return apiService(`/api/currentadvert/`, "GET");
  },
};

export const InvestmentNameService = {
  list() {
    return apiService(`/api/unlinkedinvestmentname/`, "GET");
  },
};

export const PlatformService = {
  get({scenarioId, platformId}) {
    return apiService(`/api/scenarios/${scenarioId}/platforms/${platformId}/`, "GET");
  },
  update(state, rootState) {
    return apiService(`/api/scenarios/${rootState.scenario.activeScenario.id}/platforms/${state.activePlatform.id}/`, "PATCH", state.activePlatform);
  },
};
export const PlatformAAService = {
  list({scenarioId, platformId}) {
    return apiService(`/api/scenarios/${scenarioId}/platforms/${platformId}/aasummary/`, "GET");
  },
};

export const PlatformNameService = {
  list(endpoint) {
    if (endpoint) {
      return apiService(endpoint, "GET");
    } else {
      return apiService(`/api/platformnames/`, "GET");
    }
  },
};

export const UserService = {
  get() {
    return apiService(`/api/user/`, "GET");
  },
  update(user) {
    return apiService(`/api/user/${user.id}/`, "PATCH", user);
  },
  login(credentials) {
    return apiService(`/api/token/`, "POST", credentials);
  },
  register(user) {
    return apiService(`/api/rego/`, "POST", user);
  },
  registerDetails(user) {
    return apiService(`/api/regodetails/${user.id}/`, "PATCH", user);
  },
  resetPassword(user) {
    // Custom update() method in serializer just sends a token.
    return apiService(`/api/resetpassword/${user.email}/`, "PATCH", user);
  },
  changePassword(payload) {
    return apiService(`/api/changepassword/${payload.id}/`, "PATCH", payload);
  },
  verify(payload) {
    // Note - this API is write-only
    return apiService(`/api/verify/${payload.id}/`, "PATCH", payload);
  },
  resendVerificationToken(user) {
    return apiService(`/api/rego/${user.id}/`, "PATCH", user);
  },
  refreshToken(refreshToken) {
    return apiService(`/api/token/refresh/`, "POST", refreshToken);
  },
};
