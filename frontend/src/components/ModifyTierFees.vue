<template lang="html">
  <v-dialog v-model="tierDialog" width="700px">
    <template v-slot:activator="{ on }">
      <v-btn color="primary" v-on="on">
        <v-icon>
          mdi-magnify
        </v-icon>
      </v-btn>
    </template>
    <v-card>
      <v-card-title class="headline grey lighten-2 pr-3">
        Sliding Administration Fees
        <v-spacer></v-spacer>
        <v-btn
          color="secondary"
          text
          @click="tierDialog = false"
        >X</v-btn>
      </v-card-title>
      <v-container class="pa-3">
        <v-form
          @submit.prevent="onSubmit"
          ref="form">
          <v-row
            dense>
            <v-col>
              <v-card>
                <v-card-text>
                  <strong>
                    Lower Threshold
                  </strong>
                </v-card-text>
              </v-card>
            </v-col>
            <v-col>
              <v-card>
                <v-card-text>
                  <strong>
                     Upper Threshold
                  </strong>
                </v-card-text>
              </v-card>
            </v-col>
            <v-col>
              <v-card>
                <v-card-text>
                  <strong>
                    Percentage Fee
                  </strong>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
          <template
            v-if="tierThresholds.length && tierPercs.length">
            <v-row
              v-for="(threshold, i) in tierThresholds"
              :key="threshold.id"

              dense>
              <v-col :cols="4">
                <v-currency-field
                  dense solo
                  :decimal-length="0"
                  v-model = "threshold.lower_threshold"
                  prefix="$"
                  type="number"
                  :rules="$rule8Digits"
                  hide-details='auto'
                  />
              </v-col>
              <v-col  :cols="4">
                <v-currency-field
                  dense solo
                  :decimal-length="0"
                  v-model = "threshold.threshold"
                  prefix="$"
                  type="number"
                  :rules="$rule8Digits"
                  hide-details='auto'
                  />
              </v-col>
              <v-col  :cols="4">
                <v-text-field
                  dense solo
                  :value = "getPercentage(i)"
                  @change = "setPercentage($event, i)"
                  suffix="%"
                  type="number"
                  :rules="rulePercentageLTZero"
                  hide-details='auto'
                  />
              </v-col>
            </v-row>
          </template>
          <template v-if="tierThresholds.length > 0">
            <v-divider class="mt-4" />
            <v-card-subtitle class="pb-2">
              Add a new threshold
            </v-card-subtitle>
          </template>
          <v-row
            dense>
            <v-col :cols="4">
              <v-currency-field
                dense solo
                :decimal-length="0"
                v-model = "newThreshold.lower_threshold"
                prefix="$"
                type="number"
                :rules="$rule8Digits"
                hide-details='auto'
                />
            </v-col>
            <v-col  :cols="4">
              <v-currency-field
                dense solo
                :decimal-length="0"
                v-model = "newThreshold.threshold"
                prefix="$"
                type="number"
                :rules="validateThreshold"
                hide-details='auto'
                validate-on-blur
              />
            </v-col>
            <v-col
              :cols="4">
              <v-text-field
                dense solo
                v-model = "newPercentage.percentage"
                suffix="%"
                type="number"
                :rules="rulePercentageLTZero"
                hide-details='auto'
              >
                <template v-slot:append-outer>

                  <v-icon color="primary"
                    @click="addNewTier" >
                    mdi-plus
                  </v-icon>
                </template>
              </v-text-field>
            </v-col>
          </v-row>
          <v-divider class="mt-4 mb-2" />
          <v-row dense>
            <v-col class="text-right" dense>
              <v-btn  @click="onSubmit" color="primary" >
                Save All
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
import { mapGetters } from "vuex";
import { rule8Digits, ruleGTZero } from "@/components/mixins/Rules.js";

export default {
  name: "ModifyTierFees",
  mixins: [rule8Digits, ruleGTZero],
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
  },
  data() {
    return {
      error: null,
      tierDialog: false,
      tierThresholds: [],
      tierPercs: [],
      newThreshold: {
        lower_threshold: 0,
        threshold: 0,
        platform_fee_group: this.platformFee.id
      },
      newPercentage: {
        percentage: 0,
        platform_fee_group: this.platformFee.id
      },
    };
  },
  computed: {
    ...mapGetters(["activeScenario", "activeUser", "activePlatform", "platformNames"]),
    validateThreshold() {
      if (this.newThreshold.threshold > 0 || this.newPercentage.percentage > 0) {
        return this.$ruleGTZero.concat(this.$rule8Digits)
      } else {
        return this.$rule8Digits
      }
    },
    rulePercentageLTZero() {
      return [v => (v < 10) && (v >= -10) || 'Must be between -10% and 10%']
    }
    // lastThreshold() {
    //   return this.tierThresholds[this.tierThresholds.length - 1]
    // }
  },
  // watch: {
  //   tierThresholds() {
  //     this.newThreshold.lower_threshold = this.lastThreshold.threshold
  //   }
  // },
  methods: {
    getTierThresholds() {
      let endpoint = null
      if (this.template) {
        endpoint = `/api/platformtemplates/${this.platform}/fees/${this.platformFee.id}/tier-thresholds/`;
      } else {
        endpoint = `/api/scenarios/${this.activeScenario.id}/platforms/${this.activePlatform.id}/platformfees/${this.platformFee.id}/tier-thresholds/`;
      };
      apiService(endpoint).then(data => {
        this.tierThresholds = data.results;
      });
    },
    getTierPercs() {
      let endpoint = null
      if (this.template) {
        endpoint = `/api/platformtemplates/${this.platform}/fees/${this.platformFee.id}/tier-percs/`;
      } else {
        endpoint = `/api/scenarios/${this.activeScenario.id}/platforms/${this.activePlatform.id}/platformfees/${this.platformFee.id}/tier-percs/`;
      };
      apiService(endpoint).then(data => {
        this.tierPercs = data.results;
      });
    },
    // Too many things that can go wrong with these helper functions rn
    // setLowerThreshold(event, index) {
    //   this.tierThresholds[index].lower_threshold = event;
    //   if (index > 0) {
    //     this.tierThresholds[index-1].threshold = event;
    //   }
    // },
    // setThreshold(event, index) {
    //   this.tierThresholds[index].threshold = event;
    //   if (index < this.tierThresholds.length-1) {
    //     this.tierThresholds[index+1].lower_threshold = event;
    //   }
    // },
    addNewTier(){
      if (this.$refs.form.validate()) {
        if (this.newThreshold.threshold > 0) {
          // Push the new threshold obj to the threshold array
          this.tierThresholds.push({...this.newThreshold});
          // Reset the newThreshold
          this.newThreshold.lower_threshold = 0;
          this.newThreshold.threshold = 0;
          // same as the threshold object, but for perc.
          this.newPercentage.percentage = (this.newPercentage.percentage/100).toFixed(6);
          this.tierPercs.push({...this.newPercentage});
          this.newPercentage.percentage = null;
          this.onSubmit()
        } else {
          this.error = "Upper threshold must be greater than 0"
        }
      }
    },
    setPercentage(event, index) {
      this.tierPercs[index].percentage = (event/100).toFixed(6);
    },
    getPercentage(index) {
      return (this.tierPercs[index].percentage*100).toFixed(4)
    },
    selectMethod(item) {
      if (item.id) {
        return "PATCH"
      } else {
        return "POST"
      };
    },
    thresholdOrPerc(item) {
      if (item.threshold) {
        return "tier-thresholds"
      } else {
        return "tier-percs"
      }
    },
    endpointSelector(item){
      let subRoute = this.thresholdOrPerc(item);
      if (this.template) {
        if (item.id) {
          return `/api/platformtemplates/${this.platform}/fees/${this.platformFee.id}/${subRoute}/${item.id}/`;
        } else {
          return `/api/platformtemplates/${this.platform}/fees/${this.platformFee.id}/${subRoute}/`;
        }
      } else {
        if (item.id) {
          return `/api/scenarios/${this.activeScenario.id}/platforms/${this.activePlatform.id}/platformfees/${this.platformFee.id}/${subRoute}/${item.id}/`;
        } else {
          return `/api/scenarios/${this.activeScenario.id}/platforms/${this.activePlatform.id}/platformfees/${this.platformFee.id}/${subRoute}/`;
        }
      };
    },
    onSubmit() {
      if (this.newPercentage.percentage) {
        this.addNewTier();
      } else {
        if (this.$refs.form.validate()) {
          for (let i=0; i < this.tierThresholds.length; i++) {
            let endpoint = this.endpointSelector(this.tierThresholds[i]);
            apiService(endpoint, this.selectMethod(this.tierThresholds[i]),
              this.tierThresholds[i]
            ).then(data => {
              this.tierThresholds[i].id = data.id
            })
          };
          for (let i=0; i < this.tierPercs.length; i++) {
            let endpoint = this.endpointSelector(this.tierPercs[i]);
            apiService(endpoint, this.selectMethod(this.tierPercs[i]),
              this.tierPercs[i]
            ).then(data => {
              this.tierPercs[i].id = data.id;
            })
          };
        }
      }
    }
  },
  mounted() {
    this.getTierPercs();
    this.getTierThresholds();
  }
}
</script>
