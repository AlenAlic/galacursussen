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
        this.$store.getters.hasLanguages && this.$store.getters.hasCommittees
      );
    }
  }
};
</script>
