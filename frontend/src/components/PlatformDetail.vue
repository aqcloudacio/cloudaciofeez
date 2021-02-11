<template lang="html">
  <v-dialog v-model="dialog">
    <template v-slot:activator="{ on }">

      <v-container  v-on="on" class="pa-2">
        <v-row dense>
          <v-col dense>
            <span class="display-1 font-weight-medium"><strong>{{ customName }}</strong></span><br>
            <span v-if="activePlatform.account_number" class="subtitle-1">
                {{ activePlatform.account_number }}
            </span>
            <v-card-actions class="pl-0 pb-0">
              <v-tooltip right @click.stop>
                <template v-slot:activator="{ on }">
                  <v-btn
                    v-if="activePlatform.name"
                    @click.stop
                    v-on="on"
                    icon
                    :href="activePlatform.name.PDS_link"
                    color="green"
                    target="_blank">
                    <v-icon>
                      mdi-file-document-box-search-outline
                    </v-icon>
                  </v-btn>
                </template>
                <span>
                  View PDS
                </span>
              </v-tooltip>
              <v-tooltip right @click.stop>
                <template v-slot:activator="{ on }">
                  <v-btn icon v-on="on" >
                    <v-icon :color="isLinked" medium @click.stop>mdi-share-variant</v-icon>
                  </v-btn>
                </template>
                <template v-for="(item,index) in platformLinks">
                  <span :key="`${item[0]} - ${index}`">
                    {{item[0]}}<template v-if="item[1]">: {{item[1] | toCurrency}}</template>
                    <template v-else>: $0</template>
                    <br>
                  </span>
                </template>
              </v-tooltip>
            </v-card-actions>
          </v-col>
          <v-divider vertical inset class="mb-4 mx-4"/>


          <v-col :cols="7" dense>
            <v-container class="px-2 py-0">
              <v-row dense>
                <v-col dense :cols="4">
                  <span style="font-size:18px" class="black--text font-weight-medium">Balance: </span> <br>
                  <span style="font-size:22px" class="accent--text font-weight-medium">{{ activePlatform.platform_total | toCurrency }}</span>
                </v-col>
                <v-col dense>
                  <span style="font-size:18px" class="black--text font-weight-medium">Fees: </span><br>
                  <span style="font-size:22px" class="grey--text font-weight-medium">{{activePlatform.platform_total_fees | toCurrency }}</span>
                </v-col>
              </v-row>
                <!-- Unallocated Funds: $XXXXX  don't want to implement this yet-->
              <v-row>
                <v-col :cols="4">
                  <v-btn
                    width="100%"
                    rounded
                    small
                    color="primary"
                    dark>
                    <span class="font-weight-light">Detail</span>
                  </v-btn>
                </v-col>
                <v-col :cols="4">
                  <v-menu offset-y
                    @click.stop
                    transition="slide-y-transition"
                    :close-on-content-click="true">
                    <template v-slot:activator="{ on }">
                      <v-btn
                        width="100%"
                        rounded
                        small
                        color="primary"
                        dark
                        v-on="on"
                      >
                      <span class="font-weight-light">Fees</span>
                      </v-btn>
                    </template>
                    <v-list>
                      <template v-for="platformFee in platformFees">
                        <PlatformFeeSummary
                          v-on="$listeners"
                          :platformFee="platformFee"
                          :key="platformFee.id"
                        />
                      </template>
                    </v-list>
                  </v-menu>
                </v-col>
                <v-col :cols="4">
                  <AddPortfolio v-on="$listeners" />
                </v-col>
              </v-row>
            </v-container>
        </v-col>
      </v-row>
    </v-container>
  </template>


  <v-card>
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
                <v-row>
                  <v-col :cols="7">
                    <v-card-title v-if="editName === false && changePlatform === false">
                      {{customName}}
                    </v-card-title>
                    <v-text-field
                      class="px-4"
                      v-else-if="editName === true"
                      hide-details
                      :value="customName"
                      @change="setActivePlatformProp('custom_name', $event)"
                      label="Set a custom name"
                    />
                    <v-combobox
                      class="px-4"
                      v-else-if="changePlatform === true"
                      :value="customName"
                      @input="setNewName($event)"
                      :items="platformNames"
                      @keyup.enter="closeMenu"
                      label="Swap platforms"
                      item-text="name"
                      no-data-text="Create a custom platform"
                      ref="combobox"
                      :search-input.sync="search"
                      >
                      <template v-slot:no-data>
                        <v-list-item>
                          <v-list-item-content>
                            <v-list-item-title>
                              No platforms match "<strong>{{ search }}</strong>". Press <kbd>enter</kbd> to create a custom platform.
                            </v-list-item-title>
                          </v-list-item-content>
                        </v-list-item>
                      </template>
                    </v-combobox>
                  </v-col>
                  <v-spacer>
                  </v-spacer>
                  <v-col  :cols="5" class="mt-2" >
                    <v-btn
                      icon
                      large
                      @click="editName = !editName">
                      <v-icon
                        color="orange"
                        >
                        mdi-pencil-circle-outline
                      </v-icon>
                    </v-btn>
                    <v-dialog v-model="confirmDialog" max-width="290">
                      <template v-slot:activator="{ on }">
                        <v-btn
                          v-on="on"
                          icon
                          large>
                          <v-icon
                            color="green" >
                            mdi-swap-horizontal-circle-outline
                          </v-icon>
                        </v-btn>
                      </template>
                      <v-container>
                        <v-card>
                          <v-card-text>
                            Warning: swapping platforms will reset all platform fees<br>
                            Do you want to proceed?
                          </v-card-text>
                          <template>
                            <v-btn @click="swapPlatform">
                              Yes
                            </v-btn>
                            <v-btn @click="confirmDialog = !confirmDialog">
                              No
                            </v-btn>
                          </template>
                        </v-card>
                      </v-container>
                    </v-dialog>
                  </v-col>
                </v-row>
                <v-card-text v-if="activePlatform.PDS_date || activePlatform.PDS_version">
                  PDS <template v-if="activePlatform.PDS_date">
                    Date: {{activePlatform.PDS_date}}
                  </template>
                  <template v-if="activePlatform.PDS_version">
                    version {{activePlatform.PDS_version}}
                  </template>
                  <template v-if="activePlatform.name"> <br>
                    Last Checked: {{activePlatform.last_checked}}
                  </template>
                </v-card-text>
                <v-select
                  class="pa-4"
                  :items="getReadableList('platform_type')"
                  @change="convertToRealName('platform_type', $event)"
                  :value="convertLongName('platform_type')"
                  label="Account Type"
                  dense
                  hide-details
                ></v-select>
                <v-text-field
                  class="px-4 pb-4"
                  hide-details
                  :value="activePlatform.account_number"
                  @change="setActivePlatformProp('account_number', $event)"
                  dense
                  label="Account Number"
                />
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
                  <v-row class="ma-0">
                    <v-col class="pa-0">
                      <v-currency-field
                        type="number"
                        v-if="activePlatform.allowed_fee_link != 'None'"
                        hide-details
                        prefix="$"
                        :decimal-length="0"
                        @change="setActivePlatformProp('manual_linking_adjustment', $event, 'number')"
                        :value="activePlatform.manual_linking_adjustment"
                        label="Manual fee linking adjustment"
                      />
                    </v-col>
                  </v-row>
                  <v-row class="ma-0"  v-if="activePlatform.allowed_fee_link != 'None'">
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
                        v-if="activePlatform.fee_link_type == 'Reduction'"
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
                        v-model="activePlatform.shared_admin_fee">
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
                        v-model="activePlatform.single_fee_group">
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
                        v-on="on"
                        hide-details
                        v-model="activePlatform.white_label_admin_fee"
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
                    @change="setActivePlatformProp('switch_fee', $event, 'number')"
                    :value="activePlatform.switch_fee"
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
                    @change="setActivePlatformProp('admin_fee_cutoff', $event)"
                    :value="activePlatform.admin_fee_cutoff"
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
                    @change="setActivePlatformProp('ORR_levy_cap', $event)"
                    :value="activePlatform.ORR_levy_cap"
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
import AddPortfolio from "@/components/AddPortfolio.vue";
import PlatformFeeSummary from "@/components/PlatformFeeSummary.vue";
import { apiService } from "@/common/api.service.js";
import { rule4Digits, rule7Digits, rulePercentage } from "@/components/mixins/Rules.js";

import { mapGetters } from "vuex";
import {
  SET_ACTIVE_PLATFORM_PROP,
} from "@/store/mutations.type";
import {
  PLATFORM_UPDATE,
} from "@/store/actions.type";

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
    platformFees: {
      type: Array,
      required: true,
    },
  },
  components: {
    AddPortfolio,
    PlatformFeeSummary,
  },
  data() {
    return {
      changedName: null,
      valueOn: true,
      confirmDialog: false,
      search: null,
      dialog: false,
      changePlatform: false,
      editName: false,
      error: null,
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
    ...mapGetters(["activeScenario", "activeUser", "activePlatform", "platformNames"]),
    platformLinks() {
      if (this.activePlatform.linked_platforms == null) {
        return [["No linked platforms"]]
      } else {
        return this.activePlatform.linked_platforms
      }
    },
    isLinked() {
      if (this.activePlatform.linked_platforms == null) {
        return "grey"
      } else {
        return "blue"
      }
    },
    allowedWidth() {
      if (this.activePlatform.allowed_fee_link != "None") {
        return 9;
      } else {
        return 12;
      }
    },
    typeWidth() {
      if (this.activePlatform.fee_link_type == "Reduction") {
        return 9;
      } else {
        return 12;
      }
    },
    customName() {
      if (this.activePlatform.name === null) {
        return this.activePlatform.custom_name;
      } else if (this.activePlatform.custom_name != null) {
        return this.activePlatform.custom_name;
      } else if (this.activePlatform.name) {
        return this.activePlatform.name.name;
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
    setActivePlatformProp(prop, event, type) {
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
      this.$store.commit(SET_ACTIVE_PLATFORM_PROP, {
        'prop': prop,
        'value': event
      })
    },
    setPercentage(prop, event) {
      this.$store.commit(SET_ACTIVE_PLATFORM_PROP, {
        'prop': prop,
        'value': (event/100).toFixed(6)
      })
    },
    getPercentage(prop) {
      if (this.activePlatform[prop] > 0) {
        return (this.activePlatform[prop]*100).toFixed(2);
      } else {
        return null
      }
    },
    swapPlatform() {
      this.changePlatform = !this.changePlatform;
      this.confirmDialog = !this.confirmDialog;
    },
    setNewName(event){
      let name = null;
      let name_id = null;
      let custom_name = null;
      if (event.id != null) {
        // If the new name is NOT a custom name
        name = event;
        name_id = event.id;
        custom_name = null;
      } else {
        // If the new name is a custom name
        name = null;
        name_id = null;
        custom_name = event;
      }
      this.$store.commit(SET_ACTIVE_PLATFORM_PROP, {
        'prop': 'name',
        'value': name
      });
      this.$store.commit(SET_ACTIVE_PLATFORM_PROP, {
        'prop': 'name_id',
        'value': name_id
      });
      this.$store.commit(SET_ACTIVE_PLATFORM_PROP, {
        'prop': 'custom_name',
        'value': custom_name
      });
      this.$store.commit(SET_ACTIVE_PLATFORM_PROP, {
        'prop': 'refresh',
        'value': true
      });
    },
    getReadableList(item){
      let list = this.activePlatform[this.joinList(item)];
      let cleanList = [];
      if (list != null) {
        for (let i=0; i<list.length; i++) {
          cleanList.push(list[i][1]);
        }
      }
      return cleanList
    },
    convertLongName(item){
      let list = this.activePlatform[this.joinList(item)];
      let realName = "";
      if (list != null) {
        for (let i=0; i<list.length; i++) {
          if (this.activePlatform[item] == list[i][0]) {
            realName = list[i][1];
          }
        }
      }
      return realName;
    },
    convertToRealName(prop, event){
      let list = this.activePlatform[this.joinList(prop)];
      let realName = "";
      if (list != null) {
        for (let i=0; i<list.length; i++) {
          if (event == list[i][1]) {
            realName = list[i][0];
            this.$store.commit(SET_ACTIVE_PLATFORM_PROP, {
              'prop': prop,
              'value': realName
            })
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
        this.changePlatform = false;
        this.editName = false;
        this.dialog = false;
        if (this.template) {
          let endpoint = this.templateToggle();
          apiService(endpoint, "PATCH", this.platform).then(data => {
            this.$emit("modify-platform", data);
          });
        } else {
          this.$store.commit(SET_ACTIVE_PLATFORM_PROP, {
            'prop': 'edited',
            'value': true
          })
          this.$store.dispatch(PLATFORM_UPDATE);
        }
      }
    },
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
