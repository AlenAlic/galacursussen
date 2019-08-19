<template>
  <div id="app" class="grey lighten-3">
    <navbar v-if="$auth.isAuthenticated()" />
    <router-view class="container" />
  </div>
</template>

<script>
import { USER_PROFILE } from "./store/modules/auth";
import Navbar from "@/components/navs/Navbar";
export default {
  name: "app",
  components: { Navbar },
  created() {
    if (this.$store.state.auth.token) this.$store.dispatch(USER_PROFILE);
  }
};
</script>

<style lang="scss">
#app {
  min-height: 100%;
  height: 100%;
  text-align: center;
  overflow-x: auto;
}
</style>
<!-- Import SCSS boilerplate -->
<style src="./assets/css/styles.scss" lang="scss"></style>
