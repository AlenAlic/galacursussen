<template>
  <div>
    <h6 class="title"><b>Responses</b> - {{ totalResponses }}</h6>
    <response-list-entry
      v-for="assignment in responded"
      :key="assignment.id"
      :assignment="assignment"
    />
    <h6 class="title"><b>Not responded</b> - {{ totalRequests - totalResponses }}</h6>
    <response-list-entry
      v-for="assignment in notResponded"
      :key="assignment.id"
      :assignment="assignment"
    />
  </div>
</template>

<script>
import ResponseListEntry from "@/components/courses/ResponseListEntry";
export default {
  name: "ResponseListSingle",
  props: { assignments: Array },
  components: { ResponseListEntry },
  computed: {
    totalRequests: function() {
      return this.assignments.length;
    },
    totalResponses: function() {
      return this.totalRequests - this.notResponded.length;
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
        .concat(...this.yes)
        .concat(...this.maybe)
        .concat(...this.no);
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
