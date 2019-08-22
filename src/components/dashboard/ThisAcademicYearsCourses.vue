<template>
  <collapse-card
    title="This years courses/workshops"
    :loading="this.$store.state.courses.loading"
    :counter="courses.length"
  >
    <course v-for="course in courses" :key="course.key" :course="course" />
  </collapse-card>
</template>

<script>
import CollapseCard from "@/components/CollapseCard";
import Course from "@/components/courses/Course";
export default {
  name: "ThisAcademicYearsCourses",
  components: { CollapseCard, Course },
  computed: {
    courses: function() {
      return this.$store.getters.courses;
    }
  }
};
</script>
