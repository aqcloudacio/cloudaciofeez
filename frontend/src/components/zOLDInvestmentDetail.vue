<template lang="html">
  <v-dialog v-model="dialog">
    <template v-slot:activator="{ on }">
      <v-btn color="primary" dark v-on="on"><v-icon dark>
        mdi-magnify
      </v-icon>
    </v-btn>
    </template>
    <v-form  @submit.prevent="onSubmit">
      <v-container>
        <v-row>
          <v-col>
            <v-card>
              <v-card-title class="headline">
                {{ investment.custom_name ? investment.custom_name : investment.name.name }}
              </v-card-title>
              <v-card-subtitle class="headline">
                <template v-if="investment.investment_class">
                  {{ investment.investment_class.name }}
                </template>
                {{ investment.APIR_code }}{{ investment.ASX_code
                }}{{ investment.other_code }}
              </v-card-subtitle>
              <v-card-text>
                <v-currency-field
                  v-model="investment.amount"
                  label="Amount"
                  clearable outlined dense
                  prefix="$"
                  />
                <v-text-field
                  label="Investment Fee"
                  clearable outlined dense
                  suffix="%"
                  v-model="percentageFee"
                />
                  {{ +investment.buy_spread | toPercentage }} /
                  {{ +investment.sell_spread | toPercentage }}<br>
                 <p v-if="investment.cash">Nominated cash account</p>
                <p v-if="investment.TD">Term deposit</p>
              </v-card-text>
            </v-card>
          </v-col>
          <v-col>
            <v-card>
              <v-card-title>Asset Allocation</v-card-title>
              <v-card-text>
                  <span v-for="(value, key) in aaObj" :key="key">
                    {{key}}: {{value  | toPercentage}} <br>
                  </span>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
        <v-row>
          <v-btn type="submit" color="primary" dark dense>Update</v-btn>
        </v-row>
      </v-container>
    </v-form>
  </v-dialog>
</template>

<script>
import { apiService } from "@/common/api.service.js";

export default {
  name: "InvestmentDetail",
  inject: ["platformId", "scenarioId"],
  props: {
    investment: {
      type: Object,
      required: true
    },
  },
  data() {
    return {
      error: null,
      dialog: false,
      aaList: [],
    };
  },
  computed: {
    percentageFee: {
      get: function(){
        if (isNaN(this.investment.investment_fee)) {
          return "Enter numbers only"
        } else {
        return +(this.investment.investment_fee * 100).toFixed(2)
        }
      },
      set: function(newValue){
        if (isNaN(newValue)) {
          return null
        } else {
          this.investment.investment_fee = (newValue/100).toFixed(4);
        }
      }
    },
    aaObj: function (){
      var aaObject = {};
      for (let i = 0; i < this.aaList.length; i++) {
        let found = false;
        for (let x = 0; x < this.aaList[i].rp_aa_name.length; x++) {
          let aaName = this.aaList[i].rp_aa_name[x];
          if (aaName in aaObject) {
            aaObject[aaName] += this.aaList[i].rp_aa_percentage;
            found = true;
            break;
          }

          if (!found) {
            let key = this.aaList[i].rp_aa_name[x];
            let value = this.aaList[i].rp_aa_percentage;
            aaObject[key] = value;
            found = false;
          }
        }
      }
      return (aaObject)
    }
  },
  methods: {
    getAAData() {
      let endpoint = `/api/scenarios/${this.scenarioId}/platforms/${this.platformId}/investments/${this.investment.id}/aa/`;
      apiService(endpoint).then(data => {
        this.aaList = data.results;
      });
    },
    onSubmit() {
      let endpoint = `/api/scenarios/${this.scenarioId}/platforms/${this.platformId}/investments/${this.investment.id}/`;
      apiService(endpoint, "PATCH", {
        amount: this.investment.amount,
        investment_fee: this.investment.investment_fee
      });
    }
  },
  mounted() {
    this.getAAData();
  }
};
</script>
