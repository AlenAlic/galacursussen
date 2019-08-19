<template>
  <collapse-card title="Add new course/workshop" :loading="!formLoaded">
    <create-new-request-form />
  </collapse-card>
</template>

<script>
import CreateNewRequestForm from "@/components/courses/CreateNewRequestForm";
import CollapseCard from "@/components/CollapseCard";
export default {
  name: "CreateNewRequest",
  components: { CreateNewRequestForm, CollapseCard },
  computed: {
    formLoaded: function() {
      return (
        this.$store.state.courses.languages.length > 0 &&
        this.$store.state.courses.committees.length > 0
      );
    }
  }
};
</script>
