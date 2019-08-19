<template>
  <div class="row">
    <div class="col s12 m6">
      <h6 class="title">
        <b>Responses</b> - {{ totalResponses }} / {{ totalRequests }}
      </h6>
      <response-list-entry
        v-for="assignment_request in yes"
        :key="assignment_request.id"
        :assignment_request="assignment_request"
      >
      </response-list-entry>
      <response-list-entry
        v-for="assignment_request in maybe"
        :key="assignment_request.id"
        :assignment_request="assignment_request"
      >
      </response-list-entry>
      <response-list-entry
        v-for="assignment_request in no"
        :key="assignment_request.id"
        :assignment_request="assignment_request"
      >
      </response-list-entry>
    </div>
    <div class="col s12 m6">
      <h6 class="title">
        <b>Not responded</b> - {{ totalRequests - totalResponses }}
      </h6>
      <response-list-entry
        v-for="assignment_request in not_responded"
        :key="assignment_request.id"
        :assignment_request="assignment_request"
      >
      </response-list-entry>
    </div>
  </div>
</template>

<script>
import ResponseListEntry from "@/components/courses/ResponseListEntry";
export default {
  name: "ResponseList",
  props: { assignment_requests: Array },
  components: { ResponseListEntry },
  computed: {
    totalRequests: function() {
      return this.assignment_requests.length;
    },
    totalResponses: function() {
      return this.totalRequests - this.not_responded.length;
    },
    yes: function() {
      return this.assignment_requests.filter(r => {
        return r.attendance === "yes";
      });
    },
    maybe: function() {
      return this.assignment_requests.filter(r => {
        return r.attendance === "maybe";
      });
    },
    no: function() {
      return this.assignment_requests.filter(r => {
        return r.attendance === "no";
      });
    },
    not_responded: function() {
      return this.assignment_requests.filter(r => {
        return !r.attendance;
      });
    }
  }
};
</script>

<style scoped lang="scss">
.title {
  border-bottom: 1px solid grey;
}
</style>
