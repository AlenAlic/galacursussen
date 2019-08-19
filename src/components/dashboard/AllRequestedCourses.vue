<template>
  <collapse-card title="All courses/workshops" :loading="!hasCourses">
    <course v-for="course in courses" :key="course.id" :data="course" />
  </collapse-card>
</template>

<script>
import CollapseCard from "@/components/CollapseCard";
import Course from "@/components/courses/Course";
export default {
  name: "AllRequestedCourses",
  components: { CollapseCard, Course },
  computed: {
    courses: function() {
      // let c = this.$store.state.courses.courses;
      // c.filter(c => {
      //   let d = new Date(c.date).getDate() + 86400;
      //   return d > new Date();
      // });
      // return c;
      return this.$store.state.courses.courses;
    },
    hasCourses: function() {
      return this.$store.state.courses.courses.length > 0;
    }
  }
};
</script>
