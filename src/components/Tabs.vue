<template>
  <div>
    <ul class="tabs">
      <li class="tab" v-for="(tab, index) in tabs" :key="tab">
        <a
          href="javascript:void(0);"
          :class="{ active: page === index }"
          @click="changePage(index)"
        >
          {{ tab }}</a
        >
      </li>
    </ul>
    <div
      v-for="(tab, index) in pages"
      :key="index"
      :style="{ display: page === index ? 'block' : 'none' }"
    >
      {{ tab }}
    </div>
  </div>
</template>

<script>
export default {
  name: "Tabs",
  props: { data: {} },
  data: function() {
    return {
      page: 0
    };
  },
  methods: {
    changePage: function(i) {
      this.page = i;
    }
  },
  computed: {
    tabs: function() {
      let x = this.data;
      return x !== {} ? Object.keys(x) : [];
    },
    pages: function() {
      let x = this.data;
      return x !== {} ? Object.values(x) : [];
    }
  }
};
</script>

<style scoped lang="scss"></style>
