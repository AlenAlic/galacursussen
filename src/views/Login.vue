<template>
  <div class="login">
    <login-card />
  </div>
</template>

<script>
import LoginCard from "@/components/auth/LoginCard";
export default {
  name: "Login",
  components: {
    LoginCard
  },
  created() {
    if (this.$auth.isAuthenticated())
      this.$router.push({
        name: "dashboard"
      });
  }
};
</script>

<style scoped>
.login {
  min-height: 100%;
  display: -ms-flexbox;
  display: flex;
  -ms-flex-align: center;
  align-items: center;
}
</style>
