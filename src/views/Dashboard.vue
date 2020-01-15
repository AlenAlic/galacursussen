<template>
  <div>
    <create-new-request v-if="this.$store.getters.hasOrganizerPrivileges" />
    <not-responded-courses v-if="this.$store.getters.committeeMember" />
    <upcoming-courses v-if="courses && this.$store.getters.committeeMember" />
    <h4 v-else-if="!this.$store.state.courses.loading && !this.$store.getters.isTreasurer">
      There are no upcoming courses.
    </h4>
    <treasurer-courses v-if="this.$store.getters.isTreasurer" />
  </div>
</template>

<script>
import { COURSES } from "@/store/modules/courses";
import NotRespondedCourses from "@/components/dashboard/NotRespondedCourses";
import CreateNewRequest from "@/components/dashboard/CreateNewRequest";
import UpcomingCourses from "@/components/dashboard/UpcomingCourses";
import TreasurerCourses from "@/components/dashboard/TreasurerCourses";
export default {
  name: "Dashboard",
  components: {
    TreasurerCourses,
    UpcomingCourses,
    NotRespondedCourses,
    CreateNewRequest
  },
  created() {
    if (!this.$store.getters.hasCourses) this.$store.dispatch(COURSES);
  },
  computed: {
    courses: function() {
      return this.$store.getters.courses.length > 0;
    }
  }
};
</script>

<style scoped lang="scss"></style>
