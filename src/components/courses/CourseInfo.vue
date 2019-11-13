<template>
  <div :class="{ 'is-cancelled': course.cancelled }">
    <h5>
      {{ course.requested_by
      }}<span v-if="this.$store.getters.showCommitteeTitle">
        ({{ course.committee }})</span
      >
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
      <b>Price: </b>{{ price }}
    </div>
    <div :class="{ 'grey-text': !pastCourseDate }">
      <b>Paid: </b>{{ course.paid ? "Yes" : "No" }}
    </div>
    <div><b>MuCie available: </b>{{ course.has_mucie ? "Yes" : "No" }}</div>
  </div>
</template>

<script>
import { DateTime } from "luxon";
import { currencyFormat } from "@/assets/js/utilities";
export default {
  name: "CourseInfo",
  props: { course: Object },
  computed: {
    pastCourseDate: function() {
      return (
        DateTime.fromISO(this.course.date, { zone: "UTC" }) <
        DateTime.local().setZone("UTC")
      );
    },
    price: function() {
      return currencyFormat(this.course.price);
    }
  }
};
</script>

<style scoped lang="scss">
.response-list {
  margin-bottom: 1.5rem;
  border-bottom: 1px solid grey;
  padding-bottom: 0.75rem;
}
.is-cancelled {
  text-decoration: line-through;
}
</style>
