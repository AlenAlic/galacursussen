<template>
  <li :class="{ active: this.$route.path === navigateTo }">
    <router-link tag="a" :to="navigateTo" class="waves-effect">
      <i v-if="icon" class="material-icons left">{{ icon }}</i
      >{{ text }}</router-link
    >
  </li>
</template>

<script>
export default {
  name: "nav-link",
  props: { navigateTo: String, text: String, icon: String }
};
</script>
