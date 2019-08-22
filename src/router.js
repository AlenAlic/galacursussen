import Vue from "vue";
import Router from "vue-router";
const Login = () => import("@/views/Login.vue");
const Dashboard = () => import("@/views/Dashboard.vue");
const PastCourses = () => import("@/views/PastCourses.vue");
const Profile = () => import("@/views/Profile.vue");
const TestingGrounds = () => import("@/views/TestingGrounds.vue");

Vue.use(Router);

let router = new Router({
  mode: "history",
  base: process.env.BASE_URL,
  routes: [
    {
      path: "/",
      redirect: "/login"
    },
    {
      path: "/login",
      name: "login",
      component: Login
    },
    {
      path: "/dashboard",
      name: "dashboard",
      component: Dashboard,
      meta: {
        auth: true
      }
    },
    {
      path: "/past_courses",
      name: "past_courses",
      component: PastCourses,
      meta: {
        auth: true
      }
    },
    {
      path: "/profile",
      name: "profile",
      component: Profile,
      meta: {
        auth: true
      }
    },
    {
      path: "/testing",
      name: "testing",
      component: TestingGrounds,
      meta: {
        auth: true
      }
    }
  ]
});

router.beforeEach((to, from, next) => {
  if (to.meta && to.meta.auth) {
    //Check if user is logged in.
    if (!Vue.prototype.$auth.isAuthenticated()) {
      next({
        name: "login",
        query: {
          redirect: to.path
        }
      });
      return;
    }
  }
  next();
});

export default router;
