<template>
  <div class="members">
    <div class="left-align">
      <b v-if="bold">{{ title }}</b>
      <span v-else>{{ title }}</span>
      <i
        class="material-icons right trans-rotate clickable"
        @click="changing"
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
  props: { title: String, bold: Boolean },
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
  },
  methods: {
    changing: function() {
      this.$emit("changing");
      this.open = !this.open;
    }
  }
};
</script>

<style scoped lang="scss">
.trans-collapsible,
.members {
  width: 100%;
}
</style>
