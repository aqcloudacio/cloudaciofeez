<template lang="html">
  <v-dialog v-model="dialog">
    <template v-slot:activator="{ on }">
      <v-card  v-on="on" >
        <v-row class="mb-0">
          <v-col class="pb-0 pt-6"  >
            <v-tooltip right @click.stop>
              <template v-slot:activator="{ on }">
                <v-btn
                  v-if="platform.name"
                  @click.stop
                  v-on="on"
                  icon
                  :href="platform.name.direct_pds_link"
                  color="green"
                  target="_blank">
                  <v-icon>
                    mdi-file-search-outline
                  </v-icon>
                </v-btn>
              </template>
              <span>
                View PDS
              </span>
            </v-tooltip>
          </v-col>
        </v-row>
        <v-row class="mt-0 mx-2">
          <v-col :cols="4">
            <v-btn
              width="100%"
              small
              color="primary"
              dark>
              Detail
            </v-btn>
          </v-col>
        </v-row>
      </v-card>
    </template>
    <v-card v-if="!_.isEmpty(platform)">
      <v-card-title class="headline grey lighten-2 pr-3">
        Platform Details
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
          ref="form">
          <v-row>
            <v-col class="pt-0">
              <v-row>
                <v-col>
                  <v-card>
                    <v-text-field
                      hide-details="auto"
                      v-model="platform.PDS_version"
                      label="PDS version"
                    />
                    <v-text-field
                      hide-details="auto"
                      v-model="platform.PDS_date"
                      label="PDS date (YYYY-MM-DD)"
                    />
                    <v-text-field
                      hide-details="auto"
                      v-model="platform.last_checked"
                      label="Last checked"
                    />
                    <v-select
                      hide-details="auto"
                      v-model="platform.fee_link_group"
                      :items="feeLinkGroup"
                      label="Family fee group"
                      item-text="description"
                      item-value="id"
                    />

                    <v-select
                      class="pa-4"
                      :items="getReadableList('platform_type')"
                      @change="convertToRealName('platform_type', $event)"
                      :value="convertLongName('platform_type')"
                      label="Account Type"
                      dense
                      hide-details
                    ></v-select>

                  </v-card>
                  <v-card>
                    <v-card-title>
                      Fee Linking
                    </v-card-title>
                    <v-card-text>
                      <v-row class="ma-0">
                        <v-col class="pa-0">
                          <v-select
                            :items="getReadableList('allowed_fee_link')"
                            @change="convertToRealName('allowed_fee_link', $event)"
                            :value="convertLongName('allowed_fee_link')"
                            label="Allowable Fee Link"
                            hide-details
                          ></v-select>
                        </v-col>
                      </v-row>
                      <v-row class="ma-0"  v-if="platform.allowed_fee_link != 'None'">
                        <v-col class="pa-0" :cols="typeWidth">
                          <v-select
                            :items="getReadableList('fee_link_type')"
                            @change="convertToRealName('fee_link_type', $event)"
                            :value="convertLongName('fee_link_type')"
                            label="Fee Linking Type"
                            hide-details
                          ></v-select>
                        </v-col>
                        <v-col class="pa-0" :cols="3">
                          <v-text-field
                            v-if="platform.fee_link_type == 'Reduction'"
                            hide-details="auto"
                            type="number"
                            label="Reduction"
                            :value="getPercentage('admin_fee_linking_reduction')"
                            @change="setPercentage('admin_fee_linking_reduction', $event)"
                            suffix="%"
                          />
                        </v-col>
                      </v-row>
                    </v-card-text>
                  </v-card>
                </v-col>
              </v-row>
            </v-col>
            <v-col>
              <v-card>
                <v-card-title class="pb-0">
                  Fee Information
                </v-card-title>
                <v-card-text>
                  <v-row class="pa-0">
                    <v-col class="pt-0">
                      <v-tooltip bottom @click.stop>
                        <template v-slot:activator="{ on }">
                          <v-checkbox
                            v-on="on"
                            hide-details
                            v-model="platform.shared_admin_fee">
                            <span slot="label" v-on="on">{{getLabel("shared_admin_fee")}}</span>
                          </v-checkbox>
                        </template>
                        <span>
                          {{getToolTip("shared_admin_fee")}}
                        </span>
                      </v-tooltip>
                      <v-tooltip bottom @click.stop>
                        <template v-slot:activator="{ on }">
                          <v-checkbox
                            v-on="on"
                            hide-details
                            v-model="platform.single_fee_group">
                            <span slot="label" v-on="on">{{getLabel("single_fee_group")}}</span>
                          </v-checkbox>
                        </template>
                        <span>
                          {{getToolTip("single_fee_group")}}
                        </span>
                      </v-tooltip>
                    </v-col>
                    <v-col  class="pt-0">
                      <v-tooltip bottom @click.stop>
                        <template v-slot:activator="{ on }">
                          <v-checkbox
                            hide-details
                            v-model="platform.white_label_admin_fee"
                            >
                            <span slot="label" v-on="on">{{getLabel("white_label_admin_fee")}}</span>
                          </v-checkbox>
                        </template>
                        <span>
                          {{getToolTip("white_label_admin_fee")}}
                        </span>
                      </v-tooltip>
                    </v-col>
                  </v-row>
                  <v-row class="mt-0">
                    <v-col  class="pt-0">
                      <v-text-field
                        hide-details="auto"
                        :value="getPercentage('cash_fee')"
                        @change="setPercentage('cash_fee', $event)"
                        label="Cash account fee"
                        suffix="%"
                        type="number"
                        :rules="$rulePercentage"
                      />
                    </v-col>
                    <v-col  class="pt-0">
                      <v-currency-field
                        hide-details="auto"
                        prefix="$"
                        :decimal-length="2"
                        @change="setPlatformProp('switch_fee', $event, 'number')"
                        :value="platform.switch_fee"
                        label="Switching fee"
                        type="number"
                        :rules="$rule4Digits"
                      />
                    </v-col>
                  </v-row>
                  <v-row class="mt-0">
                    <v-col  class="pt-0">
                      <v-currency-field
                        hide-details="auto"
                        prefix="$"
                        :decimal-length="0"
                        @change="setPlatformProp('admin_fee_cutoff', $event)"
                        :value="platform.admin_fee_cutoff"
                        label="Admin fee cutoff"
                        type="number"
                        :rules="$rule7Digits"
                      />
                    </v-col>
                    <v-col  class="pt-0">
                      <v-currency-field
                        hide-details='auto'
                        prefix="$"
                        :decimal-length="2"
                        @change="setPlatformProp('ORR_levy_cap', $event)"
                        :value="platform.ORR_levy_cap"
                        label="ORR Levy cap"
                        type="number"
                        :rules="$rule4Digits"
                      />
                    </v-col>
                  </v-row>
                </v-card-text>
              </v-card>
              <v-container
                class="d-flex flex-row-reverse"
                height="300">
                <v-btn type="submit" color="primary">
                  Save
                </v-btn>
              </v-container>
            </v-col>
        </v-row>
      </v-form>
    </v-container>
  </v-card>
</v-dialog>
</template>

<script>
import { apiService } from "@/common/api.service.js";
import { rule4Digits, rule7Digits, rulePercentage } from "@/components/mixins/Rules.js";

import { mapGetters } from "vuex";

export default {
  name: "PlatformDetail",
  mixins: [rule4Digits, rule7Digits, rulePercentage],
  props: {
    platform: {
      type: Object,
      required: false,
    },
    template: {
      type: Boolean,
      required: false,
    },
  },
  data() {
    return {
      changedName: null,
      valueOn: true,
      confirmDialog: false,
      search: null,
      dialog: false,
      error: null,
      feeLinkGroup: [],
      displayItemsAdmin: [
          //format is ["field name", "friendly name", "editable by", "type", "tooltip"]
          ["status", "Platform status","all","list",null], //hidden for user (user can use Scenario view) /
          ["platform_type", "Platform type","all","list",null], //editable for user /
          ["PDS_date", "PDS date","admin","date",null], //read only for user /
          ["PDS_version", "PDS version","admin","string",null], //read only for user /
          ["PDS_link", "Link to PDS","admin","link",null], //read-only link /
          ["AA_link", "Link to Asset Allocation","admin","link",null], //read-only link /
          ["ICR_link", "Link to Investment Fees","admin","link",null], //read-only link /
          ["last_checked", "Last checked","admin","date",null], //read only for user /
          ["notes","Notes","admin","string",null] //hidden for user /
        ],
      displayItemsMisc: [
          //format is ["field name", "friendly name", "editable by", "tooltip"]
          ["shared_admin_fee", "Shared admin fee","all","boolean","If a platform has multiple fee structures, but only one fixed admin fee will be charged"],
          ["single_fee_group", "Single fee group","all","boolean",'If there is no "splitting" of platform fee groupings. That is, you can only have one fee group for the platform.'],
          ["allowed_fee_link", "Account linking allowed","all","list","The methods allowed to link accounts for the purposes of amin fee splitting."],
          ["maximum_linked_accounts", "Number of linked accounts","all","number","Maximum number of accounts that can be linked"],
          ["fee_link_type", "Fee linking effect","all","list","The way that fee linking modifies the administration fee."],
          ["admin_fee_linking_reduction", "Admin fee reduction through linking","all","number","The amount that the admin fee is reduced by linking accounts."],
          ["fee_link_group", "Linkable platforms","all","FK","Platforms that can be linked together."], //hidden for user /
          ["admin_fee_cutoff", "Admin fee cutoff","all","number","The fixed admin fee is not charged for balances above this level."],
          ["white_label_admin_fee", "White labled admin fee","all","boolean","The platform includes the administration fee in the investment fee of its investment options."],
          ["ORR_levy_cap", "Maximum ORR Levy","all","number","The cap on the ORR Levy for the entire platform."],
        ],
    };
  },
  computed: {
    ...mapGetters(["platformNames"]),
    platformLinks() {
      if (this.platform.linked_platforms == null) {
        return [["No linked platforms"]]
      } else {
        return this.platform.linked_platforms
      }
    },
    isLinked() {
      if (this.platform.linked_platforms == null) {
        return "grey"
      } else {
        return "blue"
      }
    },
    allowedWidth() {
      if (this.platform.allowed_fee_link != "None") {
        return 9;
      } else {
        return 12;
      }
    },
    typeWidth() {
      if (this.platform.fee_link_type == "Reduction") {
        return 9;
      } else {
        return 12;
      }
    },
    customName() {
      if (this.platform.name === null) {
        return this.platform.custom_name;
      } else if (this.platform.custom_name != null) {
        return this.platform.custom_name;
      } else if (this.platform.name) {
        return this.platform.name.name;
      } else {
        return null;
      }
    }
  },
  watch: {
    dialog() {
      if (this.$refs.form) {
        this.$refs.form.resetValidation()
      } else {
        //pass
      }
    }
  },
  methods: {
    getToolTip(prop) {
      // Vuetify bug means that tooltip does not display on labels unless
      // the label is split out via slot:label and v-on:on included.
      let item = this.displayItemsMisc.find(e => e[0] === prop)
      return item[4]
    },
    getLabel(prop) {
      // Vuetify bug means that tooltip does not display on labels unless
      // the label is split out via slot:label and v-on:on included.
      let item = this.displayItemsMisc.find(e => e[0] === prop)
      return item[1]
    },
    setPlatformProp(prop, event, type) {
      // Set null bools to false
      if (event===null) {
        event = false;
      }
      /// Set null numbers to zero
      if (type === "number" && !event) {
        event = 0;
      }
      // For some reason v-currency-field does not parse numbers with zero dp
      // properly so we check if they have a comma, then remove it and parsefloat.
      if (typeof event === "string"){
        if (event.indexOf(',') > -1) {
            event = parseFloat(event.replace(/,/g, ''))
        }
      }
      this.platform[prop] = event;
    },
    setPercentage(prop, event) {
      this.platform[prop] = (event/100).toFixed(6)
    },
    getPercentage(prop) {
      if (this.platform[prop] > 0) {
        return (this.platform[prop]*100).toFixed(2);
      } else {
        return null
      }
    },
    swapPlatform() {
      this.confirmDialog = !this.confirmDialog;
    },
    getReadableList(item){
      let list = this.platform[this.joinList(item)];
      let cleanList = [];
      if (list != null) {
        for (let i=0; i<list.length; i++) {
          cleanList.push(list[i][1]);
        }
      }
      return cleanList
    },
    convertLongName(item){
      let list = this.platform[this.joinList(item)];
      let realName = "";
      if (list != null) {
        for (let i=0; i<list.length; i++) {
          if (this.platform[item] == list[i][0]) {
            realName = list[i][1];
          }
        }
      }
      return realName;
    },
    convertToRealName(prop, event){
      let list = this.platform[this.joinList(prop)];
      let realName = "";
      if (list != null) {
        for (let i=0; i<list.length; i++) {
          if (event == list[i][1]) {
            realName = list[i][0];
            this.platform[prop] = realName
          }
        }
      }
    },
    joinList(item){
      return item.concat("_list");
    },
    templateToggle() {
      if (this.template){
        let endpoint = `/api/platformtemplates/${this.platform.id}/`;
        this.platform.template = true;
        return endpoint
      }
    },
    closeMenu() {
      // closes the comnbobox dropdown - vuetify bug
      this.$refs.combobox.isMenuActive = false;
    },
    onSubmit() {
      if (this.$refs.form.validate()) {
        this.dialog = false;
        if (this.template) {
          let endpoint = this.templateToggle();
          apiService(endpoint, "PATCH", this.platform).then(data => {
            this.$emit("modify-platform", data);
          });
        }
      }
    },
    getFeeGroups() {
      let endpoint = `/api/platformfamilygroups/`;
      apiService(endpoint).then(data => {
        this.feeLinkGroup = data.results;
      });
    }
  },
  mounted() {
    this.getFeeGroups()
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
