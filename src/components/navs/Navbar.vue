<template>
  <div>
    <nav>
      <div class="nav-wrapper container">
        <a
          href="javascript:void(0);"
          class="left sidenav-trigger"
          @click.prevent="showSideNav"
          ><i class="material-icons">menu</i></a
        >
        <ul class="left hide-on-med-and-down">
          <nav-link navigate-to="/about" path="path" text="About" />
          <nav-link
            navigate-to="/dashboard"
            text="Dashboard"
            icon="dashboard"
          />
        </ul>
        <ul class="right hide-on-med-and-down">
          <nav-link navigate-to="/profile" text="Profile" icon="person" />
          <li>
            <a
              @click.prevent="logout"
              class="waves-effect waves-light btn teal lighten-2 white-text"
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
          <div class="user-view">
            <div class="background">
              <img
                src="https://leasticoulddo.com/wp-content/uploads/2019/08/licd5144-aug16_19_thumbnail.jpg"
                alt="Dummy"
              />
            </div>
            <a href="#"
              ><img
                class="circle"
                src="https://leasticoulddo.com/wp-content/uploads/2019/08/licd5144-aug16_19_thumbnail.jpg"
                alt="Dummy"
            /></a>
            <a href="#"><span class="white-text name">John Doe</span></a>
            <a href="#"
              ><span class="white-text email">jdandturk@gmail.com</span></a
            >
          </div>
        </li>
        <li>
          <a href="#"
            ><i class="material-icons">cloud</i>First Link With Icon</a
          >
        </li>
        <li><a href="#">Second Link</a></li>
        <li><div class="divider"></div></li>
        <li><a class="subheader">Subheader</a></li>
        <li><a class="waves-effect" href="#">Third Link With Waves</a></li>
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
      this.dragging = true;
      this.startPosition = this.calculateDraggingPos(
        event.targetTouches[0].clientX
      );
    },
    draggingSideNavOpen: function(event) {
      this.position = this.calculateDraggingPos(event.targetTouches[0].clientX);
    },
    draggingSideNavClose: function(event) {
      let x =
        this.calculateDraggingPos(event.targetTouches[0].clientX) +
        100 -
        this.startPosition;
      x = x > 100 ? 100 : x;
      this.position = x;
    },
    stopDraggingSideNav: function() {
      this.dragging = false;
      this.setSideNav(this.position >= 80);
    }
  }
};
</script>

<style scoped lang="scss">
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
