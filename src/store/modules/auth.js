/* eslint-disable no-undef */
import Vue from "vue";

let decode = require("jwt-decode");

const SET_TOKEN = "SET_TOKEN: Set token in store";

const LOGIN = "LOGIN";
const LOGIN_REQUEST = "LOGIN: Login request sent.";
const LOGIN_SUCCESS = "COURSES_FORM: Successful request.";
const LOGIN_ERROR = "COURSES_FORM: Failed request.";

const LOGOUT = "LOGOUT";
const LOGOUT_REQUEST = "LOGOUT: Logout request sent.";
const LOGOUT_SUCCESS = "LOGOUT: Successful request.";
const LOGOUT_ERROR = "LOGOUT: Failed request.";

const UNAUTHORIZED = "UNAUTHORIZED: Unauthorized.";

const RENEW = "RENEW: Renew auth token.";
const RENEW_REQUEST = "RENEW: Renew request sent.";
const RENEW_SUCCESS = "RENEW: Successful request.";
const RENEW_ERROR = "RENEW: Failed request.";

const USER_PROFILE = "USER_PROFILE: Get user profile data";
const PROFILE_REQUEST = "USER_PROFILE: Login request sent.";
const SET_PROFILE = "USER_PROFILE: Set profile data in store.";
const PROFILE_SUCCESS = "USER_PROFILE: Successful request.";
const PROFILE_ERROR = "USER_PROFILE: Failed request.";

const TEST = "TEST";
const TEST_REQUEST = "TEST: Renew request sent.";
const TEST_SUCCESS = "TEST: Successful request.";
const TEST_ERROR = "TEST: Failed request.";

export { LOGIN, LOGOUT, UNAUTHORIZED, RENEW, USER_PROFILE, TEST };

export default {
  state: {
    token: localStorage.getItem("token"),
    loading: false,
    errors: [],
    userId: undefined,
    profile: undefined
  },
  mutations: {
    [SET_TOKEN](state, result) {
      const token = result.token;
      const userId = result.id;
      state.token = token;
      state.userId = userId;
      if (token) {
        localStorage.setItem("token", token);
      } else {
        localStorage.removeItem("token");
      }
    },
    [SET_PROFILE](state, profile) {
      state.profile = profile;
    },

    [LOGIN_REQUEST](state) {
      state.loading = true;
      state.errors = [];
    },
    [LOGIN_SUCCESS](state) {
      state.loading = false;
    },
    [LOGIN_ERROR](state, errors) {
      state.loading = false;
      state.errors = errors;
    },

    [LOGOUT_REQUEST](state) {
      state.loading = true;
      state.errors = [];
    },
    [LOGOUT_SUCCESS](state) {
      state.loading = false;
    },
    [LOGOUT_ERROR](state, errors) {
      state.loading = false;
      state.errors = errors;
    },

    [RENEW_REQUEST](state) {
      state.loading = true;
      state.errors = [];
    },
    [RENEW_SUCCESS](state) {
      state.loading = false;
    },
    [RENEW_ERROR](state, errors) {
      state.loading = false;
      state.errors = errors;
    },

    [TEST_REQUEST](state) {
      state.loading = true;
      state.errors = [];
    },
    [TEST_SUCCESS](state) {
      state.loading = false;
    },
    [TEST_ERROR](state, errors) {
      state.loading = false;
      state.errors = errors;
    },

    [PROFILE_REQUEST](state) {
      state.loading = true;
      state.errors = [];
    },
    [PROFILE_SUCCESS](state) {
      state.loading = false;
    },
    [PROFILE_ERROR](state, errors) {
      state.loading = false;
      state.errors = errors;
    }
  },
  actions: {
    // Sign a user in
    [LOGIN]({ commit, dispatch }, { username, password, remember }) {
      commit(LOGIN_REQUEST);
      return Vue.axios
        .post("auth/login", {
          email: username,
          password: password,
          remember_me: remember
        })
        .then(resp => {
          commit(SET_TOKEN, resp.data);
          commit(LOGIN_SUCCESS);
          dispatch(USER_PROFILE);
        })
        .catch(({ status, errors }) => {
          // Failure
          commit(LOGIN_ERROR, errors);
          throw { status, errors };
        });
    },

    // Sign a user out
    [LOGOUT]: ({ commit }) => {
      commit(LOGOUT_REQUEST);

      return Vue.axios
        .post("auth/logout")
        .then(() => {
          commit(SET_TOKEN, { token: null, userId: undefined });
          commit(LOGOUT_SUCCESS);
        })
        .catch(({ status, errors }) => {
          commit(LOGOUT_ERROR, errors);
          throw { status, errors };
        });
    },

    [UNAUTHORIZED]: ({ commit }) => {
      commit(LOGOUT_REQUEST);
      commit(SET_TOKEN, { token: null, userId: undefined });
      commit(LOGOUT_SUCCESS);
    },

    // // Renew token
    // [RENEW]: ({ commit }) => {
    //   commit(RENEW_REQUEST);
    //
    //   return Vue.axios
    //     .post("auth/renew")
    //     .then(resp => {
    //       commit(SET_TOKEN, resp.data);
    //       commit(RENEW_SUCCESS);
    //     })
    //     .catch(({ status, errors }) => {
    //       commit(RENEW_ERROR, errors);
    //       throw { status, errors };
    //     });
    // },

    // Test token
    [TEST]: ({ commit }) => {
      commit(TEST_REQUEST);
      return Vue.axios
        .get("auth/test")
        .then(() => {
          commit(TEST_SUCCESS);
        })
        .catch(({ status, errors }) => {
          commit(TEST_ERROR, errors);
          throw { status, errors };
        });
    },

    // Get logged in user's profile
    [USER_PROFILE]: ({ commit, state }) => {
      commit(PROFILE_REQUEST);

      if (!state.userId) {
        state.userId = decode(state.token).id;
      }

      return Vue.axios
        .get(`/auth/user/${state.userId}`)
        .then(resp => {
          commit(SET_PROFILE, resp.data);
          commit(PROFILE_SUCCESS);
        })
        .catch(({ status, errors }) => {
          commit(PROFILE_ERROR, errors);
          throw { status, errors };
        });
    }
  },
  getters: {
    decodedToken: state => {
      return state.token != null ? decode(state.token) : null;
    },
    isTokenExpired: (state, getters) => {
      let decoded = getters.decodedToken;
      if (!decoded) return true;
      return decoded.exp * 1000 < new Date().getTime();
    },
    isAuthenticated: (state, getters) => {
      return state.token != null && !getters.isTokenExpired;
    },
    currentUser: (state, getters) => {
      let decoded = getters.decodedToken;
      return {
        firstName: decoded != null ? decoded.first_name : null,
        lastName: decoded != null ? decoded.last_name : null,
        id: decoded != null ? decoded.id : null,
        admin: state.profile ? state.profile.admin : false,
        organizer: state.profile ? state.profile.organizer : false
      };
    },
    profile: state => {
      return state.profile;
    }
  }
};
