<template>
  <div>
    <not-responded-courses />
    <create-new-request
      v-if="
        this.$store.getters.currentUser.admin ||
          this.$store.getters.currentUser.organizer
      "
    />
    <all-requested-courses
      v-if="
        this.$store.getters.currentUser.admin ||
          this.$store.getters.currentUser.organizer
      "
    />
  </div>
</template>

<script>
import { COURSES } from "@/store/modules/courses";
import NotRespondedCourses from "@/components/dashboard/NotRespondedCourses";
import CreateNewRequest from "@/components/dashboard/CreateNewRequest";
import AllRequestedCourses from "@/components/dashboard/AllRequestedCourses";
export default {
  name: "dashboard",
  components: {
    NotRespondedCourses,
    CreateNewRequest,
    AllRequestedCourses
  },
  created() {
    this.$store.dispatch(COURSES);
  }
};
</script>

<style scoped lang="scss">
.test {
  display: block;
}
</style>
