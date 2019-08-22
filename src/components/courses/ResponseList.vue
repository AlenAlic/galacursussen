<template>
  <div class="row">
    <div class="col s12 m6">
      <h6 class="title">
        <b>Responses</b> - {{ totalResponses }} / {{ totalRequests }}
      </h6>
      <response-list-entry
        v-for="assignment in responded"
        :key="assignment.id"
        :assignment="assignment"
      />
    </div>
    <div class="col s12 m6">
      <h6 class="title">
        <b>Not responded</b> - {{ totalRequests - totalResponses }}
      </h6>
      <response-list-entry
        v-for="assignment in notResponded"
        :key="assignment.id"
        :assignment="assignment"
      />
    </div>
  </div>
</template>

<script>
import ResponseListEntry from "@/components/courses/ResponseListEntry";
export default {
  name: "ResponseList",
  props: { assignments: Array },
  components: { ResponseListEntry },
  computed: {
    totalRequests: function() {
      return this.assignments.length;
    },
    totalResponses: function() {
      return this.totalRequests - this.not_responded.length;
    },
    yes: function() {
      return this.assignments.filter(r => {
        return r.attendance === "yes";
      });
    },
    maybe: function() {
      return this.assignments.filter(r => {
        return r.attendance === "maybe";
      });
    },
    no: function() {
      return this.assignments.filter(r => {
        return r.attendance === "no";
      });
    },
    responded: function() {
      return []
        .push(...this.yes)
        .push(...this.maybe)
        .push(...this.no);
    },
    notResponded: function() {
      return this.assignments.filter(r => {
        return !r.attendance;
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
