<template lang="html">
  <v-form
    @submit.prevent="onSubmit"
    ref="form">
    <v-expansion-panels
      focusable
      multiple>
      <AddInvestment
        class="transparent"
        @add-investment="getInvestmentData"
        v-on="$listeners" />
      <v-expansion-panel v-for="investment in investments"
        class="transparent expansion-grey3-button py-0"
        :key="investment.id"
        dense>
        <v-expansion-panel-header class="px-3 py-2" @keyup.space.prevent >
          <v-row class="ma-0">
            <v-col
              @click.stop
              :cols="8"
              class="py-0 pl-0">
              <v-text-field
                class="rounded-card small-text"
                @click.stop
                @space.stop
                :value="investmentName(investment)"
                @input="addToChanged(investment, $event)"
                hide-details="auto"
                dense solo
                :rules="[v => !!(v) || 'You must enter an investment name']">
              </v-text-field>
            </v-col>
            <v-col
              @click.stop
              :cols="4"
              class="py-0 pl-0">
              <v-currency-field
                class="rounded-card small-text"
                @click.stop
                @input="addToChanged(investment)"
                v-model="investment.amount"
                hide-details="auto"
                prefix="$"
                :decimal-length="0"
                dense solo
                :rules="$rule8Digits">
                <template v-slot:append-outer>
                  <template  v-if="changeListID.includes(investment.id)">
                    <v-icon
                      color="teal"
                      @click.stop
                      @click="updateInvestment(investment)"
                    >mdi-check-circle-outline</v-icon>
                  </template>
                  <v-slide-x-reverse-transition
                     mode="out-in"
                     >
                     <DeleteObj
                       :objectType="'investment'"
                       :objectToDelete="investment"
                       :portfolioId="investment.portfolio"
                       @delete-object="deleteObj"
                       v-on="$listeners"
                     />
                  </v-slide-x-reverse-transition>
                </template>
              </v-currency-field>
            </v-col>
          </v-row>
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <InvestmentDetail
            :platformFees="platformFees"
             @add-investment="getInvestmentData"
             v-on="$listeners"
             :investment="investment"
             :investmentClassList="investmentClassList"
          />
        </v-expansion-panel-content>
    </v-expansion-panel>
    </v-expansion-panels>
    <v-row v-if="!(_.isEmpty(changeList))">
      <v-col class="text-right">
        <v-btn
          @click="onSubmit"
          color="primary"
          small
          rounded
          ><span class="font-weight-light">Update All Investments</span>
        </v-btn>
      </v-col>
    </v-row>
  </v-form>
</template>

<script>
import { apiService } from "@/common/api.service.js";
import AddInvestment from "@/components/AddInvestment.vue";
import InvestmentDetail from "@/components/InvestmentDetail.vue";
import DeleteObj from "@/components/DeleteObj.vue";
import { rule8Digits } from "@/components/mixins/Rules.js";

import {
  PLATFORM_AA_FETCH,
  PLATFORM_FETCH
} from "@/store/actions.type";
import { mapGetters } from "vuex";

export default {
  name: "InvestmentSummary",
  mixins: [rule8Digits],
  inject: ["platformId", "scenarioId"],
  props: {
    // Only passed as a prop so it can be watched and new investments called
    // when values changes (due to portfolio addition)
    platformTotal: {
      type: Number,
      required: true
    },
    platformFees: {
      type: Array,
      required: false,
    }
  },
  components: {
    AddInvestment,
    DeleteObj,
    InvestmentDetail
  },
  data() {
    return {
      error: null,
      investments: [],
      changeList: [],
      investmentClassList: [],
      editName: [],
      editAmount: [],
      duplicate: [],
    };
  },
  watch: {
    platformTotal() {
      this.getInvestmentData();
    },
  },
  computed: {
    ...mapGetters(["activeScenario", "activePlatform"]),
    changeListID() {
      return this.changeList.map(e => e.id);
    }
  },
  methods: {
    // stringToColour(str) {
    //   let hash = 0;
    //   for (let i = 0; i < str.length; i++) {
    //     hash = str.charCodeAt(i) + ((hash << 5) - hash);
    //   }
    //   let colour = '#';
    //   for (let i = 0; i < 3; i++) {
    //     let value = (hash >> (i * 8)) & 0xFF;
    //     colour += ('00' + value.toString(16)).substr(-2);
    //   }
    //   return colour;
    // },
    investmentName(inv) {
      if (inv.custom_name) {
        return inv.custom_name
      } else {
        return inv.name.name
      }
    },
    removeFromEdited(investment) {
      // Remove from changeList
      const i = this.changeList.findIndex(item => item.id === investment.id);
      this.changeList.splice(i,1)
    },
    addInvestment(investment) {
      this.investments.unshift(investment);
      this.duplicate.unshift(...{investment});
    },
    deleteObj(objectToDelete) {
      // Deletes the given item and removes it from the "changed" list
      this.removeFromChanged(objectToDelete)
      this.$delete(this.investments, this.investments.indexOf(objectToDelete));
    },
    addToChanged(investment, event) {
      if (event) {
        investment.custom_name = event;
      }
      // Add given investment to a list of investments that have changed.
      // This list is used to "save all" as well as show save ticks next to
      // investment summaries

      //  If it's unchanged from the original, remove it from the changed list
      if (!this.invIsChanged(investment)) {
        this.removeFromChanged(investment);
      } else if (!this.changeList.includes(investment)) {
        // else if it isn't already in the changeList, add it.
          this.changeList.push(investment);
      } else {
        // If it is changed, and is in the changeList, do nothing.
        //pass
      }
    },
    removeFromChanged(investment){
      // Removes given investment from the changelist
      const i = this.changeList.findIndex(item => item.id === investment.id);
      this.changeList.splice(i, 1);
    },
    invIsChanged(investment){
      // Checks the given investment against the original list of investments
      // to see if the amount or custom_name has changed.
      let original = this.duplicate.find(x => x.id === investment.id);
      if (((investment.custom_name || investment.name.name) === (original.custom_name || original.name.name))
        && (investment.amount == Number(original.amount)))
      {
        return false
      } else {
        return true
      }
    },
    validateInvestment(investment) {
      // Manual validation to block updating investments. Vuetify doesn't
      // support nested validation atm.
      return (investment.amount >= 0 && investment.amount < 10000000 && investment.custom_name)
    },
    updateInvestment(investment) {
      if (this.validateInvestment(investment)){
        let endpoint = `/api/scenarios/${this.scenarioId}/platforms/${this.platformId}/investments/${investment.id}/`;
        apiService(endpoint, "PATCH", {
          custom_name: investment.custom_name,
          amount: investment.amount,
        }).then(() => {
          this.removeFromEdited(investment);
          this.getActivePlatformAA();
          this.getActivePlatform();
        });
      }
    },
    async onSubmit() {
      if (this.$refs.form.validate()) {
        if (this.changeList) {
          for (let i=0; i < this.changeList.length; i++) {
            let endpoint = `/api/scenarios/${this.scenarioId}/platforms/${this.platformId}/investments/${this.changeList[i].id}/`;
            await apiService(endpoint, "PATCH", this.changeList[i])
          };
          this.getInvestmentData();
          this.getActivePlatformAA();
          this.getActivePlatform();
        };
      }
    },
    getActivePlatformAA() {
      // refreshes the platform aa chart when an investment is saved
      this.$store.dispatch(PLATFORM_AA_FETCH, {
        'scenarioId': this.activeScenario.id,
        'platformId': this.activePlatform.id,
      })
    },
    getActivePlatform() {
      // refreshes the platform aa chart when an investment is saved
      this.$store.dispatch(PLATFORM_FETCH, {
        'scenarioId': this.activeScenario.id,
        'platformId': this.activePlatform.id,
      })
    },
    getInvestmentData() {
      let endpoint = `/api/scenarios/${this.scenarioId}/platforms/${this.platformId}/investments/`;
      apiService(endpoint).then(data => {
        this.duplicate = JSON.parse(JSON.stringify(data.results));
        this.investments = data.results;
        this.changeList = [];
      });
    },
    getInvestmentClassList() {
      let endpoint = `/api/investmentclass/`;
      apiService(endpoint, "GET").then(data => {
        this.investmentClassList = data.results;
      });
    },
    // setCustomNames(){
    //   if (!this._.isEmpty(this.investments)) {
    //     for (let item of this.investments) {
    //       if (item.custom_name === "") {
    //         item.custom_name = item.name.name
    //       }
    //     }
    //     this.duplicate = JSON.parse(JSON.stringify(this.investments));
    //   }
    // }
  },
  mounted() {
    this.getInvestmentData();
    this.getInvestmentClassList();
  }
};
</script>
<style>
  .v-expansion-panel-content__wrap {
    padding: 0 !important;
  }
</style>
