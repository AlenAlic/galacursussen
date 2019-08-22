<template>
  <collapse-card :title="title" :counter="courses.length" :loading="loading">
    <div>
      <div class="left-align">
        <select v-model="year" id="year">
          <option disabled value="">Choose your option</option>
          <option v-for="year in years" :key="year" :value="year">{{
            year
          }}</option>
        </select>
        <label for="year">Year</label>
      </div>
      <course v-for="course in courses" :key="course.key" :course="course" />
    </div>
  </collapse-card>
</template>

<script>
import Vue from "vue";
import CollapseCard from "@/components/CollapseCard";
import Course from "@/components/courses/Course";
export default {
  name: "PreviousYearsCourses",
  components: { CollapseCard, Course },
  data: function() {
    return {
      courses: [],
      year: "",
      loading: false
    };
  },
  computed: {
    years: function() {
      const YEAR = 2018;
      const range = n => [...Array(n).keys()];
      let now = new Date().getFullYear();
      return range(now - YEAR).map(r => r + YEAR);
    },
    title: function() {
      let academicYear = this.year
        ? `${this.year} - ${Number(this.year) + 1}`
        : "...";
      return `Courses from the academic year   ${academicYear}`;
    }
  },
  mounted: function() {
    this.$nextTick(function() {
      // eslint-disable-next-line no-undef
      M.FormSelect.init(document.querySelectorAll("select"));
    });
  },
  watch: {
    year: function(newVal) {
      this.loading = true;
      Vue.axios
        .get(`courses/${newVal}`)
        .then(res => {
          this.courses = res.data;
          this.loading = false;
        })
        .catch(({ errors }) => {
          this.errors = errors;
          this.loading = false;
        });
    }
  }
};
</script>

<style scoped lang="scss">
.select-wrapper + label {
  position: relative;
  top: -65px;
  left: 0;
  font-size: 0.8rem;
}
</style>
