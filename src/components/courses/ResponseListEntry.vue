<template>
  <div>
    <div v-if="assignment_request" :class="attendanceClass(assignment_request)">
      {{ assignment_request.name }}
      <font-awesome-icon v-if="assignment_request.mucie" icon="music" />
    </div>
  </div>
</template>

<script>
export default {
  name: "ResponseListEntry",
  props: { assignment_request: Object },
  methods: {
    attendanceClass: function(assignment_request) {
      return {
        "grey-text": !assignment_request.attendance,
        "text-success": assignment_request.attendance === "yes",
        "text-super-success": assignment_request.attendance === "preference",
        "text-warning": assignment_request.attendance === "maybe",
        "text-danger": assignment_request.attendance === "no"
      };
    }
  }
};
</script>

<style scoped lang="scss"></style>
