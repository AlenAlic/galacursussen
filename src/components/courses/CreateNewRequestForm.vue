<template>
  <form v-on:submit.prevent>
    <div class="input-field">
      <font-awesome-icon class="prefix" :icon="['far', 'building']"></font-awesome-icon>
      <input v-model="requested_by" type="text" id="requested_by" />
      <label for="requested_by">Requested by</label>
    </div>
    <div class="row no-padd no-marg-bottom">
      <div class="col s12 m6">
        <div class="input-field datetime-fix" :class="{ incorrect: this.errors.date }">
          <font-awesome-icon class="prefix" :icon="['far', 'calendar-alt']"></font-awesome-icon>
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
            :minute-step="5"
            zone="UTC"
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
          <font-awesome-icon class="prefix" :icon="['far', 'clock']"></font-awesome-icon>
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
      <font-awesome-icon class="prefix" :icon="['far', 'compass']"></font-awesome-icon>
      <input v-model="location" type="text" id="location" />
      <label for="location">Location</label>
    </div>
    <div class="input-field">
      <font-awesome-icon class="prefix" :icon="['far', 'clipboard']"></font-awesome-icon>
      <input v-model="dances" type="text" id="dances" />
      <label for="dances">Dances</label>
    </div>
    <div class="radios">
      <div class="radio-title">Course language</div>
      <label>
        <input v-model="language" value="nl" name="language" type="radio" />
        <span>Dutch</span>
      </label>
      <label>
        <input v-model="language" value="en" name="language" type="radio" />
        <span>English</span>
      </label>
      <label>
        <input v-model="language" value="unknown" name="language" type="radio" />
        <span>Unknown</span>
      </label>
    </div>
    <div class="radios">
      <div class="radio-title">What committee is the course for?</div>
      <label>
        <input v-model="committee" value="incie" name="committee" type="radio" />
        <span>InCie</span>
      </label>
      <label>
        <input v-model="committee" value="salcie" name="committee" type="radio" />
        <span>SalCie</span>
      </label>
    </div>
    <div class="input-field">
      <font-awesome-icon class="prefix" :icon="['far', 'clipboard']"></font-awesome-icon>
      <input v-model="notes" type="text" id="notes" />
      <label for="notes">Notes</label>
    </div>
    <button
      @click.prevent="newCourse"
      :disabled="filled !== true"
      class="waves-effect waves-light btn"
      :class="{ 'no-click': !filled }"
    >
      Add course
    </button>
  </form>
</template>

<script>
import Vue from "vue";
import { COURSES } from "./../../store/modules/courses";
import { DateTime } from "luxon";
import { Datetime } from "vue-datetime";
export default {
  name: "CreateNewRequestForm",
  components: { Datetime },
  data: function() {
    return {
      requested_by: "",
      date: "",
      duration: DateTime.fromISO("1970-01-01T01:30:00.000Z").toISO(),
      location: "",
      notes: "",
      language: "",
      committee: "",
      dances: "",
      errors: {}
    };
  },
  computed: {
    filled: function() {
      return this.requested_by !== "" && this.committee !== "" && this.language !== "";
    }
  },
  methods: {
    newCourse: function() {
      Vue.axios
        .post("courses/new", {
          requested_by: this.requested_by,
          date: this.date,
          duration: this.duration,
          location: this.location,
          notes: this.notes,
          language: this.language ? this.language : "unknown",
          committee: this.committee,
          dances: this.dances
        })
        .then(() => {
          this.$notify(`Added course for ${this.requested_by}..`, "success");
          this.$store.dispatch(COURSES);
          this.requested_by = "";
          this.date = "";
          this.duration = DateTime.fromISO("1970-01-01T01:30:00.000Z").toISO();
          this.location = "";
          this.notes = "";
          this.language = "";
          this.committee = "";
          this.dances = "";
          this.errors = {};
        })
        .catch(({ errors }) => {
          this.errors = errors;
        });
    }
  },
  watch: {
    date: function() {
      if (this.errors.date) delete this.errors.date;
    }
  }
};
</script>

<style scoped lang="scss">
@import "../../assets/css/config";
.radios {
  /*padding-left: 45px;*/
  /*text-align: left;*/
  margin: 1rem 0;
  label {
    padding-right: 16px;
  }
  .radio-title {
    font-size: 0.8rem;
    color: #9e9e9e;
  }
}
</style>
