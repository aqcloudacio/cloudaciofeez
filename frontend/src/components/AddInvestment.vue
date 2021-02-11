<template lang="html">
  <v-expansion-panel @click.stop class="py-0">
    <v-expansion-panel-header class="px-3 py-2"  @click.stop expand-icon="mdi-plus" disabled>
      <v-form ref="form">
        <v-row class="ma-0" @click.stop >
          <v-col :cols="8" class="py-0 pl-0" @click.stop>
            <v-combobox
              solo dense
              class="rounded-card small-text"
              v-model="newInvestment"
              :items="investmentList"
              @keyup.enter="$refs.combobox.blur()"
              ref="combobox"
              no-data-text="Create a custom investment"
              allow-overflow
              @keyup.space.prevent
              @click.stop
              hide-details="auto"
              placeholder="Add an investment by typing its name"
              :search-input.sync="search"
              item-text="name"
              :filter="filterObject"
              :rules="[v => !!(v) || 'You must select an investment']"
              validate-on-blur>
              <!-- <template v-slot:append-outer>
                <v-menu
                  top offset-y
                  :close-on-content-click="false">
                  <template v-slot:activator="{ on }">
                    <v-icon
                      color="teal"
                      @click.stop
                      v-on="on">
                        mdi-sort
                    </v-icon>
                  </template>
                  <v-list dense>
                    <template v-for="(item, idx) in filterItems">
                      <v-list-item
                        :key="item.id"
                        :disabled="item.disabled">
                        <v-checkbox
                          dense
                          class='mt-0'
                          hide-details
                          @change="setSelected($event, item.id)"
                          v-model="item.selected"
                        />
                        <v-list-item-title class="mt-1">
                          {{ item.name }}
                        </v-list-item-title>
                      </v-list-item>
                      <v-divider v-if="item.id===1" :key="idx" class="mx-4"></v-divider>
                    </template>
                  </v-list>
                </v-menu>
              </template> -->
              <template v-slot:prepend-item v-if="showSponsoredItem">
                <v-list-item @click="selectSponsored">
                  <v-tooltip left>
                    <template v-slot:activator="{ on }">
                      <v-list-item-icon class="my-3 mr-2"  v-on="on">
                        <v-icon color="yellow">mdi-star</v-icon>
                      </v-list-item-icon>
                    </template>
                    <span>Sponsored Product</span>
                  </v-tooltip>
                  <v-list-item-content>
                    <v-list-item-title>{{sponsoredItem.investment_name}}</v-list-item-title>
                  </v-list-item-content>
                  <v-list-item-action class="ml-2 my-2">
                    <v-btn icon @click.stop :href="sponsoredItem.link" target="_blank">
                      <v-icon color="grey lighten-1">mdi-information</v-icon>
                    </v-btn>
                  </v-list-item-action>
                </v-list-item>
              </template>
              <template v-slot:no-data>
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-title>
                      No investments match "<strong>{{ search }}</strong>". Press <kbd>enter</kbd> to create a custom investment.
                    </v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </template>
              <template v-slot:item='{ item }'>
                <v-list-item-content class="pr-2">
                  <v-list-item-title v-text="item.name"></v-list-item-title>
                </v-list-item-content>
                <v-spacer></v-spacer>
                <v-chip v-if="item.code" right outlined>
                  {{ item.code }}
                </v-chip>
              </template>
            </v-combobox>
          </v-col>
          <v-col :cols="4" class="py-0 pl-0">
            <v-currency-field
              style="color:grey"
              prefix="$"
              :decimal-length="0"
              placeholder="Amount"
              dense solo
              class="rounded-card small-text"
              hide-details="auto"
              type="number"
              @keydown.space.prevent
              @click.stop
              v-model="investmentAmount"
              :rules="$rule8Digits">
              <template v-slot:append>
                <v-slide-x-reverse-transition
                   mode="out-in"
                   >
                  <v-icon
                    :key="`icon-${isSaving}`"
                    ref="submit"
                    @click="delaySubmit"
                    color="primary"
                    v-text="'mdi-plus-circle'"
                    :disabled="isDisabled"
                    >
                  </v-icon>
                </v-slide-x-reverse-transition>
              </template>
              <template v-slot:append-outer>

                <v-menu
                  top offset-y
                  :close-on-content-click="false">
                  <template v-slot:activator="{ on }">
                    <v-icon
                      color="grey"
                      @click.stop
                      v-on="on">
                        mdi-sort
                    </v-icon>
                  </template>
                  <v-list dense>
                    <template v-for="(item, idx) in filterItems">
                      <v-list-item
                        :key="item.id"
                        :disabled="item.disabled">
                        <v-checkbox
                          dense
                          class='mt-0'
                          hide-details
                          @change="setSelected($event, item.id)"
                          v-model="item.selected"
                        />
                        <v-list-item-title class="mt-1">
                          {{ item.name }}
                        </v-list-item-title>
                      </v-list-item>
                      <v-divider v-if="item.id===1" :key="idx" class="mx-4"></v-divider>
                    </template>
                  </v-list>
                </v-menu>
              </template>
            </v-currency-field>
          </v-col>
        </v-row>
      </v-form>
    </v-expansion-panel-header>
  </v-expansion-panel>
</template>

<script>
import { apiService } from "@/common/api.service.js";
import { mapGetters } from "vuex";
import {
  INVESTMENTNAME_ALL,
  PLATFORM_AA_FETCH,
} from "@/store/actions.type";
import {rule8Digits} from "@/components/mixins/Rules.js";

export default {
  name: "AddInvestment",
  mixins: [rule8Digits,],
  data() {
    return {
      search: null,
      newInvestment: null,
      investmentAmount: null,
      linkedInvestmentNames: [],
      error: null,
      next: null,
      selected: [],
      isSaving: false,
      filterItems: [
        {name: "Show all", selected: true, disabled: false, id: 1},
        {name: "Show fund-specific investments", selected: false, disabled: true, id: 2},
        {name: "Show managed funds", selected: true, disabled: false, id: 3},
        {name: "Show managed accounts", selected: true, disabled: false, id: 4},
        {name: "Show listed investments", selected: true, disabled: false, id: 5},
        {name: "Show other assets", selected: true, disabled: false, id: 6},
      ]
    }
  },
  computed: {
    ...mapGetters(["activePlatform", "activeScenario", "investmentNames", "adverts"]),
    isDisabled() {
      return this.newInvestment === null && this.search === null
    },
    recOrAlt() {
      return this.activePlatform.status === "Recommended" || this.activePlatform.status === "Alternative"
    },
    showSponsoredItem() {
      return (!this._.isEmpty(this.sponsoredItem) && this.recOrAlt && !this.fundSpecificShown)
    },
    sponsoredItem() {
      let item = [];
      if (this.adverts) {
        item =  this.adverts.filter(x => x.type_name === "starred_investment");
      }
      return item[0]
    },
    nameIdOrNull() {
      if (this.newInvestment.id != null) {
        return this.newInvestment.id;
      } else {
        return null;
      }
    },
    customName() {
      if (this.newInvestment.id != null) {
        return null
      } else {
        return this.newInvestment;
      }
    },
    fundSpecificShown() {
      return this.filterItems.find(x => x.id === 2).selected === true
    },
    filteredList() {
      // filters the whole unlinked investment list based on user input.
      let list = [];
      if (this.filterItems.find(x => x.id === 1).selected === true) {
        list.push(...this.investmentNames);
      }
      if (this.filterItems.find(x => x.id === 3).selected === true) {
        let f = this._.filter(this.investmentNames, {investment_class: 'MF'});
        list.push(...f);
      }
      if (this.filterItems.find(x => x.id === 4).selected === true) {
        let f = this._.filter(this.investmentNames, {investment_class: 'MA'});
        list.push(...f);
      }
      if (this.filterItems.find(x => x.id === 5).selected === true) {
        let f = this._.filter(this.investmentNames, {investment_class: 'LISTED'});
        list.push(...f);
      }
      if (this.filterItems.find(x => x.id === 6).selected === true) {
        let f = this._.filter(this.investmentNames, {investment_class: 'OTHER'});
        list.push(...f);
      }
      return list
    },
    investmentList() {
      // joins the linked investment names (if applicable) and the filtered full
      // investment name list
      let fullList = [];
      if (this.filterItems.find(x => x.id === 2).selected === true) {
        fullList.push(...this.linkedInvestmentNames);
      }
      if (this.filterItems.some(x => (x.id != 2) && (x.selected===true))) {
        fullList.push(...this.filteredList);
      }
      return fullList
    }
  },
  watch: {
    activePlatform() {
      this.setCheckBoxes();
      this.getLinkedInvestmentNames();
    }
  },
  methods: {
    selectSponsored(){
      this.search = this.sponsoredItem.investment_name;
      this.newInvestment = new Object();
      this.newInvestment['name'] = this.sponsoredItem.investment_name;
      this.newInvestment['id'] = this.sponsoredItem.investment_template;
      this.$refs.combobox.isMenuActive = false;
    },
    getInvestmentAmount(amount){
      if (amount) {
        return amount
      } else {
        return 0
      }
    },
    filterObject(item, queryText) {
      // Allows searching by code as well as name
      if (item) {
        const textOne = item.name.toLowerCase()
        const searchText = queryText.toLowerCase()

        if (item.code) {
          const textTwo = item.code.toLowerCase()
          return textOne.indexOf(searchText) > -1 ||
            textTwo.indexOf(searchText) > -1
        } else {
          return textOne.indexOf(searchText) > -1
        }
      }
    },
    nameAndCode(item) {
      return item.name + item.code
    },
    setSelected(event, id) {
      // If "Show all" is selected, show/hide all items except "fund-specfic"
      if (id === 1){
        for (let item of this.filterItems) {
          // Don't automatically select/deselect "fund-specific"
          if (item.id != 2) {
            item.selected = event;
            // Check if it has linked_investments first
          } else if (this.activePlatform.name && this.activePlatform.name.linked_investments) {
            item.selected = event;
          }
        }
      } // Else if a field is being deselected, change the prop.
      else if (event === false) {
        let idx = this.filterItems.findIndex(x => x.id === 1);
        this.filterItems[idx].selected = false;
      }
    },
    setCheckBoxes() {
      // Checks if the activePlatform has linked investments. If it does,
      // selects the "show fund specific" item and deselects the rest.
      let linkedInvIdx = this.filterItems.findIndex(x => x.id === 2);
      if (this.activePlatform.name && this.activePlatform.name.linked_investments) {
        this.filterItems[linkedInvIdx].selected = true;
        this.filterItems[linkedInvIdx].disabled = false;
        for (let item of this.filterItems) {
          if (item.id != 2) {
            item.selected = false;
          }
        }
      } else {
        this.setSelected(true,1);
      }
    },
    getInvestmentNames() {
      if (this._.isEmpty(this.investmentNames)) {
        this.$store.dispatch(INVESTMENTNAME_ALL)
      }
    },
    getLinkedInvestmentNames() {
      if (this.activePlatform.name && this.activePlatform.name.linked_investments) {
        let endpoint = ''
        if (this.next === null) {
          endpoint = `/api/platformnames/${this.activePlatform.name.id}/investmentnames/`
        } else {
          endpoint = this.next;
        }
        apiService(endpoint, "GET").then(data => {
          this.linkedInvestmentNames.push(...data.results);
          if (data.next) {
            this.next = data.next;
            this.getLinkedInvestmentNames()
          } else {
            this.next = null;
          }
        });
      }
    },
    delaySubmit() {
      // Resolves a weird combobox bug where it does not update props until blur
      this.$refs.combobox.blur();
      this.$nextTick(() => {
        this.onSubmit();
      })
    },
    onSubmit() {
      if (this.$refs.form.validate()) {
        this.isSaving = true;
        let endpoint = `/api/scenarios/${this.activeScenario.id}/platforms/${this.activePlatform.id}/investments/`;
        apiService(endpoint, "POST", {
          name_id: this.nameIdOrNull,
          investment_class_id: null,
          platform: this.activePlatform.id,
          amount: this.getInvestmentAmount(this.investmentAmount),
          custom_name: this.customName,
        }).then(data => {
          this.$emit("add-investment", data);
          this.newInvestment = null;
          this.investmentAmount = null;
          this.getActivePlatformAA();
          this.isSaving = false;
        });
      }
    },
    getActivePlatformAA() {
      // Refreshes the platform aa chart when an investment is saved
      this.$store.dispatch(PLATFORM_AA_FETCH, {
        'scenarioId': this.activeScenario.id,
        'platformId': this.activePlatform.id,
      })
    },
  },
  mounted() {
    this.getInvestmentNames();
    this.setCheckBoxes();
    this.getLinkedInvestmentNames();
  }
};
</script>
