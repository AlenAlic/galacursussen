<template>
  <collapse-card :title="title" :counter="courses.length" :loading="loading">
    <div>
      <div class="left-align">
        <select v-model="year" id="year">
          <option disabled value="">Choose your option</option>
          <option v-for="year in years" :key="year" :value="year"
            >{{ year }}
          </option>
        </select>
        <label for="year">Year</label>
      </div>
      <div v-if="!loading && courses.length > 0">
        <course
          v-for="course in courses"
          :key="course.key"
          :course="course"
          @closeModal="closeModal"
          class="mb"
        />
      </div>
      <h6 v-else-if="year !== '' && !loading">
        There are no courses for the selected year.
      </h6>
    </div>
  </collapse-card>
</template>

<script>
import Vue from "vue";
import CollapseCard from "@/components/CollapseCard";
import Course from "@/components/courses/Course";
import { availableYears } from "@/assets/js/utilities";
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
      return availableYears();
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
  methods: {
    closeModal: function() {
      this.updateCourses(this.year);
    },
    updateCourses: function(year) {
      this.loading = true;
      Vue.axios
        .get(`courses/${year}`)
        .then(res => {
          this.courses = Object.values(res.data);
          this.loading = false;
        })
        .catch(() => {
          this.loading = false;
        });
    }
  },
  watch: {
    year: function(newVal) {
      this.updateCourses(newVal);
    }
  }
};
</script>

<style scoped lang="scss">
.select-wrapper + label {
  position: relative;
  left: 0;
}
.mb {
  margin-bottom: 3rem;
}
</style>
