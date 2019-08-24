<template>
  <form v-on:submit.prevent class="center-align">
    <h4>{{ course.requested_by }}</h4>
    <h5>
      Currently assigned
      <span v-if="assigned.length > 0">({{ assigned.length }})</span>
    </h5>
    <div v-if="assigned.length > 0" class="assigned">
      <div
        v-for="assignment in assigned"
        :key="assignment.id"
        class="underline"
      >
        <div class="assign">
          <div class="left-align">
            <b>
              {{ assignment.name }}
              <font-awesome-icon v-if="assignment.mucie" icon="music" />
              ({{ assignment.hours }})
            </b>
            <br />
            <i v-if="assignment.notes">{{ assignment.notes }}</i>
          </div>
          <div>
            <button class="btn" @click.prevent="assign(assignment.id, false)">
              Remove
            </button>
          </div>
        </div>
        <div class="assign right-align" v-if="assignment.role">
          <div>
            {{ assignment.role }}
          </div>
          <div class="assign-buttons">
            <button class="btn" @click.prevent="setRole(assignment.id, null)">
              Clear role
            </button>
          </div>
        </div>
        <div class="assign" v-else>
          <div></div>
          <div
            class="assign-buttons"
            v-if="
              !(
                assignment.has_teacher &&
                assignment.has_assistant &&
                assignment.has_mucie
              )
            "
          >
            <button
              v-if="assignment.mucie"
              :disabled="assignment.has_mucie"
              class="btn"
              @click.prevent="setRole(assignment.id, 'mucie')"
            >
              MuCie
            </button>
            <button
              v-if="assignment.committee"
              :disabled="assignment.has_teacher"
              class="btn"
              @click.prevent="setRole(assignment.id, 'teacher')"
            >
              Teacher
            </button>
            <button
              v-if="assignment.committee"
              :disabled="assignment.has_assistant"
              class="btn"
              @click.prevent="setRole(assignment.id, 'assistant')"
            >
              Assistant
            </button>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="assigned">
      No one has been assigned yet.
    </div>
    <h5>Not assigned</h5>
    <div
      v-for="assignment in notAssigned"
      :key="assignment.id"
      class="underline"
    >
      <div class="assign">
        <div class="left-align">
          <b :class="attendanceClass(assignment)">
            {{ assignment.name }}
            <font-awesome-icon v-if="assignment.mucie" icon="music" />
            ({{ assignment.hours }})
          </b>
          <br />
          <i v-if="assignment.notes">{{ assignment.notes }}</i>
        </div>
        <div>
          <button class="btn" @click.prevent="assign(assignment.id, true)">
            Assign
          </button>
        </div>
      </div>
    </div>
    <button class="btn cancel exit" @click.prevent="exit">
      Exit
    </button>
  </form>
</template>

<script>
import { UPDATE_COURSE } from "@/store/modules/courses";
import Vue from "vue";
export default {
  name: "AssignCourseForm",
  props: { courseData: Object },
  data: function() {
    return {
      course: this.courseData,
      errors: {}
    };
  },
  computed: {
    roles: function() {
      return this.$store.getters.roles;
    },
    assigned: function() {
      return this.course.assignments.filter(a => {
        return a.assigned;
      });
    },
    notAssigned: function() {
      return this.course.assignments.filter(a => {
        return !a.assigned;
      });
    },
    yes: function() {
      return this.notAssigned.filter(r => {
        return r.attendance === "yes";
      });
    },
    maybe: function() {
      return this.notAssigned.filter(r => {
        return r.attendance === "maybe";
      });
    },
    no: function() {
      return this.notAssigned.filter(r => {
        return r.attendance === "no";
      });
    },
    responded: function() {
      return []
        .concat(...this.yes)
        .concat(...this.maybe)
        .concat(...this.no);
    }
  },
  methods: {
    radioName: function(id) {
      return `assigment-${id}`;
    },
    attendanceClass: function(assignment) {
      return {
        "grey-text": !assignment.attendance,
        "text-success": assignment.attendance === "yes",
        "text-super-success": assignment.attendance === "preference",
        "text-warning": assignment.attendance === "maybe",
        "text-danger": assignment.attendance === "no"
      };
    },
    assign: function(assignment, assigned) {
      Vue.axios
        .patch(`courses/assign/${assignment}`, {
          assigned: assigned
        })
        .then(res => {
          this.$notify(res.data.message, "success");
          this.course = res.data.course;
        })
        .catch(({ errors }) => {
          this.errors = errors;
        });
    },
    setRole: function(assignment, role) {
      Vue.axios
        .patch(`courses/role/${assignment}`, {
          role: role
        })
        .then(res => {
          this.$notify(res.data.message, "success");
          this.course = res.data.course;
        })
        .catch(({ errors }) => {
          this.errors = errors;
        });
    },
    exit: function() {
      let id = this.course.id;
      this.$store.dispatch(UPDATE_COURSE, { id });
      this.$emit("close");
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
.assigned {
  margin-bottom: 1rem;
}
.assign {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  margin: 0.25rem 0;
}
.assign-buttons {
  padding-top: 0.25rem;
  button {
    margin-left: 1rem;
  }
}
.underline {
  border-bottom: 1px solid lightgrey;
}
.exit {
  margin-top: 1.5rem;
}
</style>
