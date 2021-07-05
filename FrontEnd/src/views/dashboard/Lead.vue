<template>
  <div class="container">
    <div class="columns is-multiline">
      <div class="column is-12">
        <h1 class="title">{{ lead.company }}</h1>
        <div class="buttons">
          <router-link
            :to="{ name: 'EditLead', params: { id: lead.id } }"
            class="button is-light"
            >Edit</router-link
          >
          <button @click="convertTolient" class="button is-info">
            Convert to Client
          </button>
          <button @click="deleteLead()" class="button is-danger">Delete</button>
        </div>
      </div>
      <div class="column is-6">
        <div class="box">
          <h2 class="subtitle">Details</h2>
          <p><strong>Status: </strong>{{ lead.status }}</p>
          <p><strong>Priority: </strong>{{ lead.priority }}</p>
          <p><strong>Confidience: </strong>{{ lead.confidencec }}</p>
          <p><strong>Estimated Value: </strong>{{ lead.estimated_value }}</p>
          <p>
            <strong>Assigned to: </strong>
            <template v-if="lead.assigned_to"
              >{{ lead.assigned_to.first_name }}
              {{ lead.assigned_to.last_name }}</template
            >
            <template v-else>Not Assigned Yet</template>
          </p>
          <p><strong>Created At: </strong>{{ lead.created_at }}</p>
          <p><strong>Modified At: </strong>{{ lead.modified_at }}</p>
        </div>
      </div>
      <div class="column is-6">
        <div class="box">
          <h2 class="subtitle">Contact Information</h2>
          <p><strong>Contact Person:</strong> {{ lead.contact_person }}</p>
          <p><strong>Contact EMail:</strong> {{ lead.email }}</p>
          <p><strong>Contact Phone:</strong> {{ lead.phone }}</p>
          <p><strong>Contact Website:</strong> {{ lead.website }}</p>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import axios from "axios";
export default {
  name: "Lead",
  data() {
    return {
      lead: {},
    };
  },
  mounted() {
    this.getLead();
  },
  methods: {
    async deleteLead() {
      this.$store.commit("setIsLoading", true);

      const leadId = this.$route.params.id;

      await axios
        .post(`/api/v1/leads/delete/${leadId}/`)
        .then((response) => {
          console.log(response.data);
          this.$router.push({ name: "Leads" });
        })
        .catch((error) => {
          console.log(error);
        });

      this.$store.commit("setIsLoading", false);
    },
    async getLead() {
      this.$store.commit("setIsLoading", true);

      const leadId = this.$route.params.id;

      await axios
        .get(`/api/v1/leads/${leadId}/`)
        .then((response) => {
          this.lead = response.data;
        })
        .catch((error) => {
          console.log(error);
        });

      this.$store.commit("setIsLoading", false);
    },

    async convertTolient() {
      this.$store.commit("setIsLoading", true);

      const leadId = this.$route.params.id;

      const data = {
        lead_id: leadId,
      };

      await axios
        .post(`/api/v1/convert-lead-to-client/`, data)
        .then((response) => {
          console.log("Converted to Client");
          this.$route.push({ name: "Clients" });
        })
        .catch((error) => {
          console.log(error);
        });

      this.$store.commit("setIsLoading", false);
    },
  },
};
</script>