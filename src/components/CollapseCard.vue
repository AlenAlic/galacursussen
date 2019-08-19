<template>
  <div class="card">
    <div class="card-content">
      <span class="card-title left-align">
        {{ title }}
        <i
          class="material-icons right trans-rotate clickable"
          @click="open = !open"
          :class="{ 'rotate-180': open }"
        >
          arrow_drop_down_circle</i
        >
        <loading-spinner class="loading" size="tiny" v-if="loading" />
      </span>
      <div
        class="trans-collapsible"
        :style="{ height: `${this.height}px` }"
        ref="form"
      >
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<script>
import LoadingSpinner from "@/components/LoadingSpinner";
export default {
  name: "CollapseCard",
  props: { title: String, loading: Boolean },
  components: { LoadingSpinner },
  data: function() {
    return {
      open: false,
      height: 0
    };
  },
  watch: {
    open: function(newVals) {
      this.height = newVals ? this.$refs.form.scrollHeight : 0;
    }
  }
};
</script>

<style scoped lang="scss">
.loading {
  margin-left: 1rem;
}
</style>
