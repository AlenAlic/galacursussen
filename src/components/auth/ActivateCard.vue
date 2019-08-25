<template>
  <div class="card">
    <div class="card-content" v-if="loading">
      <h4>Authenticating</h4>
      <loading-spinner class="mt" size="small" />
    </div>
    <div class="card-content" v-else-if="invalid">
      <h4>Invalid token</h4>
      <p>This token is not valid.</p>
    </div>
    <div class="card-content" v-else>
      <h4>Account activated</h4>
      <loading-spinner class="mt" size="small" />
    </div>
  </div>
</template>

<script>
import Vue from "vue";
import LoadingSpinner from "@/components/LoadingSpinner";
export default {
  name: "ActivateCard",
  components: { LoadingSpinner },
  props: { course: Object },
  data: function() {
    return {
      loading: true,
      redirecting: false,
      invalid: false
    };
  },
  mounted() {
    Vue.axios
      .get(`auth/activate/${this.$route.params.token}`)
      .then(res => {
        let token = res.data;
        setTimeout(() => {
          this.loading = false;
          this.redirecting = true;
          setTimeout(() => {
            this.$router.push({ name: "set_password", params: { token } });
          }, 1000);
        }, 1000);
      })
      .catch(() => {
        setTimeout(() => {
          this.loading = false;
          this.invalid = true;
        }, 500);
      });
  }
};
</script>

<style scoped lang="scss">
.card {
  max-width: 400px;
  width: 100%;
}
.mt {
  margin-top: 1rem;
}
</style>
