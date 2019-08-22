<template>
  <div class="response-list">
    <card-collapse-list title="Assigned" :bold="true">
      <div v-for="assignment in assigned" :key="assignment.id">
        {{ assignment.name }}
        <i class="pl" v-show="assignment.role">{{ assignment.role }}</i>
      </div>
    </card-collapse-list>
  </div>
</template>

<script>
import CardCollapseList from "@/components/courses/CardCollapseList";
export default {
  name: "CourseAssigned",
  props: { course: Object },
  components: {
    CardCollapseList
  },
  computed: {
    assigned: function() {
      return this.course.assignments.filter(r => {
        return r.assigned;
      });
    }
  },
  methods: {
    role: function(assignment) {
      return assignment.role === "teacher"
        ? "L"
        : assignment.role === "assistant"
        ? "A"
        : assignment.role === "mucie"
        ? "M"
        : "";
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
.pl {
  padding-left: 0.75rem;
}
</style>
