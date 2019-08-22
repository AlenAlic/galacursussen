<template>
  <collapse-card
    title="Add new course/workshop"
    :loading="this.$store.state.courses.loadingForm"
  >
    <create-new-request-form />
  </collapse-card>
</template>

<script>
import CreateNewRequestForm from "@/components/courses/CreateNewRequestForm";
import CollapseCard from "@/components/CollapseCard";
export default {
  name: "CreateNewRequest",
  components: { CreateNewRequestForm, CollapseCard }
};
</script>
