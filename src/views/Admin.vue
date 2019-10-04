<template>
  <div>
    <div class="center-card-container">
      <create-new-user />
    </div>
    <div>
      <view-all-users />
    </div>
  </div>
</template>

<script>
import CreateNewUser from "@/components/admin/CreateNewUser";
import ViewAllUsers from "@/components/admin/ViewAllUsers";
export default {
  name: "Admin",
  components: { ViewAllUsers, CreateNewUser }
};
</script>

<style scoped lang="scss"></style>
