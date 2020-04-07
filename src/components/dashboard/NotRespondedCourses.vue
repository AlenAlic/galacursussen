<template>
  <div>
    <div v-if="this.$store.state.courses.loading" class="spinner-container">
      <loading-spinner />
    </div>
    <div v-else>
      <not-responded-card v-for="course in courses" :key="course.id" :course="course"></not-responded-card>
    </div>
  </div>
</template>

<script>
import NotRespondedCard from "@/components/courses/NotRespondedCard";
import LoadingSpinner from "@/components/LoadingSpinner";
export default {
  name: "NotRespondedCourses",
  components: { LoadingSpinner, NotRespondedCard },
  computed: {
    courses: function() {
      let courses = this.$store.getters.courses;
      if (courses.length > 0) {
        courses = courses.filter(c => {
          return !c.cancelled;
        });
        courses = courses.filter(c => {
          let d = new Date(c.date);
          return d > new Date();
        });
        courses = courses.filter(c => {
          return c.assignments.some(a => a.user_id === this.$store.getters.currentUser.id && !a.attendance);
        });
      }
      return courses;
    },
    hasCourses: function() {
      return this.courses.length > 0;
    }
  }
};
</script>

<style scoped lang="scss">
.spinner-container {
  display: flex;
  justify-content: center;
  width: 100%;
  padding: 2rem 0;
}
</style>
