/* eslint-disable no-undef */
import Vue from "vue";

const COURSES_FORM = "COURSES_FORM: Get form data.";
const COURSES_FORM_REQUEST = "COURSES_FORM: Request sent.";
const COURSES_FORM_SUCCESS = "COURSES_FORM: Successful request.";
const COURSES_FORM_ERROR = "COURSES_FORM: Failed request.";

const SET_COURSES_FORM = "COURSES_FORM: Set new form default data.";

const ADD_COURSE = "ADD_COURSE: Adding new course to database.";
const ADD_COURSE_REQUEST = "ADD_COURSE: Request sent.";
const ADD_COURSE_SUCCESS = "ADD_COURSE: Successful request.";
const ADD_COURSE_ERROR = "ADD_COURSE: Failed request.";

const SET_COURSES = "COURSES: Set available courses.";

const COURSES = "COURSES: Retrieving all courses.";
const COURSES_REQUEST = "COURSES: Request sent.";
const COURSES_SUCCESS = "COURSES: Successful request.";
const COURSES_ERROR = "COURSES: Failed request.";

const SET_UPDATE_COURSE = "SET_UPDATE_COURSE: Set available courses.";

const UPDATE_COURSE = "UPDATE_COURSE: Retrieving all courses.";
const UPDATE_COURSE_REQUEST = "UPDATE_COURSE: Request sent.";
const UPDATE_COURSE_SUCCESS = "UPDATE_COURSE: Successful request.";
const UPDATE_COURSE_ERROR = "UPDATE_COURSE: Failed request.";

export { COURSES_FORM, ADD_COURSE, COURSES, UPDATE_COURSE };

export default {
  state: {
    loadingForm: false,
    committees: [],
    languages: [],
    attendance: [],
    loading: false,
    courses: undefined
  },
  mutations: {
    [SET_COURSES_FORM](state, data) {
      state.committees = data.committees;
      state.languages = data.languages;
      state.attendance = data.attendance;
    },
    [COURSES_FORM_REQUEST](state) {
      state.loadingForm = true;
    },
    [COURSES_FORM_SUCCESS](state) {
      state.loadingForm = false;
    },
    [COURSES_FORM_ERROR](state) {
      state.loadingForm = false;
    },

    [SET_COURSES](state, data) {
      state.courses = data;
    },
    [COURSES_REQUEST](state) {
      state.loading = true;
    },
    [COURSES_SUCCESS](state) {
      state.loading = false;
    },
    [COURSES_ERROR](state) {
      state.loading = false;
    },

    [SET_UPDATE_COURSE](state, data) {
      Vue.set(state.courses, data.id, data);
    },
    [UPDATE_COURSE_REQUEST]() {},
    [UPDATE_COURSE_SUCCESS]() {},
    [UPDATE_COURSE_ERROR]() {}
  },
  actions: {
    [COURSES_FORM]({ commit }) {
      commit(COURSES_FORM_REQUEST);
      return Vue.axios
        .get("courses/new")
        .then(resp => {
          commit(SET_COURSES_FORM, resp.data);
          commit(COURSES_FORM_SUCCESS);
        })
        .catch(({ status, errors }) => {
          commit(COURSES_FORM_ERROR, errors);
          throw { status, errors };
        });
    },
    [ADD_COURSE](
      { commit },
      {
        requested_by,
        date,
        duration,
        location,
        notes,
        language,
        committee,
        dances
      }
    ) {
      commit(ADD_COURSE_REQUEST);
      return Vue.axios
        .post("courses/new", {
          requested_by: requested_by,
          date: date,
          duration: duration,
          location: location,
          notes: notes,
          language: language,
          committee: committee,
          dances: dances
        })
        .then(() => {
          commit(ADD_COURSE_SUCCESS);
        })
        .catch(({ status, errors }) => {
          commit(ADD_COURSE_ERROR, errors);
          throw { status, errors };
        });
    },
    [COURSES]({ commit }) {
      commit(COURSES_REQUEST);
      return Vue.axios
        .get("courses")
        .then(resp => {
          commit(SET_COURSES, resp.data);
          commit(COURSES_SUCCESS);
        })
        .catch(({ status, errors }) => {
          commit(COURSES_ERROR, errors);
          throw { status, errors };
        });
    },
    [UPDATE_COURSE]({ commit }, { id }) {
      commit(UPDATE_COURSE_REQUEST);
      return Vue.axios
        .get(`courses/updated/${id}`)
        .then(resp => {
          commit(SET_UPDATE_COURSE, resp.data);
          commit(UPDATE_COURSE_SUCCESS);
        })
        .catch(({ status, errors }) => {
          commit(UPDATE_COURSE_ERROR, errors);
          throw { status, errors };
        });
    }
  },
  getters: {
    committees: state => {
      return state.committees;
    },
    hasCommittees: (state, getters) => {
      return getters.committees.length > 0;
    },
    languages: state => {
      return state.languages;
    },
    hasLanguages: (state, getters) => {
      return getters.languages.length > 0;
    },
    attendance: state => {
      return state.attendance;
    },
    hasAttendance: (state, getters) => {
      return getters.attendance.length > 0;
    },
    courses: state => {
      return state.courses ? Object.values(state.courses) : [];
    },
    hasCourses: (state, getters) => {
      return getters.courses.length > 0;
    }
  }
};
