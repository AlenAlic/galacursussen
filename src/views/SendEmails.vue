<template>
  <div class="row">
    <div class="col m6">
      <div class="card">
        <div class="card-content">
          <span class="card-title">Availability reminder</span>
          <loading-spinner v-if="loadingAvailability" size="small" />
          <div v-else-if="availabilityUsers.length > 0">
            <p>
              Send a reminder email to the users (listed below) that have not
              yet indicated their availability for the upcoming courses.
            </p>
            <save-button
              class="card-button"
              @click.native="sendAvailabilityEmail"
              :loading="sendingAvailabilityEmail"
              :active="!sentAvailabilityEmail"
              text="Send email"
            />
            <p v-for="user in availabilityUsers" :key="user">
              {{ user }}
            </p>
          </div>
          <p v-else>
            Everyone has filled in their availability for the upcoming courses
            :)
          </p>
        </div>
      </div>
    </div>
    <div class="col m6">
      <div class="card">
        <div class="card-content">
          <span class="card-title">Assignment overview</span>
          <loading-spinner v-if="loadingAssignments" size="small" />
          <div v-else-if="courses.length > 0">
            <p>
              Send an email to everyone with the current assignment for the
              upcoming courses.
            </p>
            <save-button
              class="card-button center-align"
              @click.native="sendAssignmentsEmail"
              :loading="sendingAssignmentsEmail"
              :active="!sentAssignmentsEmail && courses.length > 0"
              text="Send email"
            />
            <div class="left-align">
              <h5 class="title">InCie</h5>
              <div
                v-for="course in incie"
                :key="course.key"
                class="assigned-course"
              >
                <div>
                  <b>{{ course.date_formatted }}</b>
                </div>
                <div>
                  <i>{{ course.requested_by }}</i>
                </div>
                <div>Location: {{ course.location }}</div>
                <div>Assigned:</div>
                <div
                  v-for="assignment in getAssignedUsers(course)"
                  :key="assignment.id"
                >
                  {{ assignment.name }}
                  <i class="pl" v-show="assignment.role">{{
                    assignment.role
                  }}</i>
                </div>
                <div>Course language: {{ course.language }}</div>
                <div>Dances: {{ course.dances }}</div>
                <div>Notes: {{ course.notes }}</div>
              </div>
              <h5 class="title">SalCie</h5>
              <div
                v-for="course in salcie"
                :key="course.key"
                class="assigned-course"
              >
                <div>
                  <b>{{ course.date_formatted }}</b>
                </div>
                <div>
                  <i>{{ course.requested_by }}</i>
                </div>
                <div>Location: {{ course.location }}</div>
                <div>Assigned:</div>
                <div
                  v-for="assignment in getAssignedUsers(course)"
                  :key="assignment.id"
                >
                  {{ assignment.name }}
                  <i class="pl" v-show="assignment.role">{{
                    assignment.role
                  }}</i>
                </div>
                <div>Course language: {{ course.language }}</div>
                <div>Dances: {{ course.dances }}</div>
                <div>Notes: {{ course.notes }}</div>
              </div>
            </div>
          </div>
          <div v-else>There are no upcoming course.</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { COURSES } from "@/store/modules/courses";
import Vue from "vue";
import LoadingSpinner from "@/components/LoadingSpinner";
import { DateTime } from "luxon";
import SaveButton from "@/components/SaveButton";
export default {
  name: "SendEmails",
  components: { SaveButton, LoadingSpinner },
  data: function() {
    return {
      loadingAvailability: true,
      availabilityUsers: [],
      sendingAvailabilityEmail: false,
      sentAvailabilityEmail: false,
      loadingAssignments: true,
      assignmentCourses: [],
      sendingAssignmentsEmail: false,
      sentAssignmentsEmail: false
    };
  },
  created() {
    if (!this.$store.getters.hasCourses) {
      this.$store.dispatch(COURSES).then(() => {
        this.loadingAssignments = false;
      });
    } else {
      this.loadingAssignments = false;
    }
    this.getNotification();
  },
  computed: {
    courses: function() {
      let courses = this.$store.getters.courses;
      courses = courses.filter(c => {
        return !c.cancelled;
      });
      return courses.filter(c => {
        return (
          DateTime.fromISO(c.date, { zone: "UTC" }) >
          DateTime.local().setZone("UTC")
        );
      });
    },
    incie: function() {
      return this.courses.filter(c => {
        return c.committee_value === "incie";
      });
    },
    salcie: function() {
      return this.courses.filter(c => {
        return c.committee_value === "salcie";
      });
    }
  },
  methods: {
    getNotification: function() {
      return Vue.axios
        .get("courses/notification")
        .then(res => {
          this.availabilityUsers = res.data;
          this.loadingAvailability = false;
        })
        .catch(({ errors }) => {
          this.$notify(errors[0], "error");
          this.loadingAvailability = false;
        });
    },
    sendAvailabilityEmail: function() {
      this.sendingAvailabilityEmail = true;
      return Vue.axios
        .post("courses/notification")
        .then(() => {
          this.$notify("Emails have been sent.", "success");
          this.sendingAvailabilityEmail = false;
          this.sentAvailabilityEmail = true;
        })
        .catch(({ errors }) => {
          this.$notify(errors[0], "error");
          this.sendingAvailabilityEmail = false;
        });
    },
    sendAssignmentsEmail: function() {
      this.sendingAssignmentsEmail = true;
      return Vue.axios
        .post("courses/assignments")
        .then(res => {
          console.log(res);
          this.$notify("Emails have been sent.", "success");
          this.sendingAssignmentsEmail = false;
          this.sentAssignmentsEmail = true;
        })
        .catch(({ errors }) => {
          this.$notify(errors[0], "error");
          this.sendingAssignmentsEmail = false;
        });
    },
    getAssignedUsers: function(course) {
      return course.assignments.filter(r => {
        return r.assigned;
      });
    }
  }
};
</script>

<style scoped lang="scss">
.col {
  width: 100%;
}
.card-button {
  margin: 1rem 0;
}
.assigned-course {
  margin-bottom: 1rem !important;
}
.title {
  margin-top: 1.5rem !important;
}
</style>
