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
  faHistory,
  faUserTie,
  faSignature,
  faKey,
  faCheck,
  faTimes
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
  faUserTie,
  faSignature,
  faKey,
  faCheck,
  faTimes
);
library.add(
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
Vue.use(Notify, {
  itemClass: "notification",
  permanent: false,
  duration: 300,
  visibility: 5000,
  position: "top-full",
  closeButtonClass: "close"
});
const types = {
  info: { itemClass: "toaster", iconClass: "alert-icon mdi mdi-information" },
  error: {
    itemClass: "toaster--error",
    iconClass: "alert-icon mdi mdi-alert-circle"
  },
  warning: {
    itemClass: "toaster--warning",
    iconClass: "alert-icon mdi mdi-alert"
  },
  success: {
    itemClass: "toaster--success",
    iconClass: "alert-icon mdi mdi-checkbox-marked-circle"
  }
};
Vue.$notify.setTypes(types);

Vue.prototype.$config = {};
Vue.prototype.$config.debug = process.env.NODE_ENV === "development";
axiosInstance.defaults.baseURL = process.env.VUE_APP_BASE_URL;
Vue.use(VueAxios, axiosInstance);

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");
