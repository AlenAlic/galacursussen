<template>
  <table class="left-align">
    <thead>
      <tr>
        <th>Course</th>
        <th>Date and time</th>
        <th>Attendees</th>
        <th class="right-align">Profit</th>
        <th class="right-align">Paid</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(course, index) in courses" :key="index" :class="{ strikethrough: course.cancelled }">
        <td>{{ course.requested_by }}</td>
        <td>{{ getDateTime(course.date) }}</td>
        <td>{{ course.attendees }}</td>
        <td class="right-align">{{ price(course.price) }}</td>
        <td class="right-align paid_checkbox">
          <p v-if="course.paid">
            <label>
              <input type="checkbox" checked="checked" disabled />
              <span></span>
            </label>
          </p>
        </td>
      </tr>
      <tr>
        <td colspan="3" class="right-align">
          <b>Total</b>
        </td>
        <td class="right-align">{{ price(total) }}</td>
        <td></td>
      </tr>
    </tbody>
  </table>
</template>

<script>
import { DateTime } from "luxon";
import { currencyFormat } from "@/assets/js/utilities";
export default {
  name: "CoursesFinances",
  props: { courses: Array },
  computed: {
    total: function() {
      return this.courses.reduce((total, course) => {
        return total + course.price;
      }, 0);
    }
  },
  methods: {
    getDateTime: function(date) {
      let datetime = DateTime.fromISO(date, { zone: "UTC" });
      return datetime.toFormat("dd-LL-kkkk (HH:mm)");
    },
    price: function(price) {
      return currencyFormat(price);
    }
  }
};
</script>

<style scoped lang="scss">
.strikethrough {
  text-decoration: line-through;
}
.paid_checkbox {
  [type="checkbox"] + span {
    padding-left: 25px;
  }
}
</style>
