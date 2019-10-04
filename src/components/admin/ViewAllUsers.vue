<template>
  <div class="card">
    <div class="card-content">
      <span class="card-title">All users</span>
      <loading-spinner v-if="loading" />
      <table v-else>
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Access</th>
            <th>Account active</th>
            <th>Active member</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.full_name }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.access_level }}</td>
            <td>
              <font-awesome-icon icon="check" v-if="user.is_active" />
              <font-awesome-icon icon="times" v-else />
            </td>
            <td>
              <font-awesome-icon icon="check" v-if="user.active_member" />
              <font-awesome-icon icon="times" v-else />
            </td>
            <td>
              <button class="btn btn-small" @click="setModal(user)">
                Edit
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <modal v-if="showModal" @close="showModal = false" size="medium">
        <edit-user-form
          slot="body"
          :user-data="modalData"
          @close="showModal = false"
        />
      </modal>
    </div>
  </div>
</template>

<script>
import Vue from "vue";
import LoadingSpinner from "@/components/LoadingSpinner";
import Modal from "@/components/Modal";
import EditUserForm from "@/components/admin/EditUserForm";
export default {
  name: "ViewAllUsers",
  components: { EditUserForm, Modal, LoadingSpinner },
  props: { course: Object },
  data: function() {
    return {
      users: [],
      loading: true,
      errors: [],
      showModal: false,
      modalData: null
    };
  },
  created() {
    this.getUsers();
  },
  methods: {
    getUsers: function() {
      this.loading = true;
      return Vue.axios
        .get("admin/users")
        .then(res => {
          this.users = res.data;
          this.loading = false;
        })
        .catch(() => {
          this.loading = false;
        });
    },
    setModal: function(user) {
      this.showModal = true;
      this.modalData = user;
    }
  }
};
</script>

<style scoped lang="scss"></style>
