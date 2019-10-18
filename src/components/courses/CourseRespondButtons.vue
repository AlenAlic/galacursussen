<template>
  <card-collapse-list title="Update course attendance" :bold="false">
    <div class="card-action">
      <form v-on:submit.prevent>
        <div>
          <div class="input-field" :class="{ 'datetime-fix': !!notes }">
            <font-awesome-icon
              class="prefix"
              :icon="['far', 'clipboard']"
            ></font-awesome-icon>
            <input v-model="notes" type="text" id="notes" :disabled="loading" />
            <label for="notes">Notes</label>
          </div>
          <div v-if="loading" class="buttons-container">
            <loading-spinner class="spinner" size="small" />
          </div>
          <div v-else class="buttons-container">
            <button class="btn success" @click="attend('yes')">
              Yes
            </button>
            <button class="btn warning" @click="attend('maybe')">
              Maybe
            </button>
            <button class="btn danger" @click="attend('no')">
              No
            </button>
          </div>
        </div>
      </form>
    </div>
  </card-collapse-list>
</template>

<script>
import { UPDATE_COURSE } from "@/store/modules/courses";
import Vue from "vue";
import LoadingSpinner from "@/components/LoadingSpinner";
import CardCollapseList from "@/components/courses/CardCollapseList";
export default {
  name: "CourseRespondButtons",
  props: { course: Object, assignment: Object },
  components: {
    CardCollapseList,
    LoadingSpinner
  },
  data: function() {
    return {
      notes: this.assignment.notes,
      loading: false,
      hide: false,
      height: undefined
    };
  },
  methods: {
    attend: function(attendance) {
      this.loading = true;
      Vue.axios
        .patch("courses/attend", {
          user_id: this.$store.getters.currentUser.id,
          course_id: this.course.id,
          attendance: attendance,
          notes: this.notes
        })
        .then(() => {
          this.$notify(
            `Attendance updated for ${this.course.requested_by}.`,
            "success"
          );
          let id = this.course.id;
          this.$store.dispatch(UPDATE_COURSE, { id });
        })
        .catch(({ errors }) => {
          this.$notify(errors, "error");
          this.loading = false;
        });
    }
  }
};
</script>

<style scoped lang="scss">
.card-action {
  text-align: center;
  padding: 0;
  .can {
    margin-bottom: 1rem;
  }
  .btn {
    margin: 0 0.5rem;
  }
  .buttons-container {
    min-height: 45px;
  }
}
</style>
