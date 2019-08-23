<template>
  <button
    :disabled="!active || loading"
    class="waves-effect waves-light btn"
    :class="{ 'no-click': !active }"
  >
    {{ text }} <loading-spinner size="spinner-btn" v-if="loading" />
  </button>
</template>

<script>
import LoadingSpinner from "@/components/LoadingSpinner";
export default {
  name: "SaveButton",
  components: { LoadingSpinner },
  props: { loading: Boolean, active: Boolean, text: String }
};
</script>
