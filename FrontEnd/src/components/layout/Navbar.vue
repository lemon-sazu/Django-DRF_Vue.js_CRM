<template>
  <nav class="navbar" role="navigation" aria-label="main navigation">
    <div class="navbar-brand">
      <router-link class="navbar-item" to="#">
        <strong>Mynul CRM</strong>
      </router-link>
    </div>

    <div id="navbarBasicExample" class="navbar-menu">
      <div class="navbar-end">
        <template v-if="$store.state.isAuthenticated">
          <router-link :to="{ name: 'Clients' }" class="navbar-item"
            >Clients</router-link
          >
          <router-link to="/dashboard/leads" class="navbar-item"
            >Leads</router-link
          >
          <router-link to="/dashboard/team" class="navbar-item"
            >Team</router-link
          >
        </template>
        <div class="navbar-item">
          <div class="buttons">
            <template v-if="!$store.state.isAuthenticated">
              <router-link class="button is-success" to="/sign-up">
                <strong>Sign up</strong>
              </router-link>
              <router-link class="button is-light" to="/log-in">
                Log in
              </router-link>
            </template>
            <template v-else>
              <router-link to="/my-account/" class="button is-info"
                >My account</router-link
              >
            </template>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>
<script>
export default {
  name: "Navbar",
};
</script>