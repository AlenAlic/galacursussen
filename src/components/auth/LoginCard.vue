<template>
  <div class="form">
    <div class="card">
      <div class="card-content">
        <form v-on:submit.prevent>
          <errors :errors="errors" />
          <div class="input-field">
            <i class="material-icons prefix">person</i>
            <input v-model="email" type="email" id="email" />
            <label for="email">Email</label>
          </div>
          <div class="input-field">
            <i class="material-icons prefix">verified_user</i>
            <input v-model="password" type="password" id="password" />
            <label for="password">Password</label>
          </div>
          <div class="remember-me">
            <label for="remember-me">
              <input v-model="rememberMe" id="remember-me" type="checkbox" />
              <span>Remember me</span>
            </label>
          </div>
          <loading-spinner size="tiny" v-if="loading" />
          <button
            v-else
            @click.prevent="login"
            :disabled="filled !== true"
            class="waves-effect waves-light btn"
            :class="{ 'no-click': !filled }"
          >
            Login
          </button>
        </form>
      </div>
    </div>
    <a href="javascript:void(0);" @click.prevent="resetPassword">Forgot password?</a>
  </div>
</template>

<script>
import Errors from "@/components/Errors";
import LoadingSpinner from "@/components/LoadingSpinner";
export default {
  name: "LoginCard",
  components: { LoadingSpinner, Errors },
  data: function() {
    return {
      email: "",
      password: "",
      rememberMe: false,
      errors: [],
      loading: false
    };
  },
  computed: {
    filled: function() {
      return this.email !== "" && this.password !== "";
    }
  },
  methods: {
    login: function() {
      this.error = undefined;
      this.loading = true;
      this.$auth
        .signInWithUsernameAndPassword(this.email, this.password, this.rememberMe)
        .then(() => {
          this.$router.push({
            name: "dashboard"
          });
        })
        .catch(({ errors }) => {
          this.loading = false;
          return (this.errors = errors);
        });
    },
    resetPassword: function() {
      this.$router.push({
        name: "reset_password"
      });
    }
  }
};
</script>

<style scoped lang="scss">
.form {
  width: 100%;
  max-width: 330px;
  padding: 15px;
  margin: auto;
}
.remember-me {
  padding-bottom: 1rem;
}
</style>
