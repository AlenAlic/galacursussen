<template>
  <div class="left-align">
    <div>
      <h5>{{ course.requested_by }}</h5>
      <h6>{{ course.date_formatted }}</h6>
      <div><b>Committee: </b>{{ course.committee }}</div>
      <div><b>Attendees: </b>{{ course.attendees }}</div>
      <div><b>Price: </b>{{ price }}</div>
      <div><b>Paid: </b>{{ course.paid ? "Yes" : "No" }}</div>
      <div class="center-align mt">
        <save-button @click.native="createUser" :loading="loading" :active="true" :text="buttonText" />
      </div>
    </div>
  </div>
</template>

<script>
import { UPDATE_COURSE } from "@/store/modules/courses";
import Vue from "vue";
import { currencyFormat } from "@/assets/js/utilities";
import SaveButton from "@/components/SaveButton";
export default {
  name: "TreasurerCourse",
  components: { SaveButton },
  props: { course: Object },
  data: function() {
    return {
      paid: this.course.paid,
      errors: [],
      loading: false
    };
  },
  computed: {
    price: function() {
      return currencyFormat(this.course.price);
    },
    buttonText: function() {
      return this.paid ? "Mark as not paid" : "Mark as paid";
    }
  },
  methods: {
    createUser: function() {
      this.loading = true;
      let id = this.course.id;
      Vue.axios
        .patch(`courses/paid/${id}`, {
          paid: !this.paid
        })
        .then(() => {
          this.paid = !this.paid;
          this.loading = false;
          this.$store.dispatch(UPDATE_COURSE, { id });
          this.$notify("Course payment updated", "success");
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
.mt {
  margin-top: 1rem;
}
</style>
