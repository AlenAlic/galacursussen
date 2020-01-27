<template>
  <form v-on:submit.prevent class="center-align">
    <div class="input-field">
      <font-awesome-icon class="prefix" :icon="['far', 'building']"></font-awesome-icon>
      <input v-model="requested_by" type="text" id="requested_by" />
      <label for="requested_by" :class="{ active: requested_by }">Requested by</label>
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
      <label for="location" :class="{ active: location }">Location</label>
    </div>
    <div class="input-field">
      <font-awesome-icon class="prefix" :icon="['far', 'clipboard']"></font-awesome-icon>
      <input v-model="dances" type="text" id="dances" />
      <label for="dances" :class="{ active: dances }">Dances</label>
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
      <input v-model="notes" type="text" :id="`notes-${course.id}-edit`" />
      <label :for="`notes-${course.id}-edit`" :class="{ active: notes }">Notes</label>
    </div>
    <div class="row no-padd no-marg-bottom">
      <div class="col s4">
        <div class="input-field">
          <font-awesome-icon class="prefix" icon="hashtag"></font-awesome-icon>
          <input v-model="attendees" type="number" id="attendees" min="0" step="1" />
          <label for="attendees" :class="{ active: attendees }">Attendees</label>
        </div>
      </div>
      <div class="col s4">
        <div class="input-field">
          <font-awesome-icon class="prefix" icon="euro-sign"></font-awesome-icon>
          <input v-model="price" type="number" id="price" min="0" step="0.01" />
          <label for="price" :class="{ active: price }">Price</label>
        </div>
      </div>
      <div class="col s4 paid-checkbox">
        <label for="paid">
          <input type="checkbox" id="paid" v-model="paid" />
          <span>Paid</span>
        </label>
      </div>
    </div>
    <div class="buttons-container">
      <button slot="button" class="btn" @click.prevent="patchCourse">
        Save <loading-spinner size="spinner-btn" v-if="loading" />
      </button>
      <button class="btn cancel" @click.prevent="$emit('cancel')">
        Cancel
      </button>
    </div>
    <h4>Attendance</h4>
    <div v-for="request in course.assignments" :key="request.id">
      <div>
        <div>
          <b>
            {{ request.name }}
            <font-awesome-icon v-if="request.mucie" icon="music" />
          </b>
        </div>
        <div>
          <div v-if="request.notes">
            <i>{{ request.notes }}</i>
          </div>
        </div>
        <div>
          <div class="radios">
            <label>
              <input
                value="yes"
                :name="radioName(request.id)"
                type="radio"
                @click="addAttendance(request.id, 'yes')"
                :checked="request.attendance === 'yes'"
              />
              <span>Yes</span>
            </label>
            <label>
              <input
                value="maybe"
                :name="radioName(request.id)"
                type="radio"
                @click="addAttendance(request.id, 'maybe')"
                :checked="request.attendance === 'maybe'"
              />
              <span>Maybe</span>
            </label>
            <label>
              <input
                value="no"
                :name="radioName(request.id)"
                type="radio"
                @click="addAttendance(request.id, 'no')"
                :checked="request.attendance === 'no'"
              />
              <span>No</span>
            </label>
            <label>
              <input
                :value="null"
                :name="radioName(request.id)"
                type="radio"
                @click="addAttendance(request.id, null)"
                :checked="request.attendance === null"
              />
              <span>Not responded</span>
            </label>
          </div>
        </div>
      </div>
    </div>
  </form>
</template>

<script>
// import { UPDATE_COURSE } from "@/store/modules/courses";
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
      assignments: {},
      attendees: course.attendees,
      price: course.price,
      paid: course.paid,
      loading: false,
      errors: {}
    };
  },
  computed: {
    filled: function() {
      return this.requested_by !== "";
    }
  },
  methods: {
    addAttendance: function(id, assignment) {
      this.assignments[id] = assignment;
    },
    radioName: function(id) {
      return `assigment-${id}`;
    },
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
          dances: this.dances,
          attendees: this.attendees,
          price: this.price,
          paid: this.paid,
          assignments: this.assignments
        })
        .then(() => {
          this.$notify(`Saved changes for ${this.course.requested_by}.`, "success");
          this.$emit("close");
        })
        .catch(({ errors }) => {
          this.loading = false;
          this.$notify(errors[0], "error");
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
    margin: 1rem 0.5rem 1.5rem 0.5rem;
  }
}
.paid-checkbox {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 84px;
}
</style>
