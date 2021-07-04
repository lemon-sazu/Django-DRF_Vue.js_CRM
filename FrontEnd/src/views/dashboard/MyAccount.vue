<template>
  <div class="container">
    <div class="columns is-multiline">
      <div class="column is-12">
        <h1 class="title">My Account</h1>
      </div>
    </div>
    <div class="column is-12">
      <div class="buttons">
        <router-link
          class="button is-success"
          :to="{ name: 'EditUser', params: { id: $store.state.user.id } }"
          >Edit User</router-link
        >
        <button @click="logout()" class="button is-danger">Log out</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "MyAccount",
  methods: {
    async logout() {
      await axios
        .post("/api/v1/token/logout/")
        .then((response) => {
          console.log("LogOut Successfully");
        })
        .catch((error) => {
          console.log(JSON.stringify(error));
        });
      axios.defaults.headers.common["Authorization"] = "";
      localStorage.removeItem("token");
      localStorage.removeItem("username");
      localStorage.removeItem("userId");
      localStorage.removeItem("team_name");
      localStorage.removeItem("team_id");
      this.$store.commit("removeToken");

      this.$router.push("/");
    },
  },
};
</script>