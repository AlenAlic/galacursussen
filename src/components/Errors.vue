<template>
  <div class="errors text-danger">
    <div v-for="(err, index) in errors" v-bind:key="index" class="text-error">
      {{ err }}
    </div>
  </div>
</template>

<script>
export default {
  name: "Errors",
  props: { errors: Array }
};
</script>

<style scoped lang="scss">
.errors {
  padding-bottom: 0.5rem;
  div {
    margin: 0.25rem 0;
  }
}
</style>
