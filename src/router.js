import Vue from "vue";
import Router from "vue-router";
const Login = () => import("@/views/Login.vue");
const Dashboard = () => import("@/views/Dashboard.vue");
const PastCourses = () => import("@/views/PastCourses.vue");
const Admin = () => import("@/views/Admin.vue");
const SendEmail = () => import("@/views/SendEmails.vue");
const Activate = () => import("@/views/Activate.vue");
const SetPassword = () => import("@/views/SetPassword.vue");
const Profile = () => import("@/views/Profile.vue");
const ResetPassword = () => import("@/views/ResetPassword.vue");
const Hours = () => import("@/views/Hours.vue");

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
    { path: "/index.html", component: Login, alias: "/login" }, // Fix for PWA at /index.html
    {
      path: "/activate/:token",
      component: Activate
    },
    {
      path: "/set_password/:token",
      name: "set_password",
      component: SetPassword
    },
    {
      path: "/reset_password/:token?",
      name: "reset_password",
      component: ResetPassword
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
        auth: true,
        access: ["Admin", "Organizer", "Member"]
      }
    },
    {
      path: "/emails",
      name: "emails",
      component: SendEmail,
      meta: {
        auth: true,
        access: ["Admin", "Organizer"]
      }
    },
    {
      path: "/admin",
      name: "admin",
      component: Admin,
      meta: {
        auth: true,
        access: ["Admin"]
      }
    },
    {
      path: "/hours",
      name: "hours",
      component: Hours,
      meta: {
        auth: true,
        access: ["Admin", "Organizer", "Member"]
      }
    },
    {
      path: "/profile",
      name: "profile",
      component: Profile,
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
  // if (to.meta && to.meta.access) {
  //   //Check if user has correct authorization
  //   if (!to.meta.access.includes(Vue.$store.getters.accessLevel)) {
  //     Vue.$notify("Permission denied.", "error");
  //     next({
  //       name: "dashboard",
  //       query: {
  //         redirect: to.path
  //       }
  //     });
  //     return;
  //   }
  // }
  next();
});

export default router;
