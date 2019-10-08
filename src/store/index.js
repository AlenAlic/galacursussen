import Vue from "vue";
import Vuex from "vuex";

import auth from "./modules/auth";
import courses from "./modules/courses";
import users from "./modules/users";

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    auth: auth,
    courses: courses,
    users: users
  }
});
