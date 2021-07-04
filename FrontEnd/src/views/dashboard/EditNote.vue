<template>
  <div class="container">
    <div class="columns is-multiline">
      <div class="column is-12">
        <h1 class="title">Edit Note</h1>
      </div>
      <div class="column is-6">
        <form @submit.prevent="submitForm">
          <div class="field">
            <label>Name</label>
            <div class="control">
              <input type="text" class="input" v-model="note.name" />
            </div>
          </div>

          <div class="field">
            <label>Body</label>
            <div class="control">
              <textarea v-model="note.body" class="textarea"></textarea>
            </div>
          </div>

          <div class="field">
            <div class="control">
              <button class="button is-success">Submit</button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { toast } from "bulma-toast";
export default {
  name: "Edit",
  data() {
    return {
      note: {},
    };
  },
  mounted() {
    this.getNote();
  },
  methods: {
    async getNote() {
      this.$store.commit("setIsLoading", true);
      const clientId = this.$route.params.id;
      const noteId = this.$route.params.note_id;

      axios
        .get(`/api/v1/notes/${noteId}/?client_id=${clientId}`)
        .then((response) => {
          this.note = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
      this.$store.commit("setIsLoading", false);
    },
    async submitForm() {
      this.$store.commit("setIsLoading", true);
      const clientId = this.$route.params.id;
      const noteId = this.$route.params.note_id;
      await axios
        .patch(`/api/v1/notes/${noteId}/?client_id=${clientId}`, this.note)
        .then((response) => {
          toast({
            message: "The Note was Updated",
            type: "is-success",
            dismissible: true,
            pauseOnHover: true,
            duration: 2000,
            position: "top-right",
          });
          this.$router.push({
            name: "Client",
            params: { id: this.$route.params.id },
          });
        })
        .catch((error) => {
          console.log(error);
        });

      this.$store.commit("setIsLoading", false);
    },
  },
};
</script>