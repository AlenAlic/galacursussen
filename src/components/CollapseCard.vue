<template>
  <div class="card">
    <ul class="collapsible">
      <li>
        <div class="collapsible-header" @click="toggle">
          <div class="title">
            {{ title }} <span v-if="counter">({{ counter }})</span>
            <loading-spinner class="loading" size="tiny" v-if="loading" />
          </div>
          <div>
            <i
              class="material-icons right trans-rotate clickable unselectable"
              :class="{ 'rotate-180': open }"
            >
              arrow_drop_down_circle</i
            >
          </div>
        </div>
        <div class="collapsible-body">
          <slot></slot>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
import LoadingSpinner from "@/components/LoadingSpinner";
export default {
  name: "CollapseCard",
  props: { title: String, loading: Boolean, counter: Number },
  components: { LoadingSpinner },
  data: function() {
    return {
      open: false,
      ready: false
    };
  },
  methods: {
    toggle: function() {
      if (this.ready) this.open = !this.open;
    }
  },
  mounted: function() {
    this.$nextTick(function() {
      this.ready = true;
      // eslint-disable-next-line no-undef
      M.Collapsible.init(document.querySelectorAll(".collapsible"), {
        inDuration: 400,
        outDuration: 400
      });
    });
  }
};
</script>

<style scoped lang="scss">
.collapsible-header {
  display: flex;
  justify-content: space-between;
  align-content: center;
  width: 100%;
  line-height: 1.5rem;
  font-size: 1.5rem;
  font-weight: 300;
  padding: 2rem 1rem 2rem 2rem;
}
.loading {
  margin-left: 1rem;
}
</style>
