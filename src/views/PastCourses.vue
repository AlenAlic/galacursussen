<template>
  <div>
    <this-academic-years-courses />
  </div>
</template>

<script>
import { COURSES } from "@/store/modules/courses";
import ThisAcademicYearsCourses from "@/components/dashboard/ThisAcademicYearsCourses";
export default {
  name: "PastCourses",
  components: {
    ThisAcademicYearsCourses
  },
  created() {
    if (!this.$store.getters.hasCourses) this.$store.dispatch(COURSES);
  }
};
</script>

<style scoped lang="scss"></style>
