<template>
  <div class="card">
    <div class="card-content" v-if="this.profile">
      <span class="card-title">Profile</span>
      <form v-on:submit.prevent>
        <div class="input-field">
          <font-awesome-icon class="prefix" icon="user-tie" />
          <input v-model="first_name" type="text" id="first_name" />
          <label for="first_name" :class="{ active: first_name }">First name</label>
        </div>
        <div class="input-field">
          <font-awesome-icon class="prefix" icon="signature" />
          <input v-model="last_name" type="text" id="last_name" />
          <label for="last_name" :class="{ active: last_name }">Last name</label>
        </div>
        <div class="input-field">
          <font-awesome-icon class="prefix" icon="at" />
          <input v-model="email" type="email" id="email" />
          <label for="email" :class="{ active: email }">Email</label>
        </div>
        <p class="committees-container" v-if="!this.$store.getters.isTreasurer">
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
        <!--        <p class="email-notifications left-align">-->
        <!--          <label>-->
        <!--            <input type="checkbox" v-model="email_notifications" />-->
        <!--            <span v-if="!this.$store.getters.isTreasurer">-->
        <!--              Email me when new courses are added-->
        <!--            </span>-->
        <!--            <span v-else>Email me when courses need invoices sent</span>-->
        <!--          </label>-->
        <!--        </p>-->
        <save-button @click.native="updateProfile" :loading="loading" :active="filled" text="Save profile" />
      </form>
    </div>
  </div>
</template>

<script>
import SaveButton from "@/components/SaveButton";
import { USER_PROFILE } from "@/store/modules/auth";
import Vue from "vue";
import { validateEmail } from "@/assets/js/utilities";
export default {
  name: "ProfileCard",
  components: { SaveButton },
  props: { course: Object },
  data: function() {
    return {
      first_name: this.$store.getters.profile.first_name,
      last_name: this.$store.getters.profile.last_name,
      email: this.$store.getters.profile.email,
      incie: this.$store.getters.profile.incie,
      salcie: this.$store.getters.profile.salcie,
      mucie: this.$store.getters.profile.mucie,
      email_notifications: this.$store.getters.profile.email_notifications,
      loading: false
    };
  },
  computed: {
    profile: function() {
      return this.$store.getters.profile;
    },
    filled: function() {
      return validateEmail(this.email) && this.first_name !== "" && this.last_name !== "";
    }
  },
  methods: {
    updateProfile: function() {
      this.loading = true;
      Vue.axios
        .patch(`auth/user/${this.$store.getters.currentUser.id}`, {
          first_name: this.first_name,
          last_name: this.last_name,
          email: this.email,
          incie: this.incie,
          salcie: this.salcie,
          mucie: this.mucie,
          email_notifications: this.email_notifications
        })
        .then(() => {
          this.$notify("Changes to profile saved.", "success");
          this.loading = false;
          this.$store.dispatch(USER_PROFILE);
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
  max-width: 90vw;
  width: 400px;
}
.committees-container {
  margin-bottom: 1rem !important;
}
.email-notifications {
  margin-bottom: 1rem !important;
  margin-left: 7.5px !important;
}
</style>
