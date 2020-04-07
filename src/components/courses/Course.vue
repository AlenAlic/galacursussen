<template>
  <div class="left-align">
    <div v-if="course">
      <course-modals v-if="this.$store.getters.hasOrganizerPrivileges" :course="course" @closeModal="closeModal" />
      <course-info :course="course" />
      <course-assigned class="mt" :course="course" />
      <course-responses :course="course" />
      <course-cancel v-if="this.$store.getters.hasOrganizerPrivileges" :course="course" @closeModal="closeModal" />
    </div>
  </div>
</template>

<script>
import CourseModals from "@/components/courses/CourseModals";
import CourseInfo from "@/components/courses/CourseInfo";
import CourseResponses from "@/components/courses/CourseResponses";
import CourseAssigned from "@/components/courses/CourseAssigned";
import CourseCancel from "@/components/courses/CourseCancel";
export default {
  name: "Course",
  props: { course: Object },
  components: {
    CourseCancel,
    CourseAssigned,
    CourseResponses,
    CourseInfo,
    CourseModals
  },
  methods: {
    closeModal: function() {
      this.$emit("closeModal");
    }
  }
};
</script>

<style scoped lang="scss">
.mt {
  margin-top: 1rem;
}
</style>
