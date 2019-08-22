<template>
  <div class="navbar-fixed">
    <nav>
      <div class="nav-wrapper container">
        <a
          href="javascript:void(0);"
          class="left sidenav-trigger"
          @click.prevent="showSideNav"
          ><i class="material-icons">menu</i></a
        >
        <ul class="left hide-on-med-and-down">
          <nav-link
            navigate-to="/dashboard"
            text="Dashboard"
            icon="dashboard"
          />
          <nav-link
            navigate-to="/past_courses"
            text="Past courses"
            icon="history"
          />
          <nav-link
            v-if="this.$config.env === 'development'"
            navigate-to="/testing"
            text="Testing"
            icon="code"
          />
        </ul>
        <ul class="right hide-on-med-and-down">
          <nav-link navigate-to="/profile" text="Profile" icon="person" />
          <li>
            <a
              @click.prevent="logout"
              class="waves-effect waves-light btn white-text"
              >Log out <i class="material-icons right">exit_to_app</i></a
            >
          </li>
        </ul>
      </div>
    </nav>
    <transition :name="!dragging ? 'slide' : ''">
      <ul
        id="slide-out"
        class="sidenav"
        :class="{
          show: this.show,
          'slide-enter-active': !this.dragging
        }"
        v-touch:moved="setDraggingStartPos"
        v-touch:moving="draggingSideNavClose"
        v-touch:end="stopDraggingSideNav"
        v-touch:swipe.left="hideSideNav"
        :style="
          this.dragging
            ? { transform: `translateX(${this.position - 100}%)` }
            : null
        "
      >
        <li>
          <div class="user-view nav-img-background"></div>
        </li>
        <li>
          <nav-link
            navigate-to="/dashboard"
            text="Dashboard"
            icon="dashboard"
          />
          <nav-link
            navigate-to="/past_courses"
            text="Past courses"
            icon="history"
          />
          <nav-link
            v-if="this.$config.env === 'development'"
            navigate-to="/testing"
            text="Testing"
            icon="code"
          />
        </li>
        <li><div class="divider"></div></li>
        <li>
          <nav-link navigate-to="/profile" text="Profile" icon="person" />
        </li>
        <li>
          <div class="logout">
            <a
              @click.prevent="logout"
              class="waves-effect waves-light btn white-text"
              >Log out <i class="material-icons right">exit_to_app</i></a
            >
          </div>
        </li>
      </ul>
    </transition>
    <div
      class="drag-target"
      v-touch:moved="setDraggingStartPos"
      v-touch:moving="draggingSideNavOpen"
      v-touch:end="stopDraggingSideNav"
      v-touch:swipe.right="showSideNav"
    ></div>
    <transition :name="!dragging ? 'fade' : ''">
      <div
        class="sidenav-overlay"
        @click="hideSideNav"
        :class="{
          show: this.show,
          'fade-enter-active': !this.dragging
        }"
        v-touch:moved="setDraggingStartPos"
        v-touch:moving="draggingSideNavClose"
        v-touch:end="stopDraggingSideNav"
        v-touch:swipe.left="hideSideNav"
        :style="
          this.dragging
            ? { opacity: this.position / 100, display: 'block' }
            : null
        "
      ></div>
    </transition>
  </div>
</template>

<script>
import NavLink from "@/components/navs/NavLink";
export default {
  name: "navbar",
  components: { NavLink },
  data: function() {
    return {
      show: false,
      dragging: false,
      position: 1,
      startPosition: 0
    };
  },
  methods: {
    logout: function() {
      this.error = undefined;
      this.$auth
        .signOut()
        .then(() => {
          this.$router.replace({
            name: "login"
          });
        })
        .catch(() => {});
    },
    showSideNav: function() {
      this.show = true;
      document.body.style.overflow = "hidden";
    },
    hideSideNav: function() {
      this.show = false;
      document.body.style.overflow = "auto";
    },
    setSideNav: function(val) {
      val ? this.showSideNav() : this.hideSideNav();
    },
    calculateDraggingPos(val) {
      val = val < 0 ? 0 : val;
      val = val > 300 ? 300 : val;
      return Math.min(300, Math.abs(val)) / 3;
    },
    setDraggingStartPos: function(event) {
      if (event.type === "touchmove") {
        this.dragging = true;
        this.startPosition = this.calculateDraggingPos(
          event.targetTouches[0].clientX
        );
      }
    },
    draggingSideNavOpen: function(event) {
      if (event.type === "touchmove") {
        this.position = this.calculateDraggingPos(
          event.targetTouches[0].clientX
        );
      }
    },
    draggingSideNavClose: function(event) {
      if (event.type === "touchmove") {
        let x =
          this.calculateDraggingPos(event.targetTouches[0].clientX) +
          100 -
          this.startPosition;
        x = x > 100 ? 100 : x;
        this.position = x;
      }
    },
    stopDraggingSideNav: function() {
      this.dragging = false;
      this.setSideNav(this.position >= 80);
    }
  }
};
</script>

<style scoped lang="scss">
.user-view {
  height: 160px;
}
.sidenav .divider {
  margin: 6px 0 6px 0;
}
.logout {
  padding-top: 3rem;
}
.nav-img-background {
  background-image: url("../../../public/img/logo.png");
  background-size: contain;
  background-position: center;
  background-repeat: no-repeat;
}
@import "../../assets/css/config";
.sidenav {
  &.show {
    -webkit-transform: translateX(0%);
    transform: translateX(0%);
  }
  &-overlay {
    pointer-events: none;
    &.show {
      display: block;
      opacity: 1;
      pointer-events: auto;
    }
  }
}
.slide-enter-active,
.slide-leave-active {
  transition: transform $transition-time;
}
.slide-enter,
.slide-leave-to {
  transform: translateX(-105%);
}
.slide-enter-to,
.slide-leave {
  transform: translateX(0%);
}
.fade-enter-active,
.fade-leave-active {
  display: block;
  transition: opacity $transition-time;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}
.fade-enter-to,
.fade-leave {
  opacity: 1;
}
</style>
