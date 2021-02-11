<template lang="html">
  <v-container class='half-rounded-card-bottom-only grey3 px-6 pt-0'>
    <v-row>
      <v-col :cols="5">
        <v-card height="100%" class="rounded-card small-text ">
          <v-card-title class="grey1 justify-center subtitle-1 pa-2">
            Investment Details
          </v-card-title>
          <v-container class="py-3 px-4">
            <v-form @submit.prevent="onSubmit" ref="form">
              <v-row v-if="template===true">
                <v-col >
                  <v-autocomplete
                    v-model="inv.name"
                    :items="investmentNames"
                    :return-object="true"
                    item-text="name"
                    dense
                    label="Investment Name"/>
                </v-col>
              </v-row>

                <v-row dense >
                  <v-col>
                    <v-text-field
                      hide-details="auto"
                      :rules="$rulePercentage"
                      label="Fee"
                      type="number"
                      suffix="%"
                      :value="getPercentage(inv, 'investment_fee')"
                      @change="setPercentage($event, inv, '_investment_fee')"
                    />
                  </v-col>
                  <v-col>
                    <v-text-field
                    hide-details="auto"
                    :rules="$rulePercentage"
                    label="Buy spread"
                    type="number"
                    suffix="%"
                    :value="getPercentage(inv, 'buy_spread')"
                    @change="setPercentage($event, inv, 'buy_spread')"
                   />
                  </v-col>
                  <v-col>
                    <v-text-field
                    hide-details="auto"
                    :rules="$rulePercentage"
                    label="Sell spread"
                    type="number"
                    suffix="%"
                    :value="getPercentage(inv, 'sell_spread')"
                    @change="setPercentage($event, inv, 'sell_spread')" />
                  </v-col>
                </v-row>
                <v-row dense>
                  <v-col>
                    <v-autocomplete
                      class="pt-2"
                      hide-details
                      clearable
                      :value="inv.investment_class"
                      @input="(inv.investment_class = $event) && (inv.investment_class_id = $event.id)"
                      :items="investmentClassList"
                      item-text="name"
                      return-object
                      placeholder="Investment class"/>
                  </v-col>
                </v-row>
                <v-row dense>
                  <v-col>
                    <v-checkbox
                      dense
                      class="checkbox-small-label"
                      v-model="inv.cash"
                      hide-details
                      label="Cash Account"></v-checkbox>
                  </v-col>
                  <v-col>
                    <v-checkbox
                      class="checkbox-small-label"
                      dense
                      v-model="inv.TD"
                      hide-details
                      label="Term Deposit"></v-checkbox>
                  </v-col>
                </v-row>
                <v-row dense v-if="platformFees.length > 1">
                  <v-col>
                    <v-select
                      class="smalltext"
                      hide-details
                      :value="inv.platform_fee_group_name"
                      @input="overrideFeeGroup($event)"
                      :items="platformFees"
                      item-text="description"
                      return-object
                      label="Fee Group"/>
                  </v-col>
                  <v-col :cols="4">
                    <v-checkbox
                      class="checkbox-small-label"
                      dense
                      v-model="inv.override_fee_group"
                      hide-details
                      label="Override"></v-checkbox>
                  </v-col>
                </v-row>
                <v-row v-if="template===true">
                  <v-col>
                    <v-text-field
                    label="APIR Code"
                    dense
                    v-model="inv.APIR_code" />
                  </v-col>
                  <v-col>
                    <v-text-field
                    label="ASX Code"
                    dense
                    v-model="inv.ASX_code" />
                  </v-col>
                  <v-col>
                    <v-text-field
                    label="Other Code"
                    dense
                    v-model="inv.other_code" />
                  </v-col>
                </v-row>
                <v-row v-if="template==true">
                  <v-col>
                    <v-autocomplete
                      label="Platform Limitation"
                      dense
                      v-model="inv.platform_limitation"
                      :items="platforms"
                      item-text="name"
                      item-value="id"
                    />
                  </v-col>
                </v-row>
              </v-form>
            </v-container>
          </v-card>
        </v-col>
        <v-col v-if="!template" :cols="7">
          <v-card class="rounded-card small-text">
            <v-row class="grey1 ma-0 pa-0">
              <v-col :cols="2" class="ma-0 pa-0">
              </v-col>
              <v-col :cols="8" class="justify-center ma-0 pa-0">
                <v-card-title class="grey1 justify-center subtitle-1 pa-2">
                  Asset Allocation
                </v-card-title>
              </v-col>
              <v-col :cols="2" class="ma-0 pa-0 pr-4">
                <v-menu
                  class="transparent"
                  v-model="menu"
                  :close-on-content-click="false"
                  :close-on-click="false"
                  offset-x
                  >
                  <template v-slot:activator="{ on }">
                    <v-card-actions>
                      <v-spacer />
                      <v-btn icon small
                        v-on="on"
                        style="z-index:0"
                        >
                        <v-icon
                          color="teal"
                          dark
                          icon>
                        mdi-circle-edit-outline
                        </v-icon>
                      </v-btn>
                    </v-card-actions>
                  </template>
                  <v-card class="rounded-card small-text">
                    <v-form ref="aaForm">
                      <v-list  class="dialog-header dense">
                        <v-list-item  style="min-height:30px">
                          <v-list-item-title class="pa-0">Modify Asset Allocation</v-list-item-title>
                          <v-list-item-action>
                            <v-btn icon>
                              <v-icon>mdi-save</v-icon>
                            </v-btn>
                          </v-list-item-action>
                        </v-list-item>
                      </v-list>
                      <v-list >
                        <v-list-item
                          v-for="aa in uniqueAA"
                          :key="aa.id">
                          <v-list-item-content style="font-size:13px" class="small-text">{{aa.custom_name}}</v-list-item-content>
                          <v-list-item-action class="my-0" style="width:33%">
                            <v-text-field
                              dense
                              rounded solo
                              suffix="%"
                              :value="getAAPercentage(aa)"
                              @change="setAAPercentage($event, aa)"
                              @input="validateAA()"
                              hide-details
                              :rules="rulePercTo100"
                              type="number"
                            />
                          </v-list-item-action>
                        </v-list-item>
                      </v-list>
                      <v-divider></v-divider>
                      <v-card-actions>
                        <v-card-text class="pa-2 red--text">
                        {{aaError}}
                      </v-card-text>

                        <v-spacer></v-spacer>

                        <v-btn
                          class="mr-4"
                          style="width:80px"
                          color="primary"
                          rounded small
                          @click="hideAATab"
                        >
                          Hide
                        </v-btn>
                      </v-card-actions>
                    </v-form>
                  </v-card>
                </v-menu>
            </v-col>
</v-row>

            <InvestmentAAChartSummary
              :RPAANames="customRPAANames"
              :aaSummary="aaSummary"
            />
          </v-card>
        </v-col>
      </v-row>
      <v-card-actions>
        <v-spacer></v-spacer>
          <v-btn width="80" small @click="onSubmit" color="primary" rounded><span class="font-weight-light">Save</span></v-btn>
      </v-card-actions>
    </v-container>
</template>

<script>
import { apiService } from "@/common/api.service.js";

import {
  PLATFORM_AA_FETCH
} from "@/store/actions.type";
import { mapGetters } from "vuex";
import { rulePercTo100, rulePercentage } from "@/components/mixins/Rules.js";

import InvestmentAAChartSummary from "@/components/InvestmentAAChartSummary.vue";

export default {
  name: "InvestmentDetail",
  mixins: [rulePercTo100, rulePercentage],
  props: {
    investment: {
      type: Object,
      required: false,
      default: function() {
        return {
          id: null,
          custom_name: null,
          investment_class: null,
          amount: null,
          investment_fee: null,
          _investment_fee: null,
          buy_spread: null,
          sell_spread: null,
          cash: false,
          TD: false,
          override_fee_group: false,
        }
      },
    },
    template: {
      type: Boolean,
      required: false
    },
    investmentClassList: {
      type: Array,
      required: true
    },
    platformFees: {
      type: Array,
      required: false
    }
  },
  components: {
    InvestmentAAChartSummary,
  },
  data() {
    return {
      menu: false,
      aaError: null,
      dialog: false,
      platforms: null,
      aaSummary: null,
      aa: null,
    };
  },
  computed: {
    ...mapGetters(["activeScenario", "activePlatform","investmentNames"]),
    rulePercTo100() {
      return  [v => {
        if ((v <= 100) && (v >= 0)) {
          return true
        } else {
          return "Must be between 0% and 100"
        }
      }]
    },
    inv: {
      get() {
        return this.investment
      },
      set(newInvestment) {
        return newInvestment
      }
    },
    customRPAANames() {
      if (!this._.isEmpty(this.aaSummary)) {

        let custom_names = this.aaSummary.map(a => a.custom_name);
        let aanames = [...new Set(custom_names)];
        return aanames
        // return this.aaSummary.map(e => e.custom_name);
      } else {
        return []
      }
    },
    clearAA() {
      if (!this._.isEmpty(this.aa) && !this._.isEmpty(this.aaSummary) ) {
        // If an investment has any asset allocation names which do not match
        // the default RP AA Names (AASummary.name), this computed prop will
        // trigger a signal on save to clear all existing asset allocations
        // and replace them with default RP AA Names.
        let defaultRPAANames = this.aaSummary.map(e => e.name);
        let cleanAANames = this.aa.filter(e => e.name != null)
        let AANames = cleanAANames.map(e => e.name.name);
        return (AANames.some(e => !defaultRPAANames.includes(e)))
      } else {
        return true
      }
    },
    rebuiltAA() {
      if (this.clearAA) {
        let rebuiltAA = new Array;
        for (let aa of this.aaSummary) {
          let item = new Object;
          item['name_id'] = null;
          item['rp_name_id'] = aa.id
          item['investment'] = this.inv.id;
          if (aa.aa_total_perc) {
            item['percentage'] = (aa.aa_total_perc).toFixed(6);
          } else {
            item['percentage'] = 0
          }
          item['name'] = new Object();
          item.name['name'] = aa.name;
          if (item['percentage'] > 0) {
            rebuiltAA.push(item)
          }
        }
        return rebuiltAA
      } else {
        return null
      }
    },
    uniqueAA() {
      if (!this._.isEmpty(this.aaSummary)) {
        let unique = [];
        for (const aa of this.aaSummary) {
          if (!this._.isEmpty(unique)) {
            // Checks for existence of the current iterated item's custom_name in the unique list
            let found = unique.some(x => x.custom_name === aa.custom_name);
            if (!found) {
              //If no match, add it
              unique.push(aa);
            }
          } else {
            // If the unique list does not yet exist, add the first item in the aa array
            unique.push(aa);
          }
        }
        return unique
      } else {
        return []
      }
    },
    customOrFull() {
      if (this.inv.custom_name != null) {
        return this.inv.custom_name
      } else {
        return this.inv.name.name
      }
    }
  },
  watch: {
    inv() {
      this.getAAData();
      if (this.template === true) {
        this.inv.template = true;
        this.getPlatformList();
      }
    }
  },
  methods: {
    validateAA() {
      if (this.$refs.aaForm.validate()){
        this.clearAAError();
        return true
      } else {
        this.setAAError();
        return false;
      }
    },
    clearAAError() {
      this.aaError = null;
    },
    setAAError(){
      this.aaError = "Must be between 0% and 100";
    },
    setAAPercentage(event, uniqueSummaryItem) {
      if (this.validateAA()) {
        let aaSummaryItem = this.aaSummary.find(x => x.id === uniqueSummaryItem.id)
        // Checks for merged items that are not shown on the unique aa list
        // That is, merged items that are essentailly "hidden".
        // There will always be one merged item that is not hidden
        let mergedAASummaryItems = this.aaSummary.filter(
          x => (x.id != uniqueSummaryItem.id) && (x.custom_name === uniqueSummaryItem.custom_name) )
        // If there are merged items, clear their values
        if (!this._.isEmpty(mergedAASummaryItems)) {
          for (let item of mergedAASummaryItems) {
            item.aa_total_perc = 0
            const idx = this.aa.findIndex(x => x.rp_name_id === item.id);
            if (idx >= 0) {
              this.aa[idx].percentage = 0;
            }
          }
        }
        if (this.clearAA) {
          // If AA is being cleared, edit the aaSummary array directly.
          // This will also update the rebuiltAA computed property for API call
          aaSummaryItem.aa_total_perc = event/100;
        } else {
          // Add to aaSummary so it updates chart etc
          aaSummaryItem.aa_total_perc = event/100;

          let aa_item = this.aa.find(x => x.name.name === aaSummaryItem.name);
          // Looks for the aa item in the aa array that matches the RPAA name
          if (aa_item != null) {
            // If it finds it, sets the value
            aa_item.percentage = event/100;
          } else {
            // If it can't find it in the array, creates a new entry
            let new_aa_item = new Object()
            new_aa_item['name_id'] = null;
            new_aa_item['rp_name_id'] = aaSummaryItem.id
            new_aa_item['investment'] = this.inv.id;
            new_aa_item['percentage'] = event/100;
            new_aa_item['name'] = new Object();
            new_aa_item.name['name'] = aaSummaryItem.name;
            if (event > 0) {
              this.aa.push(new_aa_item)
            }
          }
        }
      }
    },
    getAAPercentage(aa) {
      const filterArr = this.aaSummary.filter(
        x => x.custom_name === aa.custom_name)
      // creates an array with the found items
      const percentageArr = filterArr.map(a => a.aa_total_perc);
      if (!this._.isEmpty(percentageArr)) {
        // If the found item array has value, sums the items
        const percentageTotal = percentageArr.reduce((acc, curVal) =>
          Number(acc) + Number(curVal))
        return (percentageTotal*100).toFixed(2);
      } else {
        // If no data is found, adds 0 to the array to maintain data order.
        return 0
      }
      // return (result*100).toFixed(2);
    },
    setPercentage(event, inv, field) {
      this.inv[field] = (event/100).toFixed(6);
    },
    getPercentage(inv, field) {
      return +(this.inv[field]*100).toFixed(2);
    },
    getAASummaryData() {
      if (this.template === false) {
        let endpoint = `/api/scenarios/${this.activeScenario.id}/platforms/${this.activePlatform.id}/investments/${this.inv.id}/aasummary/`;
        apiService(endpoint).then(data => {
            this.aaSummary = data.results;
            this.getAAData();
        })
      }
    },
    getAAData() {
      if (this.template === false) {
        let endpoint = `/api/scenarios/${this.activeScenario.id}/platforms/${this.activePlatform.id}/investments/${this.inv.id}/aa/`;
        apiService(endpoint).then(data => {
            this.aa = data.results;
        });
      }
    },
    hideAATab(){
      if (this.validateAA()){
        this.menu = false;
      }
    },
    overrideFeeGroup(event) {
      this.inv.platform_fee_group = event.id;
      this.inv.override_fee_group = true;
    },
    onSubmit() {
      // Vuetify does not support nested forms, so check if the aaError message
      // exists as a form of validation
      if (!this.aaError && this.$refs.form.validate()) {

        if (this.template === false) {
          let invObj = this.inv
          if (this.clearAA) {
            // Adds a new aa array to the investment if the old one is to be
            // cleared
            invObj['clear_aa'] = this.clearAA;
            invObj['asset_allocations'] = this.rebuiltAA;
          } else {
            // Otherwise adds the existing aa array
            invObj['asset_allocations'] = this.aa;
          }
          for (let aa of invObj.asset_allocations) {
              aa.name = aa.name.id
          }
          let endpoint = `/api/scenarios/${this.activeScenario.id}/platforms/${this.activePlatform.id}/investments/${this.inv.id}/`;
          apiService(endpoint, "PATCH", invObj).then(data => {
            this.inv = data;
            console.log(data);
            this.getAASummaryData();
            this.getActivePlatformAA();
          });

        } else {
          let endpoint = `/api/investmenttemplate/${this.inv.id}/`;
          apiService(endpoint, "PATCH", this.inv)
        }
      }
    },
    getActivePlatformAA() {
      // Refreshes the platform aa chart when an investment is saved
      this.$store.dispatch(PLATFORM_AA_FETCH, {
        'scenarioId': this.activeScenario.id,
        'platformId': this.activePlatform.id,
      })
    },
    getPlatformList() {
      if (this.template === true) {
        let endpoint = `/api/platformnames/`;
        apiService(endpoint, "GET").then(data => {
          this.platforms = data.results;
        });
      }
    },
  },
  mounted() {
    this.getAASummaryData();
    this.getPlatformList();
  }
};
</script>
<style scoped>
  div.v-menu__content {
    border-radius: 40px !important;
  }
  .v-input >>> .v-select__selections {
    font-size: .8rem !important;
  }
  .v-list >>> .v-list-item__title {
    font-size: .8rem !important;
  }
</style>
