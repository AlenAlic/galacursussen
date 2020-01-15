<template>
  <div class="card">
    <div class="card-content">
      <span class="card-title">Set password</span>
      <form v-on:submit.prevent>
        <errors :errors="errors"></errors>
        <div class="input-field">
          <font-awesome-icon class="prefix" icon="key" />
          <input v-model="password1" type="password" id="password1" />
          <label for="password1" :class="{ active: password1 }">Password</label>
        </div>
        <div class="input-field">
          <font-awesome-icon class="prefix" icon="key" />
          <input v-model="password2" type="password" id="password2" />
          <label for="password2" :class="{ active: password2 }">Repeat password</label>
        </div>
        <div class="strength">
          <div>Password strength</div>
          <div class="progress">
            <div
              class="determinate"
              :class="passwordColor"
              :style="{
                width: passwordWidth
              }"
            ></div>
          </div>
        </div>
        <save-button
          @click.native="setPassword"
          :loading="loading"
          :active="filled"
          text="Set password"
        />
      </form>
    </div>
  </div>
</template>

<script>
import SaveButton from "@/components/SaveButton";
import Vue from "vue";
import Errors from "@/components/Errors";
import { strongRegex, mediumRegex, weakRegex } from "@/assets/js/utilities";
export default {
  name: "ResetPasswordCard",
  components: { SaveButton, Errors },
  props: { course: Object },
  data: function() {
    return {
      password1: "",
      password2: "",
      errors: [],
      loading: false
    };
  },
  computed: {
    passwordsEqual: function() {
      return this.password1 === this.password2;
    },
    passwordWidth: function() {
      if (strongRegex.test(this.password1)) return "100%";
      if (mediumRegex.test(this.password1)) return "67%";
      if (weakRegex.test(this.password1)) return "33%";
      if (this.password1.length > 0) return "5%";
      return "0%";
    },
    passwordColor: function() {
      if (strongRegex.test(this.password1)) return "green";
      if (mediumRegex.test(this.password1)) return "yellow";
      if (weakRegex.test(this.password1)) return "red";
      return "grey";
    },
    filled: function() {
      return this.current !== "" && this.password1 !== "" && this.passwordsEqual;
    }
  },
  methods: {
    setPassword: function() {
      if (!this.passwordsEqual) {
        this.errors = ["Passwords are not equal."];
      } else {
        this.loading = true;
        Vue.axios
          .patch(`auth/password/reset/${this.$route.params.token}`, {
            password1: this.password1,
            password2: this.password2
          })
          .then(() => {
            this.password1 = "";
            this.password2 = "";
            this.$notify("Password reset.", "success");
            setTimeout(() => {
              this.$router.push({ name: "login" });
            }, 1000);
          })
          .catch(({ errors }) => {
            this.loading = false;
            this.$notify(errors[0], "error");
          });
      }
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
