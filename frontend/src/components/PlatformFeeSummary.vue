<template lang="html">
  <v-dialog v-model="dialog">
    <template v-slot:activator="{ on }" >
      <v-list-item
        v-on="on">
        <v-list-item-title >
          {{platformFee.description}}
        </v-list-item-title>
      </v-list-item>
    </template>
  <v-card>
    <v-card-title class="headline grey lighten-2 pr-3">
      Fee Detail
      <v-spacer></v-spacer>
      <v-btn
        color="secondary"
        text
        @click="dialog = false"
      >X</v-btn>
    </v-card-title>
    <v-container class="pa-3">

    <v-form
      @submit.prevent="onSubmit"
      v-if="platformFee != null"
      ref="form">
      <v-row >
        <v-col >
          <v-card height="100%">
            <v-row>
              <v-col :cols="5">
                <v-card-title>
                  {{platformFee.description}}
                </v-card-title>
              </v-col>
              <!-- <v-col  :cols="3">
                <v-card-title class="justify-end pr-0">
                  Total Fees
                </v-card-title>
              </v-col> -->

            </v-row>
            <v-card-text class="pt-0">
              <v-select
                clearable
                :items="getReadableList('admin_fee_structure')"
                @change="convertToRealName('admin_fee_structure', $event)"
                :value="convertLongName('admin_fee_structure')"
                hide-details
                label="Sliding admin fee structure"
              />
              <v-text-field
                suffix="%"
                type='number'
                hide-details='auto'
                :value="getPerc('admin_fee_rebate')"
                @change="setPerc('admin_fee_rebate', $event)"
                label="Admin fee rebate"
                :rules="$rulePercentage"
              />
              <v-select
                clearable
                :items="getReadableList('admin_fee_exclusions')"
                @change="convertToRealName('admin_fee_exclusions', $event)"
                :value="convertLongName('admin_fee_exclusions')"
                hide-details
                label="Admin fee exclusions"
              />
              <v-text-field
                v-if="template === true"
                hide-details
                v-model="platformFee.fee_group_order"
                label="Fee group order"
              />
              <v-select
                clearable
                v-if="template === true"
                hide-details
                :multiple="true"
                :items="AFSLList"
                item-value="id"
                item-text="name"
                v-model="platformFee.AFSL_limitation"
                label="AFSL Limitation"
              />
              <v-select
                clearable
                v-if="template === true"
                hide-details
                :multiple="true"
                :items="investmentClassList"
                item-value="id"
                item-text="name"
                v-model="platformFee.allowed_investment_classes"
                label="Allowed Investment Classes"
              />
              <span v-if="template === true">
                {{platformFee.platform}} {{platformFee.id}}
              </span>
            </v-card-text>
              <v-card outlined tile class="ma-4">
                <v-row dense>
                  <v-col :cols="6">
                    <v-card-text class="pa-2">
                      Fee Caps
                    </v-card-text>
                  </v-col>
                  <v-col :cols="3">
                    <v-card-text class="pa-2">
                      Minimum
                    </v-card-text>
                  </v-col>
                  <v-col :cols="3">
                    <v-card-text class="pa-2">
                      Maximum
                    </v-card-text>
                  </v-col>
                </v-row>
                <v-row dense>
                  <v-col :cols="6">
                    <v-card-text class="pa-2">
                      Admin Fee
                    </v-card-text>
                  </v-col>
                  <v-col :cols="3">
                    <v-currency-field
                      hide-details='auto'
                      prefix="$"
                      :decimal-length="2"
                      dense solo
                      v-model="platformFee.minimum_admin_fee"
                      type="number"
                      :rules="$rule4Digits"
                    />
                  </v-col>
                  <v-col :cols="3">
                    <v-currency-field
                      hide-details='auto'
                      prefix="$"
                      :decimal-length="2"
                      dense solo
                      v-model="platformFee.maximum_admin_fee"
                      type="number"
                      :rules="$rule6Digits"
                    />
                  </v-col>
                </v-row>
                <v-row dense>
                  <v-col :cols="6">
                    <v-card-text class="pa-2">
                      Total Fees
                    </v-card-text>
                  </v-col>
                  <v-col :cols="3">
                    <v-currency-field
                      hide-details='auto'
                      prefix="$"
                      :decimal-length="2"
                      dense solo
                      v-model="platformFee.minimum_total_fee"
                      type="number"
                      :rules="$rule4Digits"
                    />
                  </v-col>
                  <v-col :cols="3">
                    <v-currency-field
                      hide-details='auto'
                      prefix="$"
                      :decimal-length="2"
                      dense solo
                      v-model="platformFee.maximum_total_fee"
                      type="number"
                      :rules="$rule6Digits"
                    />
                  </v-col>
                </v-row>
              </v-card>

          </v-card>
        </v-col>
        <v-col>
          <v-card class="pa-4">

          <v-row
            v-for="item in displayItems"
            :key="item[0].value"
            dense no-gutters>
            <v-col :cols="descriptionCol(item)">
              <v-card outlined tile dense>
                <v-card-text class="pa-2" >
                  {{ item[0] }}
                </v-card-text>
              </v-card>
            </v-col>
            <v-col v-if="item[2] != null || item[1] == 'sliding_admin_fee'" :cols="3">
              <v-card outlined tile  v-if="item[2] != null">
                <v-text-field
                  v-if="item[2] != null"
                  dense solo
                  :value = "getPercentage(item)"
                  @change = "setPercentage($event, item)"
                  suffix="%"
                  type='number'
                  hide-details='auto'
                  :rules="$rulePercentage"
                />
              </v-card>
              <ModifyTierFees
                v-if="item[1]=='sliding_admin_fee'"
                :platformFee="platformFee"
                :platform="platform"
                :template="template"
              />
            </v-col>
            <v-col :cols="3">
              <v-card outlined tile dense>
                <v-currency-field
                  v-if="(item[1] === 'sliding_admin_fee') || item[1] === 'investment_fee'"
                  dense solo
                  v-model="platformFee[item[1]]"
                  prefix="$"
                  type='number'
                  hide-details='auto'
                  disabled
                />
                <template v-else-if="item[1] === 'low_balance_refund'">
                  <v-currency-field
                    v-if="platformFee.platform_fee_total < 6000"
                    dense solo
                    v-model="platformFee[item[1]]"
                    prefix="$"
                    type='number'
                    hide-details='auto'
                    disabled
                  />
                </template>
                <v-currency-field
                  v-else-if="item[1] === 'admin_fee_dollar_calculated'"
                  dense solo
                  :value="platformFee['admin_fee_dollar_calculated'] ? platformFee['admin_fee_dollar_calculated'] : 0"
                  @change="(platformFee['admin_fee_dollar_calculated'] = $event) && (platformFee['admin_fee_dollar'] = $event)"
                  prefix="$"
                  type='number'
                  hide-details='auto'
                  :rules="$rule4Digits"
                />
                <v-currency-field
                  v-else-if="item[2] === null"
                  dense solo
                  :value="platformFee[item[1]] ? platformFee[item[1]] : 0"
                  @change="platformFee[item[1]] = $event"
                  prefix="$"
                  type='number'
                  hide-details='auto'
                  :rules="$rule4Digits"
                />
                <v-currency-field
                  v-else
                  dense solo
                  @change="setPercFromAmount(item, $event)"
                  :value="platformFee[item[1]] ? platformFee[item[1]] : 0"
                  prefix="$"
                  type='number'
                  hide-details='auto'
                  :rules="$rule4Digits"
                />
              </v-card>
            </v-col>
          </v-row>
          <v-divider class="my-4"/>
          <v-row dense no-gutters>
            <v-col :cols="9" dense>
              <v-card outlined tile dense>
                <v-card-title class="pa-2 h4">
                  <strong>
                  Total Fees
                  </strong>
                  <v-spacer></v-spacer>
                  <v-tooltip bottom @click.stop>
                    <template v-slot:activator="{ on }">
                      <v-btn
                        icon
                        @click="onSubmit()"
                        v-on="on"  >
                        <v-icon >
                          mdi-calculator
                        </v-icon>
                      </v-btn>
                    </template>
                    <span>
                      Recalculate
                    </span>
                  </v-tooltip>
                </v-card-title>
              </v-card>
            </v-col>
            <!-- <v-col :cols="1" dense class="">

            </v-col> -->
            <v-col :cols="3" dense class="">
              <v-currency-field
                height="100%"
                readonly
                prefix="$"
                hide-details dense solo
                v-model="platformFee.platform_fee_total_fees"
              />
            </v-col>


          </v-row>
        </v-card>
        </v-col>
      </v-row>
      <v-row dense>
        <v-col class="text-right" dense>
          <v-btn @click="saveAndClose()" color="primary" class="ml-4">
            Save
          </v-btn>
        </v-col>
      </v-row>
    </v-form>
  </v-container>
</v-card>

</v-dialog>
</template>

<script>
import { apiService } from "@/common/api.service.js";
import ModifyTierFees from "@/components/ModifyTierFees.vue";
import { rule4Digits, rule6Digits, rule7Digits, rulePercentage } from "@/components/mixins/Rules.js";
import { mapGetters } from "vuex";

export default {
  name: "PlatformFeeSummary",
  mixins: [rule4Digits, rule6Digits, rule7Digits, rulePercentage],
  props: {
    platformFee: {
      type: Object,
      required: true,
    },
    platform: {
      type: Number,
      required: false,
    },
    template: {
      type: Boolean,
      required: false,
    },
    investmentClassList: {
      type: Array,
      required: false,
    },
  },
  components: {
    ModifyTierFees,
  },
  data() {
    return {
      dialog: false,
      keepOpen: true,
      AFSLList: [],
      displayItems: [
          ["Investment fees","investment_fee",null],
          ["Sliding administration fee","sliding_admin_fee",null],
          ["Administration fee (flat)","admin_fee_dollar_calculated", null],
          ["Administration fee (floating)","admin_fee_percentage_calculated", "admin_fee_percentage"],
          ["Expense recovery fee (flat)","expense_recovery_dollar", null],
          ["Expense recovery fee (floating)", "expense_recovery_percentage_calculated", "expense_recovery_percentage"],
          ["ORR Levy", "ORR_levy_calculated", "ORR_levy"],
          ["Fund accounting fee (flat)", "fund_accounting_fee_dollar", null],
          ["Fund accounting fee (floating)","fund_accounting_fee_percentage_calculated","fund_accounting_fee_percentage"],
          ["Trustee fee","trustee_fee_calculated", "trustee_fee"],
          ["Issuer fee", "issuer_fee_calculated", "issuer_fee"],
          ["SMA admin fee", "sma_admin_fee", null],
          ["Low balance refund", "low_balance_refund", null],
        ],
        displayAdminItems: [
          //format is ["field name", "friendly name", "editable by", "type", "tooltip"]
          ["fee_group_order","Fee group order","admin","number",null],
          ["admin_fee_structure", "Sliding fee structure","admin","list", null],
          ["admin_fee_rebate", "Admin fee rebate", "admin", "number", null],
          ["minimum_admin_fee", "Minimum admin fee", "admin", "number", null],
          ["maximum_admin_fee", "Maximum admin fee", "admin", "number", null],
          ["minimum_total_fee", "Minimum total fee", "admin", "number", null],
          ["maximum_total_fee", "Maximum total fee", "admin", "number", null],
          ["admin_fee_exclusions", "Admin fee exclusions", "admin", "list", null],
        ],
    };
  },
  computed: {
    ...mapGetters(["activeScenario", "activeUser", "activePlatform", "platformNames"]),
  },
  methods: {
    setPercFromAmount(item, event) {
      this.platformFee[item[1]] = event;
      this.platformFee[item[2]] = (event / this.platformFee.platform_fee_total).toFixed(6);
    },
    setPerc(prop, event) {
      this.platformFee[prop] = (event/100).toFixed(6)
    },
    getPerc(prop) {
      if (this.platformFee[prop] > 0) {
        return (this.platformFee[prop]*100).toFixed(2);
      } else {
        return null
      }
    },
    descriptionCol(item) {
      if (item[2] != null || item[1] == 'sliding_admin_fee') {
        return 6
      } else {
        return 9
      }
    },
    getReadableList(item){
      let list = this.platformFee[this.joinList(item)];
      let cleanList = [];
      for (let i=0; i<list.length; i++) {
        cleanList.push(list[i][1]);
      }
      return cleanList
    },
    convertLongName(item){
      let list = this.platformFee[this.joinList(item)];
      let realName = "";
      for (let i=0; i<list.length; i++) {
        if (this.platformFee[item] == list[i][0]) {
          realName = list[i][1];
        }
      }
      return realName;
    },
    convertToRealName(item, event){
      if (event == undefined) {
        this.platformFee[item] = ""
      } else {
      let list = this.platformFee[this.joinList(item)];
        let realName = "";
        for (let i=0; i<list.length; i++) {
          if (event == list[i][1]) {
            realName = list[i][0];
            this.platformFee[item] = realName;
          }
        }
      }
    },
    joinList(item){
      return item.concat("_list");
    },
    setPercentage(event, item) {
      this.platformFee[item[1]] = event / 100 * this.platformFee.platform_fee_total;
      this.platformFee[item[2]] = (event/100).toFixed(6);
    },
    getPercentage(item) {
      return (this.platformFee[item[2]]*100).toFixed(2)
    },
    getAFSLList(){
      if (this.template===true)  {
        let endpoint = `/api/afsls/`;
        apiService(endpoint, "GET").then(data => {
          this.AFSLList = data.results;
        });
      };
    },
    saveAndClose() {
      this.keepOpen = false;
      this.onSubmit();
    },
    onSubmit() {
      if (this.$refs.form.validate()) {
        let endpoint = null;
        if (this.template===true) {
          endpoint = `/api/platformtemplates/${this.platform}/fees/${this.platformFee.id}/`
        } else {
          endpoint = `/api/scenarios/${this.activeScenario.id}/platforms/${this.activePlatform.id}/platformfees/${this.platformFee.id}/`;
        }
        apiService(endpoint, "PATCH", this.platformFee).then(data => {
          this.$emit("modify-fees", data);
          this.platformFee.platform_fee_total_fees = data.platform_fee_total_fees;
          if (!this.keepOpen) {
            this.dialog=false
          }
        });
      }
    },
  },
  mounted() {
    this.getAFSLList();
  }
};
</script>
<style>
  .v-input .v-input__control .v-input__slot .v-text-field__slot input::-webkit-outer-spin-button,
  .v-input .v-input__control .v-input__slot .v-text-field__slot input::-webkit-inner-spin-button
  {
  -webkit-appearance: none;
  margin: 0;
  }
</style>
