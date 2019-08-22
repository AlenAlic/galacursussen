import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store/index";
import "./registerServiceWorker";
import VueAxios from "vue-axios";
import { axiosInstance } from "./api";
import AuthHandler from "./components/auth/AuthHandler";
import materialize from "materialize-css";
import Vue2TouchEvents from "vue2-touch-events";
import Datetime from "vue-datetime";
import "vue-datetime/dist/vue-datetime.css";
import Notify from "vue2-notify";
import { library } from "@fortawesome/fontawesome-svg-core";
import {
  faMusic,
  faCircle,
  faMapMarkerAlt,
  faAt,
  faEuroSign,
  faHashtag,
  faHistory
} from "@fortawesome/free-solid-svg-icons";
import {
  faBuilding,
  faCalendarAlt,
  faClock,
  faClipboard,
  faCompass,
  faStickyNote
} from "@fortawesome/free-regular-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

library.add(
  faMusic,
  faCircle,
  faMapMarkerAlt,
  faAt,
  faEuroSign,
  faHashtag,
  faHistory,
  faBuilding,
  faCalendarAlt,
  faClock,
  faClipboard,
  faCompass,
  faStickyNote
);
Vue.component("font-awesome-icon", FontAwesomeIcon);

Vue.config.productionTip = false;

Vue.use(AuthHandler);
Vue.use(materialize);
Vue.use(Vue2TouchEvents, { swipeTolerance: 30 });
Vue.use(Datetime);
// Default notifications configuration: vue2-notify
Vue.use(Notify, {
  itemClass: "bla",
  permanent: false,
  duration: 300,
  visibility: 5000,
  position: "top-full"
});
const types = {
  info: { itemClass: "toaster", iconClass: "alert__icon mdi mdi-information" },
  error: {
    itemClass: "toaster--error",
    iconClass: "alert__icon mdi mdi-alert-circle"
  },
  warning: {
    itemClass: "toaster--warning",
    iconClass: "alert__icon mdi mdi-alert"
  },
  success: {
    itemClass: "toaster--success",
    iconClass: "alert__icon mdi mdi-checkbox-marked-circle"
  }
};

Vue.$notify.setTypes(types);

// Use config.json for production-like env and the <env_name>.json for other env;
const configFileName =
  process.env.NODE_ENV === "production"
    ? "config.json"
    : process.env.NODE_ENV + ".json";
axiosInstance
  .get(configFileName)
  .then(config => config.data)
  .then(
    config => {
      Vue.prototype.$config = config;
      Vue.prototype.$config.debug = process.env.NODE_ENV === "development";

      // Set the baseURL according to the latest config and register the instance.
      axiosInstance.defaults.baseURL = Vue.prototype.$config.api.url;
      Vue.use(VueAxios, axiosInstance);

      new Vue({
        router,
        store,
        render: h => h(App)
      }).$mount("#app");
    },
    () => console.log("No configuration fie provided.")
  );

// new Vue({
//   el: "#app",
//   router,
//   store,
//   template: "<App/>",
//   components: { App }
// });
