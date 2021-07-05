<template>
  <div class="container">
    <div class="columns">
      <div class="column is-4 is-narrow-4 is-offset-4">
        <h1 class="title">Sign Up</h1>
        <form @submit.prevent="submitForm">
          <div class="field">
            <label class="label">Email</label>
            <div class="control">
              <input
                class="input"
                type="email"
                placeholder="Type Email"
                v-model="username"
              />
            </div>
          </div>
          <div class="field">
            <label class="label">Password</label>
            <div class="control">
              <input
                class="input"
                type="password"
                name="password"
                placeholder="Password"
                v-model="password"
              />
            </div>
          </div>

          <div class="notification is-danger" v-if="errors.length">
            <p v-for="error in errors" v-bind:key="error">
              {{ error }}
            </p>
          </div>

          <div class="field">
            <div class="control">
              <button type="submit" class="button is-success">Submit</button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
<script>
import axios from "axios";
export default {
  name: "Login",
  data() {
    return {
      username: "",
      password: "",
      errors: [],
    };
  },
  methods: {
    async submitForm() {
      this.errors = [];
      if (this.username === "") {
        this.errors.push("The Username is Missing");
      }
      if (this.password === "") {
        this.errors.push("The Password is too Short");
      }

      if (!this.errors.length) {
        const formData = {
          username: this.username,
          password: this.password,
        };
        this.$store.commit("setIsLoading", true);
        axios.defaults.headers.common["Authorization"] = "";
        localStorage.removeItem("token");
        await axios
          .post("/api/v1/token/login/", formData)
          .then((response) => {
            const token = response.data.auth_token;

            this.$store.commit("setToken", token);

            axios.defaults.headers.common["Authorization"] = "Token " + token;

            localStorage.setItem("token", token);

            this.$router.push("/my-account/");
          })
          .catch((error) => {
            if (error.response) {
              for (const property in error.response.data) {
                this.errors.push(
                  `${property}: ${error.response.data[property]}`
                );
              }
            } else if (error.message) {
              this.errors.push("Something went wrong. Please try again!");
            }
          });
        await axios
          .get("/api/v1/users/me")
          .then((response) => {
            this.$store.commit("setUser", {
              id: response.data.id,
              username: response.data.username,
            });
            localStorage.setItem("username", response.data.username);
            localStorage.setItem("userId", response.data.id);
          })
          .catch((error) => {
            console.log(error);
          });
        await axios
          .get("/api/v1/teams/get-my-team/")
          .then((response) => {
            console.log(response);
            this.$store.commit("setTeam", {
              id: response.data.id,
              name: response.data.name,
              plan: response.data.plan.name,
              max_leads: response.data.plan.max_leads,
              max_clients: response.data.plan.max_clients,
            });
            this.$router.push("/my-account/");
          })
          .catch((error) => {
            console.log(error);
          });
        this.$store.commit("setIsLoading", false);
      }
    },
  },
};
</script>