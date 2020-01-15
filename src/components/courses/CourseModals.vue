<template>
  <div>
    <div class="right-align buttons-container">
      <button class="btn btn-small" @click="showEditModal = true">
        Edit
      </button>
      <button class="btn btn-small primary" @click="showModal = true">
        Assignments
      </button>
    </div>
    <modal v-if="showEditModal" @close="showEditModal = false" size="large">
      <edit-course-form
        slot="body"
        :course="course"
        @close="closeEditModal"
        @cancel="showEditModal = false"
      />
    </modal>
    <modal v-if="showModal" @close="showModal = false" size="medium">
      <assign-course-form slot="body" :course-data="course" @close="closeAssignModal" />
    </modal>
  </div>
</template>

<script>
import Modal from "@/components/Modal";
import EditCourseForm from "@/components/courses/EditCourseForm";
import AssignCourseForm from "@/components/courses/AssignCourseForm";
export default {
  name: "CourseModals",
  props: { course: Object },
  components: {
    AssignCourseForm,
    EditCourseForm,
    Modal
  },
  data: function() {
    return {
      showEditModal: false,
      showModal: false
    };
  },
  methods: {
    closeEditModal: function() {
      this.showEditModal = false;
      this.$emit("closeModal");
    },
    closeAssignModal: function() {
      this.showModal = false;
      this.$emit("closeModal");
    }
  }
};
</script>

<style scoped lang="scss">
.buttons-container {
  display: flex;
  justify-content: space-between;
  width: 100%;
}
</style>
