<template>
  <div class="preloader-wrapper active" :class="size">
    <div class="spinner-layer">
      <div class="circle-clipper left">
        <div class="circle"></div>
      </div>
      <div class="gap-patch">
        <div class="circle"></div>
      </div>
      <div class="circle-clipper right">
        <div class="circle"></div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "LoadingSpinner",
  props: { size: String }
};
</script>

<style scoped lang="scss">
.preloader-wrapper.tiny {
  width: 24px;
  height: 24px;
}
</style>
