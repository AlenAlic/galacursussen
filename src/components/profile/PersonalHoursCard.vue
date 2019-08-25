<template>
  <div class="card">
    <div class="card-content">
      <span class="card-title">{{ committee }} hours</span>
      <loading-spinner v-if="loading" />
      <div v-else-if="hours.assignments.length > 0" class="left-align">
        <div v-for="assignment in hours.assignments" :key="assignment.id">
          <h6>
            <b>{{ assignment.requested_by }}</b>
          </h6>
          <div>{{ assignment.date_formatted }}</div>
          <div class="right-align">
            {{ assignment.duration_formatted }}
          </div>
        </div>
        <div class="total">
          <div><i>Total</i></div>
          <div>{{ hours.total }}</div>
        </div>
      </div>
      <h6 v-else>You have no hours with the {{ committee }}.</h6>
    </div>
  </div>
</template>

<script>
import LoadingSpinner from "@/components/LoadingSpinner";
export default {
  name: "PersonalHoursCard",
  components: { LoadingSpinner },
  props: { hours: Object, committee: String, loading: Boolean }
};
</script>

<style scoped lang="scss">
.card {
  max-width: 90vw;
  width: 400px;
  .card-content {
    .card-title {
      margin-bottom: 2rem;
    }
  }
}
.total {
  border-top: 1px solid grey;
  margin-top: 0.5rem;
  padding-top: 0.25rem;
  display: flex;
  justify-content: space-between;
}
</style>
