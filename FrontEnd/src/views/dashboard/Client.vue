<template>
  <div class="container">
    <div class="columns is-multiline">
      <div class="column is-12">
        <h1 class="title">{{ client.name }}</h1>
        <router-link
          :to="{ name: 'EditClient', params: { id: client.id } }"
          class="button is-light"
          >Edit</router-link
        >
        <button @click="deleteClient()" class="button is-danger">Delete</button>
      </div>
      <div class="column is-6">
        <div class="box">
          <h2 class="subtitle">Details</h2>
          <p><strong>Status: </strong>{{ client.name }}</p>

          <p><strong>Created At: </strong>{{ client.created_at }}</p>
          <p><strong>Modified At: </strong>{{ client.modified_at }}</p>
        </div>
      </div>
      <div class="column is-6">
        <div class="box">
          <h2 class="subtitle">Contact Information</h2>
          <p><strong>Contact Person:</strong> {{ client.contact_person }}</p>
          <p><strong>Contact EMail:</strong> {{ client.email }}</p>
          <p><strong>Contact Phone:</strong> {{ client.phone }}</p>
          <p><strong>Contact Website:</strong> {{ client.website }}</p>
        </div>
      </div>
      <div class="column is-6">
        <h2 class="subtitle">Notes</h2>
        <router-link class="button is-success mb-5" :to="{ name: 'AddNote' }"
          >Add Note</router-link
        >
        <div class="box" v-for="note in notes" v-bind:key="note.id">
          <h3 class="is-size-4">{{ note.name }}</h3>
          <p>
            {{ note.body }}
          </p>
          <router-link
            :to="{
              name: 'EditNote',
              params: { id: client.id, note_id: note.id },
            }"
            class="button is-warning mt-5"
            >Edit Note</router-link
          >
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import axios from "axios";
export default {
  name: "Client",
  data() {
    return {
      client: {},
      notes: {},
    };
  },
  mounted() {
    this.getClient();
  },
  methods: {
    async deleteClient() {
      this.$store.commit("setIsLoading", true);

      const clientId = this.$route.params.id;

      await axios
        .post(`/api/v1/client/delete/${clientId}/`)
        .then((response) => {
          console.log(response.data);
          this.$router.push({ name: "Clients" });
        })
        .catch((error) => {
          console.log(error);
        });

      this.$store.commit("setIsLoading", false);
    },
    async getClient() {
      this.$store.commit("setIsLoading", true);

      const clientId = this.$route.params.id;

      await axios
        .get(`/api/v1/clients/${clientId}/`)
        .then((response) => {
          this.client = response.data;
        })
        .catch((error) => {
          console.log(error);
        });

      await axios
        .get(`/api/v1/notes/?client_id=${clientId}`)
        .then((response) => {
          this.notes = response.data;
        })
        .catch((error) => {
          console.log(error);
        });

      this.$store.commit("setIsLoading", false);
    },
  },
};
</script>