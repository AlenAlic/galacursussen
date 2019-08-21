<template>
  <div>
    <not-responded-courses />
    <create-new-request
      v-if="
        this.$store.getters.currentUser.admin ||
          this.$store.getters.currentUser.organizer
      "
    />
    <this-academic-years-courses
      v-if="
        this.$store.getters.currentUser.admin ||
          this.$store.getters.currentUser.organizer
      "
    />
  </div>
</template>

<script>
import { COURSES } from "@/store/modules/courses";
import NotRespondedCourses from "@/components/dashboard/NotRespondedCourses";
import CreateNewRequest from "@/components/dashboard/CreateNewRequest";
import ThisAcademicYearsCourses from "@/components/dashboard/ThisAcademicYearsCourses";
export default {
  name: "Dashboard",
  components: {
    NotRespondedCourses,
    CreateNewRequest,
    ThisAcademicYearsCourses
  },
  created() {
    if (!this.$store.getters.hasCourses) this.$store.dispatch(COURSES);
  }
};
</script>

<style scoped lang="scss"></style>
