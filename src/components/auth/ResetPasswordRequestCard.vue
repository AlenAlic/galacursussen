<template>
  <div class="card">
    <form v-on:submit.prevent>
      <div class="card-content">
        <span class="card-title">Password reset</span>
        <div>
          <div class="input-field">
            <font-awesome-icon class="prefix" icon="key" />
            <input v-model="email" type="email" id="email" />
            <label for="email" :class="{ active: email }">Email</label>
          </div>
          <save-button
            @click.native="resetPassword"
            :loading="loading"
            :active="filled"
            text="Request password reset"
          />
        </div>
      </div>
    </form>
  </div>
</template>

<script>
import SaveButton from "@/components/SaveButton";
import Vue from "vue";
import { validateEmail } from "@/assets/js/utilities";
export default {
  name: "ResetPasswordRequestCard",
  components: { SaveButton },
  props: { course: Object },
  data: function() {
    return {
      email: "",
      loading: false,
      complete: false
    };
  },
  computed: {
    filled: function() {
      return validateEmail(this.email);
    }
  },
  methods: {
    resetPassword: function() {
      this.loading = true;
      Vue.axios
        .post("auth/password/reset", {
          email: this.email
        })
        .then(() => {
          this.complete = true;
          this.loading = false;
          this.email = "";
          this.$notify(
            "Password reset requested. If the email exists, an email to reset your password will be sent",
            "success"
          );
        })
        .catch(({ errors }) => {
          this.loading = false;
          this.$notify(errors[0], "error");
        });
    }
  }
};
</script>

<style scoped lang="scss">
.card {
  max-width: 400px;
  width: 100%;
}
.strength {
  margin: 1.5rem 0 2rem 0;
}
</style>
