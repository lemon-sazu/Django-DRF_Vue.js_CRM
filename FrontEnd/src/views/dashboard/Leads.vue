<template>
  <div class="container">
    <div class="columns is-multiline">
      <div class="column is-12">
        <h1 class="title">Leads</h1>

        <router-link
          v-if="$store.state.team.max_leads > num_leads"
          class="button is-success"
          to="/dashboard/leads/add"
          >Add Lead</router-link
        >
        <div v-else class="notification is-danger">
          You Have Reached The Top Of Your Limitations. Please Upgrade your
          Plan. <br />
          <router-link class="button is-light mt-5" :to="{ name: 'Plan' }"
            >Upgrade Now</router-link
          >
        </div>
        <hr />
        <form @submit.prevent="SearchQuery">
          <div class="field has-addons">
            <div class="control">
              <input type="text" class="input" v-model="query" />
            </div>
            <div class="control">
              <button class="button is-success">Search</button>
            </div>
          </div>
        </form>
      </div>
      <div class="column is-12">
        <table class="table is-fullwidth">
          <thead>
            <tr>
              <th>Company</th>
              <th>Contact person</th>
              <th>Assigned To</th>
              <th>Status</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="lead in leads" v-bind:key="lead.id">
              <td>{{ lead.company }}</td>
              <td>{{ lead.contact_person }}</td>
              <td>
                <template v-if="lead.assigned_to"
                  >{{ lead.assigned_to.first_name
                  }}{{ lead.assigned_to.last_name }}</template
                >
                <template v-else>Not Assigned Yet</template>
              </td>
              <td>{{ lead.status }}</td>
              <td>
                <router-link :to="{ name: 'Lead', params: { id: lead.id } }"
                  >Details</router-link
                >
              </td>
            </tr>
          </tbody>
        </table>
        <div class="butons">
          <button
            @click="goToPreviousPage()"
            v-if="showPreviousButton"
            class="button is-light"
          >
            Previous
          </button>
          <button
            @click="goToNextPage()"
            v-if="showNextButton"
            class="button is-light"
          >
            Next
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "Leads",
  data() {
    return {
      leads: [],
      num_leads: 0,
      showNextButton: false,
      showPreviousButton: false,
      currentPage: 1,
      query: "",
    };
  },
  mounted() {
    this.getLeads();
  },
  methods: {
    async goToNextPage() {
      this.currentPage += 1;
      this.getLeads();
    },
    async goToPreviousPage() {
      this.currentPage -= 1;
      this.getLeads();
    },
    async getLeads() {
      this.$store.commit("setIsLoading", true);
      this.showNextButton = false;
      this.showPreviousButton = false;

      await axios.get(`/api/v1/leads/`).then((response) => {
        this.num_leads = response.data.count;
        console.log(this.num_leads);
      });

      await axios
        .get(`/api/v1/leads/?page=${this.currentPage}&search=${this.query}`)
        .then((response) => {
          this.leads = response.data.results;
          console.log(response.data);
          if (response.data.next) {
            this.showNextButton = true;
          }
          if (response.data.previous) {
            this.showPreviousButton = true;
          }
        })
        .catch((error) => {
          console.log(error);
        });
      this.$store.commit("setIsLoading", true);
    },
    SearchQuery() {
      this.currentPage = 1;
      this.getLeads();
    },
  },
};
</script>