<template>
  <div class="left-align" :class="{ assigned: assigned }">
    <div v-if="course">
      <course-modals
        v-if="this.$store.getters.hasOrganizerPrivileges"
        :course="course"
        @closeModal="closeModal"
      />
      <course-info :course="course" />
      <course-assigned class="mt" :course="course" />
      <course-responses-single :course="course" />
      <course-respond-buttons
        v-if="assignment.attendance"
        :course="course"
        :assignment="assignment"
      />
    </div>
  </div>
</template>

<script>
import { UPDATE_COURSE } from "@/store/modules/courses";
import CourseModals from "@/components/courses/CourseModals";
import CourseInfo from "@/components/courses/CourseInfo";
import CourseResponsesSingle from "@/components/courses/CourseResponsesSingle";
import CourseAssigned from "@/components/courses/CourseAssigned";
import CourseRespondButtons from "@/components/courses/CourseRespondButtons";
export default {
  name: "UpcomingCourse",
  props: { course: Object },
  components: {
    CourseRespondButtons,
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
    },
    assignment: function() {
      let assignments = this.course.assignments;
      return assignments.filter(a => {
        return a.user_id === this.$store.getters.currentUser.id;
      })[0];
    }
  },
  methods: {
    closeModal: function() {
      let id = this.course.id;
      this.$store.dispatch(UPDATE_COURSE, { id });
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
