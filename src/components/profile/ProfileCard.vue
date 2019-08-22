<template>
  <div class="card">
    <div class="card-content" v-if="this.profile">
      <span class="card-title">{{ profile.full_name }}</span>
      <form v-on:submit.prevent>
        <div class="input-field">
          <font-awesome-icon class="prefix" icon="at" />
          <input v-model="email" type="email" id="email" />
          <label for="email" :class="{ active: email }">Email</label>
        </div>
        <p class="committees-container">
          <label>
            <input type="checkbox" v-model="incie" />
            <span>InCie</span>
          </label>
          <label>
            <input type="checkbox" v-model="salcie" />
            <span>SalCie</span>
          </label>
          <label>
            <input type="checkbox" v-model="mucie" />
            <span>MuCie</span>
          </label>
        </p>
        <button
          @click.prevent="updateProfile"
          :disabled="filled !== true"
          class="waves-effect waves-light btn"
          :class="{ 'no-click': !filled }"
        >
          Save
        </button>
      </form>
    </div>
  </div>
</template>

<script>
const validateEmail = email => {
  // eslint-disable-next-line no-useless-escape
  let re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(String(email).toLowerCase());
};
import { USER_PROFILE } from "@/store/modules/auth";
import Vue from "vue";
export default {
  name: "ProfileCard",
  props: { course: Object },
  data: function() {
    return {
      full_name: this.$store.getters.profile.full_name,
      email: this.$store.getters.profile.email,
      incie: this.$store.getters.profile.incie,
      salcie: this.$store.getters.profile.salcie,
      mucie: this.$store.getters.profile.mucie
    };
  },
  computed: {
    profile: function() {
      return this.$store.getters.profile;
    },
    filled: function() {
      return validateEmail(this.email);
    }
  },
  methods: {
    updateProfile: function() {
      Vue.axios
        .patch(`auth/user/${this.$store.getters.currentUser.id}`, {
          email: this.email,
          incie: this.incie,
          salcie: this.salcie,
          mucie: this.mucie
        })
        .then(res => {
          this.$notify(res.data, "success");
          this.$store.dispatch(USER_PROFILE);
        })
        .catch(({ errors }) => {
          this.$notify(errors[0], "error");
        });
    }
  }
};
</script>

<style scoped lang="scss">
.card {
  max-width: 90vw;
  width: 400px;
}
.committees-container {
  display: flex;
  justify-content: space-between;
  width: 100%;
  margin-bottom: 2rem !important;
  label {
    padding: 0 0.5rem;
  }
}
</style>
