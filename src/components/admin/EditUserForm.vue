<template>
  <form v-on:submit.prevent>
    <h4>Edit profile</h4>
    <div class="input-field">
      <font-awesome-icon class="prefix" icon="user-tie" />
      <input v-model="user.first_name" type="text" id="first_name" />
      <label for="first_name" :class="{ active: user.first_name }">First name</label>
    </div>
    <div class="input-field">
      <font-awesome-icon class="prefix" icon="signature" />
      <input v-model="user.last_name" type="text" id="last_name" />
      <label for="last_name" :class="{ active: user.last_name }">Last name</label>
    </div>
    <div class="input-field">
      <font-awesome-icon class="prefix" icon="at" />
      <input v-model="user.email" type="email" id="email" />
      <label for="email" :class="{ active: user.email }">Email</label>
    </div>
    <p class="committees-container single-line-checkbox">
      <label>
        <input type="checkbox" v-model="user.incie" />
        <span>InCie</span>
      </label>
      <label>
        <input type="checkbox" v-model="user.salcie" />
        <span>SalCie</span>
      </label>
      <label>
        <input type="checkbox" v-model="user.mucie" />
        <span>MuCie</span>
      </label>
    </p>
    <p class="single-line-checkbox">
      <label>
        <input type="checkbox" v-model="user.is_active" />
        <span>Account active</span>
      </label>
    </p>
    <p class="single-line-checkbox">
      <label class="single-line-checkbox">
        <input type="checkbox" v-model="user.active_member" />
        <span>Active member of committee</span>
      </label>
    </p>
    <div class="radios">
      <div class="radio-title">Access level</div>
      <label>
        <input v-model="user.access" value="0" name="access" type="radio" />
        <span>Admin</span>
      </label>
      <label>
        <input v-model="user.access" value="10" name="access" type="radio" />
        <span>Organizer</span>
      </label>
      <label>
        <input v-model="user.access" value="11" name="access" type="radio" />
        <span>Member</span>
      </label>
      <label>
        <input v-model="user.access" value="20" name="access" type="radio" />
        <span>Treasurer</span>
      </label>
    </div>
    <div class="buttons-container">
      <save-button @click.native="updateProfile" :loading="loading" :active="filled" text="Save" />
      <button class="btn cancel" @click="exit">Cancel</button>
    </div>
  </form>
</template>

<script>
import Vue from "vue";
import SaveButton from "@/components/SaveButton";
import { validateEmail } from "@/assets/js/utilities";
export default {
  name: "EditUserForm",
  components: { SaveButton },
  props: { userData: Object },
  data: function() {
    return {
      user: this.userData,
      loading: false,
      errors: {}
    };
  },
  computed: {
    profile: function() {
      return this.$store.getters.profile;
    },
    filled: function() {
      return validateEmail(this.user.email) && this.user.first_name !== "" && this.user.last_name !== "";
    }
  },
  methods: {
    updateProfile: function() {
      this.loading = true;
      Vue.axios
        .patch(`admin/user/${this.user.id}`, {
          first_name: this.user.first_name,
          last_name: this.user.last_name,
          email: this.user.email,
          incie: this.user.incie,
          salcie: this.user.salcie,
          mucie: this.user.mucie,
          is_active: this.user.is_active,
          active_member: this.user.active_member,
          access: this.user.access
        })
        .then(() => {
          this.$notify(`Changes to profile of ${this.user.first_name} saved.`, "success");
          this.loading = false;
          this.$emit("close");
        })
        .catch(({ errors }) => {
          this.loading = false;
          this.$notify(errors[0], "error");
        });
    },
    exit: function() {
      this.$emit("close");
    }
  }
};
</script>

<style scoped lang="scss">
@import "../../assets/css/config";
.radios {
  margin: 1rem 0;
  label {
    padding-right: 16px;
  }
  .radio-title {
    font-size: 0.8rem;
    color: #9e9e9e;
  }
}
.buttons-container {
  button {
    margin: 1rem 0.5rem 0.5rem 0.5rem;
  }
}
.single-line-checkbox {
  margin-bottom: 1rem !important;
}
</style>
