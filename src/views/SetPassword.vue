<template>
  <div class="center-card">
    <set-password-card />
  </div>
</template>

<script>
import SetPasswordCard from "@/components/auth/SetPasswordCard";
export default {
  name: "SetPassword",
  components: {
    SetPasswordCard
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
