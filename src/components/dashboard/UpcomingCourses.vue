<template>
  <div class="not-responded-container">
    <div class="card-container" v-for="course in courses" :key="course.key">
      <div class="card">
        <upcoming-course class="card-content" :course="course" />
      </div>
    </div>
  </div>
</template>

<script>
import UpcomingCourse from "@/components/courses/UpcomingCourse";
import { DateTime } from "luxon";
export default {
  name: "UpcomingCourses",
  components: { UpcomingCourse },
  computed: {
    courses: function() {
      let courses = this.$store.getters.courses;
      return courses.filter(c => {
        return (
          DateTime.fromISO(c.date, { zone: "UTC" }) >
          DateTime.local().setZone("UTC")
        );
      });
    }
  }
};
</script>

<style scoped lang="scss">
.not-responded-container {
  margin-top: 1rem;
  display: flex;
  justify-content: space-evenly;
  flex-wrap: wrap;
  width: 100%;
}
.card-container {
  max-width: 320px;
  width: 100%;
  margin: 0.5rem;
}
</style>
