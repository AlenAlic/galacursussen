<template>
  <collapse-card
    title="This years courses/workshops"
    :loading="this.$store.state.courses.loading"
    :counter="courses.length"
  >
    <div v-if="courses.length > 0">
      <course v-for="course in courses" :key="course.key" :course="course" @closeModal="closeModal" class="mb" />
    </div>
    <h6 v-else-if="!this.$store.state.courses.loading">
      There are no courses for this year yet.
    </h6>
  </collapse-card>
</template>

<script>
import { COURSES } from "./../../store/modules/courses";
import CollapseCard from "@/components/CollapseCard";
import Course from "@/components/courses/Course";
export default {
  name: "ThisAcademicYearsCourses",
  components: { CollapseCard, Course },
  computed: {
    courses: function() {
      return this.$store.getters.courses;
    }
  },
  methods: {
    closeModal: function() {
      this.$store.dispatch(COURSES);
    }
  }
};
</script>

<style scoped lang="scss">
.mb {
  margin-bottom: 3rem;
}
</style>
