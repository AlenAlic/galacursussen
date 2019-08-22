<template>
  <div class="left-align">
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
  }
};
</script>

<style scoped lang="scss">
.mt {
  margin-top: 1rem;
}
</style>
