/* eslint-disable no-undef */
import store from "../../store";
import { LOGIN, LOGOUT, RENEW } from "../../store/modules/auth";

const AuthHandler = {
  install(Vue) {
    /**
     * Check if a user is signed in.
     * @param methodOptions
     * @returns Object or null
     */
    Vue.prototype.$auth = {
      /**
       * Get the currently signed in user.
       * @returns {*} or null
       */
      currentUser() {
        return store.getters.currentUser;
      },

      isAuthenticated() {
        return store.getters.isAuthenticated;
      },

      accessLevel() {
        return store.getters.accessLevel;
      },

      /**
       * Sign in a user with a username and password, and a check to get a longer duration token.
       * @param username
       * @param password
       * @param remember
       * @returns {Promise}
       */
      signInWithUsernameAndPassword(username, password, remember) {
        return store.dispatch(LOGIN, { username, password, remember });
      },

      /**
       * Renew a user's session
       * @returns {Promise}
       */
      renew() {
        return store.dispatch(RENEW);
      },

      /**
       * Sign out the currently signed in user.
       * @returns {Promise}
       */
      signOut() {
        return store.dispatch(LOGOUT);
      }
    };
  }
};

export default AuthHandler;
