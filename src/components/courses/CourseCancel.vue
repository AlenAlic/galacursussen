<template>
  <div>
    <div class="cancel-button-container">
      <button
        v-if="!course.cancelled"
        class="btn btn-small danger"
        @click="showCancelModal = true"
      >
        Cancel
      </button>
      <button
        v-else
        class="btn btn-small primary"
        @click="showCancelModal = true"
      >
        Reinstate
      </button>
    </div>
    <modal
      v-if="showCancelModal"
      close-btn="No"
      :title="course.requested_by"
      @close="showCancelModal = false"
      size="medium"
    >
      <div slot="body">
        <p v-if="!course.cancelled">
          Are you sure you wish to cancel this course?
        </p>
        <p v-else>Are you sure you wish to reinstate this course?</p>
      </div>
      <button slot="button" class="btn" @click="patchCourse">
        Yes
      </button>
    </modal>
  </div>
</template>

<script>
import Vue from "vue";
import Modal from "@/components/Modal";
export default {
  name: "CourseCancel",
  props: { course: Object },
  components: {
    Modal
  },
  data: function() {
    return {
      showCancelModal: false,
      loading: false
    };
  },
  methods: {
    closeCancelModal: function() {
      this.loading = false;
      this.showCancelModal = false;
      this.$emit("closeModal");
    },
    patchCourse: function() {
      let id = this.course.id;
      this.loading = true;
      Vue.axios
        .patch(`courses/cancel/${id}`, {
          cancel: !this.course.cancelled
        })
        .then(() => {
          this.$notify(
            `Saved changes for ${this.course.requested_by}.`,
            "success"
          );
          this.closeCancelModal();
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
.cancel-button-container {
  margin-top: 1rem;
  text-align: right;
}
</style>
