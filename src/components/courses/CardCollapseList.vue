<template>
  <div class="members">
    <div class="left-align">
      {{ title }}
      <i
        class="material-icons right trans-rotate clickable"
        @click="open = !open"
        :class="{ 'rotate-180': open }"
      >
        keyboard_arrow_down</i
      >
    </div>
    <div
      class="trans-collapsible"
      :style="{ height: `${this.height}px` }"
      ref="form"
    >
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: "CardCollapseList",
  props: { title: String },
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
.members {
  width: 100%;
}
</style>
