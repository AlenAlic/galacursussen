<template>
  <div class="response-list">
    <card-collapse-list :title="responsesTitle">
      <response-list :assignments="assignments" />
    </card-collapse-list>
  </div>
</template>

<script>
import ResponseList from "@/components/courses/ResponseList";
import CardCollapseList from "@/components/courses/CardCollapseList";
export default {
  name: "CourseResponses",
  props: { course: Object },
  components: {
    CardCollapseList,
    ResponseList
  },
  data: function() {
    return {
      assignments: this.course.assignments
    };
  },
  computed: {
    totalRequests: function() {
      return this.assignments.length;
    },
    responses: function() {
      return (
        this.totalRequests -
        this.assignments.filter(r => {
          return !r.attendance;
        }).length
      );
    },
    responsesTitle: function() {
      return `Responses ${this.responses} / ${this.totalRequests}`;
    }
  }
};
</script>

<style scoped lang="scss">
.response-list {
  margin-bottom: 1.5rem;
  border-bottom: 1px solid grey;
  padding-bottom: 0.75rem;
}
</style>
