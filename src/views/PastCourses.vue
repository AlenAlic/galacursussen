<template>
  <div>
    <this-academic-years-courses />
    <previous-years-courses />
  </div>
</template>

<script>
import { COURSES } from "@/store/modules/courses";
import ThisAcademicYearsCourses from "@/components/dashboard/ThisAcademicYearsCourses";
import PreviousYearsCourses from "@/components/dashboard/PreviousYearsCourses";
export default {
  name: "PastCourses",
  components: {
    PreviousYearsCourses,
    ThisAcademicYearsCourses
  },
  created() {
    if (!this.$store.getters.hasCourses) this.$store.dispatch(COURSES);
  }
};
</script>
