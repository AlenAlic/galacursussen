<template>
  <div class="row">
    <div class="col s12 m6">
      <h6 class="title">
        <b>Assigned</b>
      </h6>
      <response-list-entry
        v-for="assignment in assigned"
        :key="assignment.id"
        :assignment="assignment"
      />
    </div>
    <div class="col s12 m6">
      <h6 class="title">
        <b>Not assigned</b>
      </h6>
      <response-list-entry
        v-for="assignment in notAssigned"
        :key="assignment.id"
        :assignment="assignment"
      />
    </div>
  </div>
</template>

<script>
import ResponseListEntry from "@/components/courses/ResponseListEntry";
export default {
  name: "AssignedList",
  props: { assignments: Array },
  components: { ResponseListEntry },
  computed: {
    assigned: function() {
      return this.assignments.filter(r => {
        return r.assigned;
      });
    },
    notAssigned: function() {
      return this.assignments.filter(r => {
        return !r.assigned;
      });
    }
  }
};
</script>

<style scoped lang="scss">
.title {
  border-bottom: 1px solid grey;
}
</style>
