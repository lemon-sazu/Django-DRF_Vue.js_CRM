<template>
  <div class="container">
    <div class="columns is-multiline">
      <div class="column is-12">
        <h1 class="title">Plan</h1>
      </div>
      <div class="column is-4">
        <div class="box">
          <h2 class="subtitle">Free</h2>
          <h4 class="is-size-3">$0</h4>

          <p>Max Clients - 5</p>
          <p>Max Leads - 5</p>

          <button @click="subscribe('free')" class="button is-primary mt-5">
            Subscribe
          </button>
        </div>
      </div>
      <div class="column is-4">
        <div class="box">
          <h2 class="subtitle">Small Team</h2>
          <h4 class="is-size-3">$10</h4>

          <p>Max Clients - 15</p>
          <p>Max Leads - 15</p>
          <button
            @click="subscribe('smallteam')"
            class="button is-primary mt-5"
          >
            Subscribe
          </button>
        </div>
      </div>
      <div class="column is-4">
        <div class="box">
          <h2 class="subtitle">Big Team</h2>
          <h4 class="is-size-3">$25</h4>

          <p>Max Clients - 50</p>
          <p>Max Leads - 50</p>
          <button @click="subscribe('bigteam')" class="button is-primary mt-5">
            Subscribe
          </button>
        </div>
      </div>
      <hr />
      <div class="column is-12">
        <button @click="cancelPLan()">Cancel Plan</button>
      </div>
    </div>
  </div>
</template>
<script>
import axios from "axios";
import { toast } from "bulma-toast";
export default {
  name: "Plan",
  data() {
    return {
      pub_key: "",
      stripe: null,
    };
  },
  async mounted() {
    await this.getPubKey();

    this.stripe = Stripe(this.pub_key);
  },
  methods: {
    async getPubKey() {
      await axios.get("/api/v1/stripe/get_pub_key/").then((response) => {
        console.log(response);
        this.pub_key = response.data.pub_key;
      });
    },
    async cancelPLan() {
      this.$store.commit("setIsLoading", true);

      axios.post("/api/v1/teams/cancel_plan/").then((response) => {
        this.$store.commit("setTeam", {
          id: response.data.id,
          name: response.data.name,
          plan: response.data.plan.name,
          max_leads: response.data.plan.max_leads,
          max_clients: response.data.plan.max_clients,
        });
        toast({
          message: "The plan was Cancelled!",
          type: "is-success",
          dismissible: true,
          pauseOnHover: true,
          duration: 2000,
          position: "bottom-right",
        });
        this.$router.push("/dashboard/team/");
      });

      this.$store.commit("setIsLoading", false);
    },
    async subscribe(plan) {
      this.$store.commit("setIsLoading", true);
      const data = {
        plan: plan,
      };

      await axios
        .post("/api/v1/stripe/create_checkout_session/", data)
        .then((response) => {
          console.log(response);
          return this.stripe.redirectToCheckout({
            sessionId: response.data.sessionId,
          });
        })
        .catch((error) => {
          console.log("Error: ", error);
        });

      // await axios
      //   .post(`/api/v1/teams/upgrade_plan/`, data)
      //   .then((response) => {
      //     console.log("Working" + response);
      //     this.$store.commit("setTeam", {
      //       id: response.data.id,
      //       name: response.data.name,
      //       plan: response.data.plan.name,
      //       max_leads: response.data.plan.max_leads,
      //       max_clients: response.data.plan.max_clients,
      //     });
      //     toast({
      //       message: "The plan was Changed!",
      //       type: "is-success",
      //       dismissible: true,
      //       pauseOnHover: true,
      //       duration: 2000,
      //       position: "bottom-right",
      //     });
      //     this.$router.push("/dashboard/Thankyou/");
      //   })
      //   .catch((error) => {
      //     console.log(error);
      //   });

      this.$store.commit("setIsLoading", false);
    },
  },
};
</script>