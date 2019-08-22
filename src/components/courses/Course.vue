<template>
  <div class=" left-align">
    <div v-if="course">
      <div class="right-align buttons-container">
        <button class="btn btn-small" @click="showEditModal = true">
          Edit
        </button>
        <button class="btn btn-small primary" @click="showModal = true">
          Assignments
        </button>
      </div>
      <h5>{{ course.requested_by }} ({{ course.committee }})</h5>
      <h6>{{ course.date_formatted }}</h6>
      <div><b>Location: </b>{{ course.location }}</div>
      <div><b>Course language: </b>{{ course.language }}</div>
      <div><b>Dances: </b>{{ course.dances }}</div>
      <div><b>Notes: </b>{{ course.notes }}</div>
      <div :class="{ 'grey-text': !pastCourseDate }">
        <b>Attendees: </b>{{ course.attendees }}
      </div>
      <div :class="{ 'grey-text': !pastCourseDate }">
        <b>Price: </b>{{ course.price }}
      </div>
      <div :class="{ 'grey-text': !pastCourseDate }">
        <b>Paid: </b>{{ course.paid ? "yes" : "" }}
      </div>
      <div><b>MuCie available: </b>{{ course.has_mucie ? "Yes" : "No" }}</div>
      <div class="respone-list">
        <card-collapse-list :title="responsesTitle">
          <response-list :assignment_requests="requests" />
        </card-collapse-list>
      </div>
      <modal
        v-if="showEditModal"
        @close="showEditModal = false"
        :show-close-btn="false"
      >
        <edit-course-form
          slot="body"
          :course="course"
          @close="showEditModal = false"
        />
      </modal>
      <modal
        v-if="showModal"
        @close="showModal = false"
        :show-close-btn="false"
      >
        <div slot="body" @close="showModal = false">
          Hello
          <button class="btn grey accent-2" @click.prevent="showModal = false">
            Cancel
          </button>
        </div>
      </modal>
    </div>
  </div>
</template>

<script>
import ResponseList from "@/components/courses/ResponseList";
import Modal from "@/components/Modal";
import CardCollapseList from "@/components/courses/CardCollapseList";
import EditCourseForm from "@/components/courses/EditCourseForm";
export default {
  name: "Course",
  props: { data: Object },
  components: { EditCourseForm, CardCollapseList, Modal, ResponseList },
  data: function() {
    return {
      course: undefined,
      requests: [],
      showEditModal: false,
      showModal: false
    };
  },
  created: function() {
    this.course = this.data;
    this.requests = this.data.assignment_requests;
  },
  computed: {
    totalRequests: function() {
      return this.requests.length;
    },
    courseDate: function() {
      return new Date(this.course.date);
    },
    pastCourseDate: function() {
      return this.courseDate < new Date();
    },
    responses: function() {
      return (
        this.totalRequests -
        this.requests.filter(r => {
          return !r.attendance;
        }).length
      );
    },
    responsesTitle: function() {
      return `Responses ${this.responses} / ${this.totalRequests}`;
    }
  }
};
</script>

<style scoped lang="scss">
.buttons-container {
  display: flex;
  justify-content: space-between;
  width: 100%;
}
.respone-list {
  margin-bottom: 1.5rem;
  border-bottom: 1px solid grey;
  padding-bottom: 0.75rem;
}
</style>
