<template>
  <collapse-card title="This years courses/workshops" :loading="!hasCourses">
    <course v-for="course in courses" :key="course.key" :data="course" />
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
    },
    hasCourses: function() {
      return this.$store.getters.hasCourses;
    }
  }
};
</script>
