<template>
  <div class=" left-align">
    <div v-if="course">
      <h5 class="title">
        {{ course.requested_by }} ({{ course.committee }})
        <button class="btn right btn-small" @click="showModal = true">
          Edit
        </button>
      </h5>
      <h6>{{ course.date_formatted }}</h6>
      <div><b>Location: </b>{{ course.location }}</div>
      <div><b>Course language: </b>{{ course.language }}</div>
      <div><b>Dances: </b>{{ course.dances }}</div>
      <div><b>Notes: </b>{{ course.notes }}</div>
      <div :class="{ 'grey-text': !pastCourseDate }">
        <b>Attendees: </b>{{ course.attendees }}
      </div>
      <div :class="{ 'grey-text': !pastCourseDate }">
        <b>Price: </b>{{ course.price1 }}
      </div>
      <div :class="{ 'grey-text': !pastCourseDate }">
        <b>Paid: </b>{{ course.paid ? "yes" : "" }}
      </div>
      <div><b>MuCie available: </b>{{ course.has_mucie ? "Yes" : "No" }}</div>
      <div>
        <response-list :assignment_requests="requests" />
      </div>
      <modal
        title="Test"
        v-if="showModal"
        @close="showModal = false"
        closeBtn="Cancel"
      >
        <p slot="body">
          Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
          eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad
          minim veniam, quis nostrud exercitation ullamco laboris nisi ut
          aliquip ex ea commodo consequat. Duis aute irure dolor in
          reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
          pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
          culpa qui officia deserunt mollit anim id est laborum.
        </p>
        <button slot="button" class="btn" @click="alert">Save</button>
      </modal>
    </div>
  </div>
</template>

<script>
import ResponseList from "@/components/courses/ResponseList";
import Modal from "@/components/Modal";
export default {
  name: "Course",
  props: { data: Object },
  components: { Modal, ResponseList },
  data: function() {
    return {
      course: undefined,
      requests: [],
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
    }
  },
  methods: {
    alert: function() {
      alert("Hi");
    }
  }
};
</script>

<style scoped lang="scss">
.title {
  border-bottom: 1px solid grey;
  padding-bottom: 0.75rem;
}
</style>
