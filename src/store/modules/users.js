/* eslint-disable no-undef */
import Vue from "vue";

const USERS = "USERS: Retrieving users.";
const USERS_REQUEST = "USERS: Request sent.";
const USERS_SUCCESS = "USERS: Successful request.";
const USERS_ERROR = "USERS: Failed request.";

const SET_USERS = "USERS: Set users.";

export { USERS };

export default {
  state: {
    loading: true,
    users: undefined
  },
  mutations: {
    [SET_USERS](state, data) {
      state.users = data;
    },
    [USERS_REQUEST](state) {
      state.loading = true;
    },
    [USERS_SUCCESS](state) {
      state.loading = false;
    },
    [USERS_ERROR](state) {
      state.loading = false;
    }
  },
  actions: {
    [USERS]({ commit }) {
      commit(USERS_REQUEST);
      return Vue.axios
        .get("admin/users")
        .then(resp => {
          commit(SET_USERS, resp.data);
          commit(USERS_SUCCESS);
        })
        .catch(({ status, errors }) => {
          commit(USERS_ERROR, errors);
          throw { status, errors };
        });
    }
  },
  getters: {
    users: state => {
      return state.users ? state.users : [];
    },
    hasUsers: (state, getters) => {
      return getters.users.length > 0;
    },
    loadingUsers: state => {
      return state.loading;
    }
  }
};
