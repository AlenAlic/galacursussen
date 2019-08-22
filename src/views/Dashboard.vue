<template>
  <div>
    <not-responded-courses />
    <upcoming-courses v-if="courses" />
    <h4 v-else-if="!this.$store.state.courses.loading">There are no upcoming courses.</h4>
    <create-new-request v-if="this.$store.getters.hasOrganizerPrivileges" />
    <this-academic-years-courses
      v-if="this.$store.getters.hasOrganizerPrivileges"
    />
  </div>
</template>

<script>
import { COURSES } from "@/store/modules/courses";
import NotRespondedCourses from "@/components/dashboard/NotRespondedCourses";
import CreateNewRequest from "@/components/dashboard/CreateNewRequest";
import ThisAcademicYearsCourses from "@/components/dashboard/ThisAcademicYearsCourses";
import UpcomingCourses from "@/components/dashboard/UpcomingCourses";
export default {
  name: "Dashboard",
  components: {
    UpcomingCourses,
    NotRespondedCourses,
    CreateNewRequest,
    ThisAcademicYearsCourses
  },
  created() {
    if (!this.$store.getters.hasCourses) this.$store.dispatch(COURSES);
  },
  computed: {
    courses: function() {
      return this.$store.getters.courses.length > 0;
    }
  }
};
</script>

<style scoped lang="scss"></style>
