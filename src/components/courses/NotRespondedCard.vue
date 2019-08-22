<template>
  <div
    class="cards-container"
    ref="container"
    :class="{ fade: this.hide }"
    :style="{ height: this.height !== undefined ? `${this.height}px` : 'auto' }"
  >
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
              v-for="assignment in course.assignments"
              :key="assignment.id"
              :assignment="assignment"
            />
          </card-collapse-list>
        </div>
      </div>
      <div class="card-action">
        <form v-on:submit.prevent>
          <div class="can">Can you attend this course?</div>
          <div>
            <div class="input-field">
              <font-awesome-icon
                class="prefix"
                :icon="['far', 'clipboard']"
              ></font-awesome-icon>
              <input
                v-model="notes"
                type="text"
                id="notes"
                :disabled="loading"
              />
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
    </div>
  </div>
</template>

<script>
import { UPDATE_COURSE } from "@/store/modules/courses";
import Vue from "vue";
import CardCollapseList from "@/components/courses/CardCollapseList";
import ResponseListEntry from "@/components/courses/ResponseListEntry";
import LoadingSpinner from "@/components/LoadingSpinner";
export default {
  name: "NotRespondedCard",
  components: { CardCollapseList, ResponseListEntry, LoadingSpinner },
  props: { course: Object },
  data: function() {
    return {
      notes: "",
      loading: false,
      hide: false,
      height: undefined
    };
  },
  methods: {
    attend: function(attendance) {
      this.loading = true;
      this.height = this.$refs.container.scrollHeight;
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
          this.height = 0;
          let id = this.course.id;
          this.$store.dispatch(UPDATE_COURSE, { id });
        })
        .catch(({ errors }) => {
          this.$notify(errors, "error");
          this.loading = false;
          this.height = undefined;
        });
    }
  }
};
</script>

<style scoped lang="scss">
@import "../../assets/css/config";
.cards-container {
  display: flex;
  justify-content: center;
  width: 100%;
  transition: opacity $transition-time ease-in-out,
    height $transition-time ease-in-out;
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
      .btn {
        margin: 0 0.5rem;
      }
      .buttons-container {
        min-height: 45px;
      }
    }
  }
}
</style>
