<template>
  <form class="center-align">
    <div class="input-field">
      <font-awesome-icon
        class="prefix"
        :icon="['far', 'building']"
      ></font-awesome-icon>
      <input v-model="requested_by" type="text" id="requested_by" />
      <label for="requested_by" :class="{ active: requested_by }"
        >Requested by</label
      >
    </div>
    <div class="row no-padd no-marg-bottom">
      <div class="col s12 m6">
        <div
          class="input-field datetime-fix"
          :class="{ incorrect: this.errors.date }"
        >
          <font-awesome-icon
            class="prefix"
            :icon="['far', 'calendar-alt']"
          ></font-awesome-icon>
          <datetime
            input-id="date"
            class="input-field"
            type="datetime"
            v-model="date"
            :format="{
              year: 'numeric',
              month: 'long',
              day: 'numeric',
              hour: 'numeric',
              minute: '2-digit'
            }"
            zone="UTC"
            :minute-step="5"
            auto
          >
            <!--suppress XmlInvalidId -->
            <label for="date" class="active" slot="before">
              Date and start time
            </label>
          </datetime>
        </div>
      </div>
      <div class="col s12 m6">
        <div class="input-field">
          <font-awesome-icon
            class="prefix"
            :icon="['far', 'clock']"
          ></font-awesome-icon>
          <datetime
            input-id="duration"
            class="input-field"
            type="time"
            v-model="duration"
            :minute-step="5"
            zone="UTC"
          >
            <!--suppress XmlInvalidId -->
            <label for="duration" class="active" slot="before">
              Course duration
            </label>
          </datetime>
        </div>
      </div>
    </div>
    <div class="input-field">
      <font-awesome-icon
        class="prefix"
        :icon="['far', 'compass']"
      ></font-awesome-icon>
      <input v-model="location" type="text" id="location" />
      <label for="location" :class="{ active: location }">Location</label>
    </div>
    <div class="input-field">
      <font-awesome-icon
        class="prefix"
        :icon="['far', 'clipboard']"
      ></font-awesome-icon>
      <input v-model="dances" type="text" id="dances" />
      <label for="dances" :class="{ active: dances }">Dances</label>
    </div>
    <div class="radios">
      <div class="radio-title">Course language</div>
      <label v-for="opt in languages" :key="opt.value">
        <input
          v-model="language"
          :value="opt.value"
          name="language"
          type="radio"
        />
        <span>{{ opt.text }}</span>
      </label>
    </div>
    <div class="radios">
      <div class="radio-title">What committee is the course for?</div>
      <label v-for="opt in committees" :key="opt.value">
        <input
          v-model="committee"
          :value="opt.value"
          name="committees"
          type="radio"
        />
        <span>{{ opt.text }}</span>
      </label>
    </div>
    <div class="input-field">
      <font-awesome-icon
        class="prefix"
        :icon="['far', 'clipboard']"
      ></font-awesome-icon>
      <input v-model="notes" type="text" id="notes" />
      <label for="notes" :class="{ active: notes }">Notes</label>
    </div>
    <loading-spinner size="small" v-if="loading" />
    <div class="buttons-container" v-else>
      <button slot="button" class="btn" @click.prevent="patchCourse">
        Save
      </button>
      <button class="btn grey accent-2" @click.prevent="$emit('close')">
        Cancel
      </button>
    </div>
  </form>
</template>

<script>
import Vue from "vue";
import { DateTime } from "luxon";
import { Datetime } from "vue-datetime";
import LoadingSpinner from "@/components/LoadingSpinner";
export default {
  name: "EditCourseForm",
  components: { LoadingSpinner, Datetime },
  props: { course: Object },
  data: function() {
    let course = this.course;
    return {
      requested_by: course.requested_by,
      date: DateTime.fromISO(course.date)
        .setLocale("UTC")
        .toISO(),
      duration: course.duration,
      location: course.location,
      notes: course.notes,
      language: course.language_value,
      committee: course.committee_value,
      dances: course.dances,
      loading: false,
      errors: {}
    };
  },
  computed: {
    languages: function() {
      return this.$store.getters.languages;
    },
    committees: function() {
      return this.$store.getters.committees;
    },
    filled: function() {
      return this.requested_by !== "";
    }
  },
  methods: {
    patchCourse: function() {
      let id = this.course.id;
      this.loading = true;
      Vue.axios
        .patch(`courses/updated/${id}`, {
          requested_by: this.requested_by,
          date: this.date,
          duration: this.duration,
          location: this.location,
          notes: this.notes,
          language: this.language,
          committee: this.committee,
          dances: this.dances
        })
        .then(res => {
          this.$notify(res.data, "success");
          this.$emit("close");
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
@import "../../assets/css/config";
.radios {
  margin: 1rem 0;
  label {
    padding-right: 16px;
  }
  .radio-title {
    font-size: 0.8rem;
    color: #9e9e9e;
  }
}
.buttons-container {
  button {
    margin: 1rem 0.5rem 0 0.5rem;
  }
}
</style>
