<template>
  <div class="left-align" :class="{ assigned: assigned }">
    <div v-if="course">
      <course-modals
        v-if="this.$store.getters.hasOrganizerPrivileges"
        :course="course"
      />
      <course-info :course="course" />
      <course-assigned class="mt" :course="course" />
      <course-responses-single :course="course" />
    </div>
  </div>
</template>

<script>
import CourseModals from "@/components/courses/CourseModals";
import CourseInfo from "@/components/courses/CourseInfo";
import CourseResponsesSingle from "@/components/courses/CourseResponsesSingle";
import CourseAssigned from "@/components/courses/CourseAssigned";
export default {
  name: "UpcomingCourse",
  props: { course: Object },
  components: {
    CourseAssigned,
    CourseResponsesSingle,
    CourseInfo,
    CourseModals
  },
  computed: {
    assigned: function() {
      let assignments = this.course.assignments;
      return (
        assignments.filter(a => {
          return a.assigned && a.user_id === this.$store.getters.currentUser.id;
        }).length > 0
      );
    }
  }
};
</script>

<style scoped lang="scss">
.mt {
  margin-top: 1rem;
}
.assigned {
  background: #4caf5030;
}
</style>
