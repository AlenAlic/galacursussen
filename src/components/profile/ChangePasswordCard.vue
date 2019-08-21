<template>
  <div class="card">
    <div class="card-content">
      <span class="card-title">Change password</span>
      <form v-on:submit.prevent>
        <errors :errors="errors"></errors>
        <div class="input-field">
          <font-awesome-icon class="prefix" icon="at" />
          <input v-model="current" type="password" id="current" />
          <label for="current" :class="{ active: current }"
            >Current password</label
          >
        </div>
        <div class="input-field">
          <font-awesome-icon class="prefix" icon="at" />
          <input v-model="password1" type="password" id="password1" />
          <label for="password1" :class="{ active: password1 }"
            >New password</label
          >
        </div>
        <div class="input-field">
          <font-awesome-icon class="prefix" icon="at" />
          <input v-model="password2" type="password" id="password2" />
          <label for="password2" :class="{ active: password2 }"
            >Repeat new password</label
          >
        </div>
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
        <button
          @click.prevent="updateProfile"
          :disabled="filled !== true"
          class="waves-effect waves-light btn"
          :class="{ 'no-click': !filled }"
        >
          Change password
        </button>
      </form>
    </div>
  </div>
</template>

<script>
const strongRegex = new RegExp(
  "^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.{16,})" // eslint-disable-line no-useless-escape
);
const mediumRegex = new RegExp(
  "^(((?=.*[a-z])(?=.*[A-Z]))|((?=.*[a-z])(?=.*[0-9]))|((?=.*[A-Z])(?=.*[0-9])))(?=.{12,})"
);
const weakRegex = new RegExp(
  "^(((?=.*[a-z])(?=.*[A-Z]))|((?=.*[a-z])(?=.*[0-9]))|((?=.*[A-Z])(?=.*[0-9])))(?=.{6,})"
);
import Vue from "vue";
import Errors from "@/components/Errors";
export default {
  name: "ChangePasswordCard",
  components: { Errors },
  props: { course: Object },
  data: function() {
    return {
      current: "",
      password1: "",
      password2: "",
      errors: []
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
      return (
        this.current !== "" && this.password1 !== "" && this.passwordsEqual
      );
    }
  },
  methods: {
    updateProfile: function() {
      if (!this.passwordsEqual) {
        this.errors = ["Passwords are not equal."];
      } else {
        Vue.axios
          .patch(`auth/password/${this.$store.getters.currentUser.id}`, {
            current: this.current,
            password1: this.password1,
            password2: this.password2
          })
          .then(res => {
            this.current = "";
            this.password1 = "";
            this.password2 = "";
            this.$notify(res.data, "success");
          })
          .catch(({ errors }) => {
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
.committees-container {
  display: flex;
  justify-content: space-between;
  width: 100%;
  padding-left: 45px;
  margin-bottom: 2rem !important;
}
</style>
