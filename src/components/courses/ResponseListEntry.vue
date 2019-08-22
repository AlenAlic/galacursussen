<template>
  <div>
    <div v-if="assignment" :class="attendanceClass(assignment)">
      {{ assignment.name }}
      <font-awesome-icon v-if="assignment.mucie" icon="music" />
    </div>
  </div>
</template>

<script>
export default {
  name: "ResponseListEntry",
  props: { assignment: Object },
  methods: {
    attendanceClass: function(assignment) {
      return {
        "grey-text": !assignment.attendance,
        "text-success": assignment.attendance === "yes",
        "text-super-success": assignment.attendance === "preference",
        "text-warning": assignment.attendance === "maybe",
        "text-danger": assignment.attendance === "no"
      };
    }
  }
};
</script>

<style scoped lang="scss"></style>
