<template>
  <div>
    <h4 v-if="notPaidCourses.length > 0">Require payment</h4>
    <div class="not-responded-container">
      <div class="card-container" v-for="course in notPaidCourses" :key="course.key">
        <div class="card">
          <treasurer-course class="card-content" :course="course" />
        </div>
      </div>
    </div>
    <h4 v-if="paidCourses.length > 0">Paid courses</h4>
    <div class="not-responded-container">
      <div class="card-container" v-for="course in paidCourses" :key="course.key">
        <div class="card">
          <treasurer-course class="card-content" :course="course" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { DateTime } from "luxon";
import TreasurerCourse from "@/components/courses/TreasurerCourse";
export default {
  name: "TreasurerCourses",
  components: { TreasurerCourse },
  computed: {
    courses: function() {
      let courses = this.$store.getters.courses;
      return courses.filter(
        c =>
          (DateTime.fromISO(c.date, { zone: "UTC" }) < DateTime.local().setZone("UTC") &&
            !c.cancelled) ||
          (c.cancelled && c.price)
      );
    },
    paidCourses: function() {
      return this.courses.filter(c => {
        return c.paid;
      });
    },
    notPaidCourses: function() {
      return this.courses.filter(c => {
        return !c.paid;
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
