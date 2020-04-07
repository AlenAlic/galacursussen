<template>
  <div>
    <div class="left-align select">
      <select v-model="year" id="year">
        <option disabled value="">Choose your option</option>
        <option v-for="year in years" :key="year" :value="year">{{ year }} </option>
      </select>
      <label for="year">Year</label>
    </div>
    <div class="card" v-if="incie || mucie || $store.getters.currentUser.admin || $store.getters.currentUser.organizer">
      <div class="card-content">
        <h4>InCie</h4>
        <loading-spinner v-if="loading" />
        <courses-finances v-else :courses="incie_courses" />
      </div>
    </div>
    <div
      class="card"
      v-if="salcie || mucie || $store.getters.currentUser.admin || $store.getters.currentUser.organizer"
    >
      <div class="card-content">
        <h4>SalCie</h4>
        <loading-spinner v-if="loading" />
        <courses-finances v-else :courses="salcie_courses" />
      </div>
    </div>
  </div>
</template>

<script>
import Vue from "vue";
import { availableYears } from "@/assets/js/utilities";
import LoadingSpinner from "@/components/LoadingSpinner";
import { DateTime } from "luxon";
import { currencyFormat } from "@/assets/js/utilities";
import CoursesFinances from "@/components/CoursesFinances";
export default {
  name: "Finances",
  components: { CoursesFinances, LoadingSpinner },
  data: function() {
    return {
      year: null,
      courses: [],
      loading: true
    };
  },
  computed: {
    incie: function() {
      return this.$store.getters.profile && this.$store.getters.profile.incie;
    },
    salcie: function() {
      return this.$store.getters.profile && this.$store.getters.profile.salcie;
    },
    mucie: function() {
      return this.$store.getters.profile && this.$store.getters.profile.mucie;
    },
    years: function() {
      return availableYears();
    },
    incie_courses: function() {
      return this.courses.filter(c => c.committee_value === "incie");
    },
    incie_total: function() {
      return this.incie_courses.reduce((total, course) => {
        return total + course.price;
      }, 0);
    },
    salcie_courses: function() {
      return this.courses.filter(c => c.committee_value === "salcie");
    }
  },
  created() {
    this.getFinances(this.year);
  },
  mounted: function() {
    this.$nextTick(function() {
      // eslint-disable-next-line no-undef
      M.FormSelect.init(document.querySelectorAll("select"));
    });
  },
  watch: {
    year: function(newVal) {
      this.getFinances(newVal);
    }
  },
  methods: {
    getFinances: function(year) {
      this.loading = true;
      return Vue.axios
        .get(`courses/finances/${year ? year : ""}`)
        .then(res => {
          this.courses = res.data;
          this.loading = false;
        })
        .catch(() => {
          this.loading = false;
        });
    },
    getDateTime: function(date) {
      let datetime = DateTime.fromISO(date, { zone: "UTC" });
      return datetime.toFormat("dd-LL-kkkk (HH:mm)");
    },
    price: function(price) {
      return currencyFormat(price);
    }
  }
};
</script>

<style scoped lang="scss">
.card {
  &.limited {
    max-width: 90vw;
    width: 400px;
  }
}
.select {
  margin-top: 2rem;
}
.select-wrapper + label {
  position: relative;
  left: 0;
}
.strikethrough {
  text-decoration: line-through;
}
</style>
