<template>
  <div class="status">
    <div class="text-success">
      <font-awesome-icon icon="circle" size="sm" />
      Yes
    </div>
    <div class="text-warning">
      <font-awesome-icon icon="circle" size="sm" />
      Maybe
    </div>
    <div class="text-danger">
      <font-awesome-icon icon="circle" size="sm" />
      No
    </div>
    <div class="grey-text" v-if="notResponded">
      <font-awesome-icon icon="circle" size="sm" />
      Not responded
    </div>
  </div>
</template>

<script>
export default {
  name: "AttendingStatus",
  props: { notResponded: Boolean }
};
</script>

<style scoped lang="scss">
.status {
  width: 100%;
  display: flex;
  justify-content: space-around;
  font-size: 0.75rem;
}
</style>
