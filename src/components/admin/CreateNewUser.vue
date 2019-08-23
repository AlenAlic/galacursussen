<template>
  <div class="card">
    <div class="card-content">
      <span class="card-title">Add new user</span>
      <form v-on:submit.prevent>
        <div class="input-field">
          <font-awesome-icon class="prefix" icon="user-tie" />
          <input v-model="first_name" type="text" id="first_name" />
          <label for="first_name" :class="{ active: first_name }"
            >First name</label
          >
        </div>
        <div class="input-field">
          <font-awesome-icon class="prefix" icon="signature" />
          <input v-model="last_name" type="text" id="last_name" />
          <label for="last_name" :class="{ active: last_name }"
            >Last name</label
          >
        </div>
        <div class="account-container">
          <label>
            <input v-model="account" name="account" type="radio" value="10" />
            <span>Organizer</span>
          </label>
          <label>
            <input v-model="account" name="account" type="radio" value="11" />
            <span>Member</span>
          </label>
          <label>
            <input v-model="account" name="account" type="radio" value="20" />
            <span>Treasurer</span>
          </label>
        </div>
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
        <save-button
          @click.native="createUser"
          :loading="loading"
          :active="filled"
          text="Add"
        />
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
import Vue from "vue";
import SaveButton from "@/components/SaveButton";
export default {
  name: "CreateNewUser",
  components: { SaveButton },
  props: { course: Object },
  data: function() {
    return {
      first_name: "",
      last_name: "",
      email: "",
      incie: false,
      salcie: false,
      mucie: false,
      account: "",
      loading: false,
      errors: []
    };
  },
  computed: {
    filled: function() {
      return (
        validateEmail(this.email) &&
        this.first_name &&
        this.last_name &&
        this.account !== ""
      );
    }
  },
  methods: {
    createUser: function() {
      this.loading = true;
      Vue.axios
        .post("auth/create", {
          first_name: this.first_name,
          last_name: this.last_name,
          email: this.email,
          incie: this.incie,
          salcie: this.salcie,
          mucie: this.mucie,
          account: this.account
        })
        .then(res => {
          this.first_name = "";
          this.last_name = "";
          this.email = "";
          this.incie = false;
          this.salcie = false;
          this.mucie = false;
          this.account = "";
          this.loading = false;
          this.$notify(res.data, "success");
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
</style>
