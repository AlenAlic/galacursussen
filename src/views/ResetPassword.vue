<template>
  <div class="center-card">
    <reset-password-card v-if="this.$route.params.token" />
    <reset-password-request-card v-else />
  </div>
</template>

<script>
import ResetPasswordCard from "@/components/auth/ResetPasswordCard";
import ResetPasswordRequestCard from "@/components/auth/ResetPasswordRequestCard";
export default {
  name: "ResetPassword",
  components: {
    ResetPasswordRequestCard,
    ResetPasswordCard
  }
};
</script>

<style scoped>
.center-card {
  min-height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
