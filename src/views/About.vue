<template>
  <div>
    <h1>This is an about page</h1>
    <button class="waves-effect waves-light btn" v-on:click="testConnection">
      Test Connection
    </button>
  </div>
</template>

<script>
import { TEST } from "./../store/modules/auth";
export default {
  methods: {
    testConnection: function() {
      this.$store.dispatch(TEST);
    }
  }
};
</script>
