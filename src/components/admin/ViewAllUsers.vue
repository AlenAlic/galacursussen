<template>
  <div class="card">
    <div class="card-content">
      <span class="card-title">All users</span>
      <loading-spinner v-if="loading" />
      <table v-else-if="$util.isScreenLargeEnough()">
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
      <table v-else>
        <tbody v-for="user in users" :key="user.id">
          <tr>
            <th>Name</th>
            <td class="icon-right">{{ user.full_name }}</td>
          </tr>
          <tr>
            <th>Email</th>
            <td class="icon-right li">{{ $util.splitEmail(user.email) }}</td>
          </tr>
          <tr>
            <th>Access</th>
            <td class="icon-right">{{ user.access_level }}</td>
          </tr>
          <tr>
            <th>Account active</th>
            <td class="icon-right">
              <font-awesome-icon icon="check" v-if="user.is_active" />
              <font-awesome-icon icon="times" v-else />
            </td>
          </tr>
          <tr>
            <th>Active member</th>
            <td class="icon-right">
              <font-awesome-icon icon="check" v-if="user.active_member" />
              <font-awesome-icon icon="times" v-else />
            </td>
          </tr>
          <tr class="edit-button-row">
            <th></th>
            <td class="icon-right">
              <button class="btn btn-small" @click="setModal(user)">
                Edit
              </button>
            </td>
          </tr>
          <tr class="padding-row"></tr>
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
import { USERS } from "@/store/modules/users";
import LoadingSpinner from "@/components/LoadingSpinner";
import Modal from "@/components/Modal";
import EditUserForm from "@/components/admin/EditUserForm";
export default {
  name: "ViewAllUsers",
  components: { EditUserForm, Modal, LoadingSpinner },
  data: function() {
    return {
      errors: [],
      showModal: false,
      modalData: null
    };
  },
  computed: {
    users: function() {
      return this.$store.getters.users;
    },
    loading: function() {
      return this.$store.getters.loadingUsers;
    }
  },
  created() {
    if (!this.$store.getters.hasUsers) this.$store.dispatch(USERS);
  },
  methods: {
    setModal: function(user) {
      this.showModal = true;
      this.modalData = user;
    }
  }
};
</script>

<style scoped lang="scss">
.icon-right {
  text-align: right;
}
.edit-button-row {
  border-bottom: none;
}
.padding-row {
  height: 3rem;
}
</style>
