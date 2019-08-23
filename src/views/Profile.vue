<template>
  <div class="profile-container">
    <div>
      <profile-card v-if="this.$store.getters.profile" />
    </div>
    <div>
      <change-password-card />
    </div>
  </div>
</template>

<script>
import ProfileCard from "@/components/profile/ProfileCard";
import ChangePasswordCard from "@/components/profile/ChangePasswordCard";
export default {
  name: "Profile",
  components: { ChangePasswordCard, ProfileCard }
};
</script>

<style scoped lang="scss">
.profile-container {
  display: flex;
  justify-content: space-evenly;
  width: 100%;
  flex-wrap: wrap;
}
</style>
