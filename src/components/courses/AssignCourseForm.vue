<template>
  <form class="center-align">
    <h4>{{ course.requested_by }}</h4>
    <h5>Currently assigned</h5>
    <div v-if="assigned.length > 0" class="assigned">
      <div
        class="assignment-request"
        v-for="assignment in assigned"
        :key="assignment.id"
      >
        <div class="assign">
          <div class="left-align">
            <b>
              {{ assignment.name }}
              <font-awesome-icon v-if="assignment.mucie" icon="music" />
            </b>
            <br />
            <i v-if="assignment.notes">{{ assignment.notes }}</i>
          </div>
          <div>
            <button class="btn" @click.prevent="remove(assignment.id)">
              Remove
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
      class="assignment-request"
      v-for="request in notAssigned"
      :key="request.id"
    >
      <div class="assign">
        <div class="left-align">
          <b :class="attendanceClass(request)">
            {{ request.name }}
            <font-awesome-icon v-if="request.mucie" icon="music" />
          </b>
          <br />
          <i v-if="request.notes">{{ request.notes }}</i>
        </div>
        <div>
          <button class="btn" @click.prevent="assign(request.user_id, null)">
            Assign
          </button>
        </div>
      </div>
    </div>
    <button class="btn cancel exit" @click.prevent="$emit('close')">
      Exit
    </button>
    <loading-spinner size="spinner-btn" v-if="false" />
  </form>
</template>

<script>
// import { UPDATE_COURSE } from "@/store/modules/courses";
import Vue from "vue";
import LoadingSpinner from "@/components/LoadingSpinner";
export default {
  name: "AssignCourseForm",
  components: { LoadingSpinner },
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
        .push(...this.yes)
        .push(...this.maybe)
        .push(...this.no);
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
    assign: function(user_id, role) {
      let id = this.course.id;
      Vue.axios
        .post(`courses/${id}/assign`, {
          user_id: user_id,
          role: role
        })
        .then(res => {
          this.$notify(res.data.message, "success");
          this.course = res.data.course;
          // this.$store.dispatch(UPDATE_COURSE, { id });
        })
        .catch(({ errors }) => {
          this.errors = errors;
        });
    },
    remove: function(assignment_id) {
      Vue.axios
        .delete(`courses/assignment/remove/${assignment_id}`)
        .then(res => {
          this.$notify(res.data.message, "success");
          this.course = res.data.course;
          // this.$store.dispatch(UPDATE_COURSE, { id });
        })
        .catch(({ errors }) => {
          this.errors = errors;
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
.assigned {
  margin-bottom: 1rem;
}
.assign {
  display: flex;
  justify-content: space-between;
  align-content: center;
  width: 100%;
  padding: 0.4rem 0;
  border-bottom: 1px solid lightgrey;
}
.exit {
  margin-top: 1.5rem;
}
</style>
