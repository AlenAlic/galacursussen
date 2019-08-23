<template>
  <div class="center-card">
    <activate-card />
  </div>
</template>

<script>
import ActivateCard from "@/components/auth/ActivateCard";
export default {
  name: "Activate",
  components: {
    ActivateCard
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
