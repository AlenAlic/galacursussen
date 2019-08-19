<template>
  <div>
    <not-responded-card
      v-for="course in courses"
      :key="course.id"
      :course="course"
    ></not-responded-card>
  </div>
</template>

<script>
import NotRespondedCard from "@/components/courses/NotRespondedCard";
export default {
  name: "NotRespondedCourses",
  components: { NotRespondedCard },
  computed: {
    courses: function() {
      let courses = this.$store.state.courses.courses;
      if (courses.length > 0) {
        courses = courses.filter(c => {
          let d = new Date(c.date);
          return d > new Date();
        });
        courses = courses.filter(c => {
          return c.assignment_requests.some(
            a =>
              a.user_id === this.$store.getters.currentUser.id && !a.attendance
          );
        });
      }
      return courses;
    },
    hasCourses: function() {
      return this.courses.length > 0;
    }
  }
};
</script>

<style scoped lang="scss">
.cards-container {
  display: flex;
  justify-content: center;
  .card {
    max-width: 320px;
    width: 100%;
    .card-content {
      .data-container {
        width: 100%;
        display: flex;
        justify-content: center;
        margin-top: 1rem;
        .data {
          max-width: 240px;
          width: 100%;
          .text-container {
            display: grid;
            grid-template-columns: 2rem auto;
            margin: 0.5rem 0;
          }
        }
      }
    }
    .card-action {
      .can {
        margin-bottom: 1rem;
      }
      .prefer {
        margin-top: 1rem;
      }
      .btn {
        margin: 0 0.5rem;
      }
    }
  }
}
</style>
