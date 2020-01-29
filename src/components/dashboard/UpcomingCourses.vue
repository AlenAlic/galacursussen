<template>
  <div class="not-responded-container" v-if="courses.length > 0">
    <div class="card-container" v-for="course in courses" :key="course.key">
      <div class="card">
        <upcoming-course class="card-content" :course="course" />
      </div>
    </div>
  </div>
  <h4 v-else-if="!this.$store.state.courses.loading">
    There are no upcoming courses.
  </h4>
</template>

<script>
import UpcomingCourse from "@/components/courses/UpcomingCourse";
import { DateTime } from "luxon";
import { filterCoursesByCommittee } from "@/assets/js/utilities";
export default {
  name: "UpcomingCourses",
  components: { UpcomingCourse },
  computed: {
    courses: function() {
      let courses = this.$store.getters.courses;
      courses = courses.filter(c => {
        return filterCoursesByCommittee(c, this.$store.getters.currentUser);
      });
      return courses.filter(c => {
        let courseDate = DateTime.fromISO(c.date, { zone: "UTC" });
        let today = DateTime.local()
          .setZone("UTC")
          .set({ hour: 0, minute: 0, second: 0, millisecond: 0 });
        return courseDate > today;
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
