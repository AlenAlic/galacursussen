<template>
  <div class="cards-container trans-opacity" :class="{ fade: this.hide }">
    <div class="card">
      <div class="card-content">
        <span class="card-title">{{ course.requested_by }}</span>
        <div>{{ course.date_formatted }}</div>
        <div class="data-container">
          <div class="data left-align">
            <div class="text-container">
              <div class="icon">
                <font-awesome-icon icon="map-marker-alt" size="lg" />
              </div>
              <div class="text">{{ course.location }}</div>
            </div>
            <div class="text-container" v-if="course.notes !== ''">
              <div class="icon">
                <font-awesome-icon :icon="['far', 'sticky-note']" size="lg" />
              </div>
              <div class="text">{{ course.notes }}</div>
            </div>
          </div>
        </div>
        <div class="data-container">
          <card-collapse-list class="data" title="Attendees">
            <response-list-entry
              v-for="assignment_request in course.assignment_requests"
              :key="assignment_request.id"
              :assignment_request="assignment_request"
            />
          </card-collapse-list>
        </div>
      </div>
      <div class="card-action">
        <form v-on:submit.prevent>
          <div class="can">Can you attend this course?</div>
          <loading-spinner size="big" v-if="buttonsDisabled" />
          <div v-else>
            <div class="input-field">
              <font-awesome-icon
                class="prefix"
                :icon="['far', 'clipboard']"
              ></font-awesome-icon>
              <input v-model="notes" type="text" id="notes" />
              <label for="notes">Notes</label>
            </div>
            <button class="btn success" @click="attend('yes')">
              Yes
            </button>
            <button class="btn warning" @click="attend('maybe')">
              Maybe
            </button>
            <button class="btn danger" @click="attend('no')">
              No
            </button>
            <div class="prefer">
              <button
                class="btn super-success"
                @click="attend('prefer')"
                :disabled="buttonsDisabled"
                :class="{ 'no-click': buttonsDisabled }"
              >
                Yes, teach/assist
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { COURSES } from "@/store/modules/courses";
import Vue from "vue";
import CardCollapseList from "@/components/courses/CardCollapseList";
import ResponseListEntry from "@/components/courses/ResponseListEntry";
import LoadingSpinner from "@/components/LoadingSpinner";
export default {
  name: "NotRespondedCard",
  components: { CardCollapseList, ResponseListEntry, LoadingSpinner },
  props: { course: Object },
  data: function() {
    return { notes: "", buttonsDisabled: false, hide: false };
  },
  methods: {
    attend: function(attendance) {
      this.buttonsDisabled = true;
      Vue.axios
        .post("courses/attend", {
          user_id: this.$store.getters.currentUser.id,
          course_id: this.course.id,
          attendance: attendance,
          notes: this.notes
        })
        .then(res => {
          this.$notify(res.data, "success");
          this.hide = true;
          this.$store.dispatch(COURSES);
        })
        .catch(({ errors }) => {
          this.$notify(errors[0], "error");
          this.buttonsDisabled = false;
        });
    }
  }
};
</script>

<style scoped lang="scss">
.cards-container {
  display: flex;
  justify-content: center;
  &.fade {
    opacity: 0;
  }
  .card {
    max-width: 320px;
    width: 100%;
    .card-content {
      .data-container {
        width: 100%;
        display: flex;
        justify-content: center;
        margin-top: 1rem;
        .data {
          max-width: 240px;
          width: 100%;
          .text-container {
            display: grid;
            grid-template-columns: 2rem auto;
            margin: 0.5rem 0;
          }
        }
      }
    }
    .card-action {
      .can {
        margin-bottom: 1rem;
      }
      .prefer {
        margin-top: 1rem;
      }
      .btn {
        margin: 0 0.5rem;
      }
    }
  }
}
</style>
