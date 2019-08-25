<template>
  <div>
    <div class="left-align select">
      <select v-model="year" id="year">
        <option disabled value="">Choose your option</option>
        <option v-for="year in years" :key="year" :value="year"
          >{{ year }}
        </option>
      </select>
      <label for="year">Year</label>
    </div>
    <div class="hours-container">
      <div>
        <personal-hours-card
          v-if="incie"
          committee="InCie"
          :hours="incie"
          :loading="loading"
        />
      </div>
      <div>
        <personal-hours-card
          v-if="salcie"
          committee="Salcie"
          :hours="salcie"
          :loading="loading"
        />
      </div>
      <div>
        <personal-hours-card
          v-if="mucie"
          committee="Mucie"
          :hours="mucie"
          :loading="loading"
        />
      </div>
    </div>
    <div class="card">
      <div class="card-content">
        <h4>Total hours</h4>
        <loading-spinner v-if="totalLoading" />
        <table class="left-align" v-else>
          <thead>
            <tr>
              <th>Name</th>
              <th>InCie</th>
              <th>SalCie</th>
              <th>MuCie</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(hours, index) in total_hours" :key="index">
              <td>{{ hours.user }}</td>
              <td>{{ hours.hours.incie }}</td>
              <td>{{ hours.hours.salcie }}</td>
              <td>{{ hours.hours.mucie }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import Vue from "vue";
import PersonalHoursCard from "@/components/profile/PersonalHoursCard";
import { availableYears } from "@/assets/js/utilities";
import LoadingSpinner from "@/components/LoadingSpinner";
export default {
  name: "Hours",
  components: { LoadingSpinner, PersonalHoursCard },
  data: function() {
    return {
      hours: undefined,
      year: new Date().getFullYear(),
      total_hours: undefined,
      loading: true,
      totalLoading: true
    };
  },
  computed: {
    incie: function() {
      return this.hours
        ? this.hours.incie
          ? this.hours.incie
          : undefined
        : undefined;
    },
    salcie: function() {
      return this.hours
        ? this.hours.salcie
          ? this.hours.salcie
          : undefined
        : undefined;
    },
    mucie: function() {
      return this.hours
        ? this.hours.mucie
          ? this.hours.mucie
          : undefined
        : undefined;
    },
    years: function() {
      return availableYears();
    }
  },
  created() {
    this.getHours(this.year);
    this.getTotalHours(this.year);
  },
  mounted: function() {
    this.$nextTick(function() {
      // eslint-disable-next-line no-undef
      M.FormSelect.init(document.querySelectorAll("select"));
    });
  },
  watch: {
    year: function(newVal) {
      this.getHours(newVal);
      this.getTotalHours(newVal);
    }
  },
  methods: {
    getHours: function(year) {
      this.loading = true;
      return Vue.axios
        .get(`courses/hours/${year}`)
        .then(res => {
          this.hours = res.data;
          this.loading = false;
        })
        .catch(({ errors }) => {
          this.loading = false;
          this.errors = errors;
        });
    },
    getTotalHours: function(year) {
      this.totalLoading = true;
      return Vue.axios
        .get(`courses/total_hours/${year}`)
        .then(res => {
          this.total_hours = res.data;
          this.totalLoading = false;
        })
        .catch(({ errors }) => {
          this.totalLoading = false;
          this.errors = errors;
        });
    }
  }
};
</script>

<style scoped lang="scss">
.hours-container {
  display: flex;
  justify-content: space-around;
  width: 100%;
  flex-wrap: wrap;
}
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
</style>
