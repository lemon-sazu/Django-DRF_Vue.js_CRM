<template>
  <div class="container">
    <div class="columns is-multiline">
      <div class="column is-12">
        <h1 class="title">Add Member</h1>
      </div>
      <div class="comumn is-12">
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
          <div class="field">
            <label class="label">Reapet Password</label>
            <div class="control">
              <input
                class="input"
                type="password"
                name="password1"
                placeholder="Password"
                v-model="password2"
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
import { toast } from "bulma-toast";
export default {
  name: "AddMember",
  data() {
    return {
      username: "",
      password: "",
      password2: "",
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
      if (this.password2 !== this.password) {
        this.errors.push("Password is not metching");
      }
      if (!this.errors.length) {
        this.$store.commit("setIsLoading", true);
        const formData = {
          username: this.username,
          password: this.password2,
        };
        const emailData = { email: this.username };
        await axios
          .post("/api/v1/users/", formData)
          .then((response) => {
            axios
              .post("/api/v1/teams/add-member/", emailData)
              .then((response) => {
                toast({
                  message: "Member added Successfully",
                  type: "is-success",
                  dismissible: true,
                  pauseOnHover: true,
                  duration: 2000,
                  position: "top-center",
                });
                this.$router.push({ name: "Team" });
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

        this.$store.commit("setIsLoading", false);
      }
    },
  },
};
</script>