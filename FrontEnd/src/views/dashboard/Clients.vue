
<template>
  <div class="container">
    <div class="columns is-multiline">
      <div class="column is-12">
        <h1 class="title">Clients</h1>
        <router-link
          class="button is-success"
          v-if="$store.state.team.max_clients > num_clients"
          :to="{ name: 'AddClient' }"
          >Add Client</router-link
        >
        <div v-else class="notification is-danger">
          You Have Reached The Top Of Your Limitations. Please Upgrade your
          Plan.
          <br />
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
        <template v-if="clients.length">
          <table class="table is-fullwidth">
            <thead>
              <tr>
                <th>Name</th>
                <th>Contact person</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="client in clients" v-bind:key="client.id">
                <td>{{ client.name }}</td>
                <td>{{ client.contact_person }}</td>

                <td>
                  <router-link
                    :to="{ name: 'Client', params: { id: client.id } }"
                    >Details</router-link
                  >
                </td>
              </tr>
            </tbody>
          </table>
          <div class="buttons">
            <button
              @click="goToPreviousPage()"
              class="button is-light"
              v-if="this.showPreviousButton"
            >
              Previous
            </button>
            <button
              @click="goToNextPage()"
              class="button is-light"
              v-if="this.showNextButton"
            >
              Next
            </button>
          </div>
        </template>
        <template v-else>
          <p>You don't have any Clients Yet. Add Now</p>
        </template>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "Clients",
  data() {
    return {
      clients: [],
      num_clients: 0,
      showNextButton: false,
      showPreviousButton: false,
      currentPage: 1,
      query: "",
    };
  },
  mounted() {
    this.getClients();
  },
  methods: {
    async goToPreviousPage() {
      this.currentPage -= 1;
      this.getClients();
    },
    async goToNextPage() {
      this.currentPage += 1;
      this.getClients();
    },
    async getClients() {
      this.$store.commit("setIsLoading", true);
      this.showNextButton = false;
      this.showPreviousButton = false;
      await axios
        .get(`/api/v1/clients/?page=${this.currentPage}&search=${this.query}`)
        .then((response) => {
          this.clients = response.data.results;
          this.num_clients = response.data.count;
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
      this.getClients();
    },
  },
};
</script>