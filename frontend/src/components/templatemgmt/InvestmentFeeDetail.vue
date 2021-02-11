<template lang="html">
  <v-container >
  <v-form @submit.prevent="onSubmit">
    <v-card class="pa-2">
      <v-row>
        <v-col>
          {{ platform.name.name }}
        </v-col>
        <v-col>
          Fee
        </v-col>
        <v-col>
          Buy Spread
        </v-col>
        <v-col>
          Sell Spread
        </v-col>
      </v-row>
      <v-row v-for="inv in investments" :key="inv.id" dense>
        <v-col>
          {{inv.name.name}}
        </v-col>
        <v-col>
          <v-text-field
            number
            dense solo hide-details
            :value = "getfee(inv)"
            @change = "setfee(inv, $event)"
          />
        </v-col>
        <v-col>
          <v-text-field
            number
            dense solo hide-details
            :value = "getbuy(inv)"
            @change = "setbuy(inv, $event)"
          />
        </v-col>
        <v-col>
          <v-text-field
            number
            dense solo hide-details
            :value = "getsell(inv)"
            @change = "setsell(inv, $event)"
          />
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-btn type="submit" color="primary">
            Save
          </v-btn>
        </v-col>
      </v-row>
    </v-card>
  </v-form>
</v-container>
</template>

<script>
import { apiService } from "@/common/api.service.js";

export default {
  name: "InvestmentFeeDetail",
  props: {
    platform: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      investments: [],
      next: null,
      total: 0,
    };
  },
  watch: {
    platform() {
      this.investments = []
      this.getInvestments();
    },
  },
  methods: {
    getfee(inv){
      return +(inv.investment_fee*100).toFixed(6)
    },
    setfee(inv, event) {
      let idx = this.investments.findIndex(i => i.id === inv.id);
      this.investments[idx].investment_fee = +(event/100).toFixed(6);
      this.investments[idx]._investment_fee = +(event/100).toFixed(6);
    },
    getbuy(inv){
      return +(inv.buy_spread*100).toFixed(6)
    },
    setbuy(inv, event) {
      let idx = this.investments.findIndex(i => i.id === inv.id);
      this.investments[idx].buy_spread = +(event/100).toFixed(6);
    },
    getsell(inv){
      return +(inv.sell_spread*100).toFixed(6)
    },
    setsell(inv, event) {
      let idx = this.investments.findIndex(i => i.id === inv.id);
      this.investments[idx].sell_spread = +(event/100).toFixed(6);
    },
    getInvestments() {
      let endpoint = null
      if (this.next) {
        endpoint = this.next;
      } else {
        endpoint = `/api/platformnames/${this.platform.name.id}/investments/`;
      }
      apiService(endpoint, "GET").then(data => {
        this.investments.push(...data.results);
        if (data.next) {
          this.next = data.next;
          this.getInvestments();
        } else {
          this.next = null;
        }
      });
    },
    onSubmit() {
      for (let i=0; i<this.investments.length; i++) {
        let endpoint = `/api/platformnames/${this.platform.name.id}/investments/${this.investments[i].id}/`;
        apiService(endpoint, "PATCH", this.investments[i]).then(data => {
          this.investments[i] = data;
          console.log("Saved: "+this.investments[i].name.name)
        });
      }
    }
  },
  mounted() {
    this.getInvestments();
  }
};

</script>
