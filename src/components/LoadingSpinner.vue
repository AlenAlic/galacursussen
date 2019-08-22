<template>
  <div class="preloader-wrapper active" :class="size">
    <div class="spinner-layer spinner-primary-only">
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
@import "../assets/css/config";
.preloader-wrapper.tiny {
  width: 24px;
  height: 24px;
}
.preloader-wrapper.spinner-btn {
  width: 18px;
  height: 18px;
  position: relative;
  top: 4px;
  margin-left: 10px;
}
.spinner-primary-only {
  border-color: $primary-color;
}
</style>
