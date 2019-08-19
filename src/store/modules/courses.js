/* eslint-disable no-undef */
import Vue from "vue";

const COURSES_FORM = "COURSES_FORM: Get form data for creating a new course.";
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

export { COURSES_FORM, ADD_COURSE, COURSES };

export default {
  state: {
    loadingForm: false,
    committees: [],
    languages: [],
    loading: false,
    courses: []
  },
  mutations: {
    [SET_COURSES_FORM](state, data) {
      state.committees = data.committees;
      state.languages = data.languages;
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
    }
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
    }
  },
  getters: {
    allCourses: state => {
      return state.course ? state.courses : {};
    }
  }
};
