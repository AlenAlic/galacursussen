<template>
  <div class="center-card-container">
    <create-new-user />
  </div>
</template>

<script>
import CreateNewUser from "@/components/admin/CreateNewUser";
export default {
  name: "Admin",
  components: { CreateNewUser }
};
</script>

<style scoped lang="scss"></style>
