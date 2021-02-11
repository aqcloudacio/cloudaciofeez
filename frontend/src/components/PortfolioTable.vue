<template lang="html">
  <v-container class="pa-0 small-text">
    <v-row
      align="center"
      :class="(canEdit && !_.isEmpty(selectedPortfolio)) ? 'mb-3' : '' ">
      <v-col
      :cols="6">
        <v-select
          class="rounded-card"
          v-if="!editPortfolioName"
          :items="portfolios"
          item-text="name"
          return-object
          v-model="selectedPortfolio"
          placeholder="Select a Model Portfolio"
          outlined dense hide-details="auto">
          <template v-slot:append-outer v-if="canEdit && portfolioIsSelected">
            <v-icon
              v-if="!editPortfolioName"
              color="primary" icon
              @click="editPortfolioName = !editPortfolioName">mdi-pencil-circle</v-icon>
          </template>
          <template v-slot:append-outer v-else-if="!canEdit && portfolioIsSelected">
            <v-tooltip bottom>
               <template v-slot:activator="{ on }">
                  <v-icon
                    v-on='on'
                    color="primary" icon
                    >mdi-lock</v-icon>
              </template>
              <span>{{lockMessage}}</span>
            </v-tooltip>
          </template>
        </v-select>
        <v-text-field
          v-else
          :value="selectedPortfolio.name"
          @change="newPortfolioName = $event"
          dense outlined
          hide-details='auto'>
          <template v-slot:append-outer v-if="canEdit">
            <v-icon
              v-if="editPortfolioName"
              color="primary" icon
              @click="updatePortfolioName()">mdi-check-circle</v-icon>
          </template>
        </v-text-field>
      </v-col>
      <v-col>
        <v-container class="pa-0 d-flex">
          <v-spacer />
          <v-card-actions class="pr-0">
            <AddPortfolioName
              @add-portfolio="addPortfolio"/>
            <v-btn icon>
              <DeleteObj
                v-if="canEdit"
                :objectType="'model portfolio'"
                :objectToDelete="selectedPortfolio"
                @delete-object="deletePortfolio($event)"
                :color="'primary'"
              />
            </v-btn>
          </v-card-actions>
        </v-container>
      </v-col>
    </v-row>
    <v-divider v-if="canEdit && !_.isEmpty(selectedPortfolio)" class="mt-1 mb-4"/>
    <v-form ref="addForm">
      <v-row
        dense
        v-if="canEdit && !_.isEmpty(selectedPortfolio)">
        <v-col
          :cols="9">
          <v-autocomplete
            class="rounded-card"
            v-model="newInvestment.investment_name"
            :items="investmentNames"
            item-text="name"
            item-value="id"
            outlined dense
            :rules="[v => !!(v) || 'Select a name from the dropdown']"
            validate-on-blur
            hide-details="auto"
            :filter="filterObject"
            label="Investment Name"
            placeholder="Add an investment by typing a name">
            <template v-slot:item='{ item }'>
              <v-list-item-content class="pr-2">
                <v-list-item-title v-text="item.name"></v-list-item-title>
              </v-list-item-content>
              <v-spacer></v-spacer>
              <v-chip v-if="item.code" right outlined>
                {{ item.code }}
              </v-chip>
            </template>
          </v-autocomplete>
        </v-col>
        <v-col
          :cols="3">
            <v-text-field
              class="rounded-card"
              placeholder="Percentage"
              type="number"
              :value = "getPercentage(newInvestment)"
              @blur = "setPercentage($event.target.value, newInvestment)"
              outlined dense
              hide-details="auto"
              :rules="$rulePercTo100"
              suffix="%">
              <template v-slot:append-outer v-if="canEdit">
                <v-slide-x-reverse-transition
                   mode="out-in"
                   >
                  <v-icon color="primary"
                    @click="addInvestment()"
                    :key="`icon-${isSaving}`">
                    mdi-plus
                  </v-icon>
                </v-slide-x-reverse-transition>
              </template>
            </v-text-field>
        </v-col>
      </v-row>
    </v-form>
    <v-form ref="mainForm">
      <v-row
        v-for="investment in investments"
        :key="investment.id"
        dense>
        <v-col
          :cols="9">
            <v-autocomplete
              class="rounded-card"
              v-model="investment.investment_name"
              :items="investmentNames"
              item-value="id"
              item-text="name"
              @change="addToChanged(investment)"
              :filter="filterObject"
              outlined dense
              :rules="[v => !!(v) || 'Select a name from the dropdown']"
              validate-on-blur
              hide-details="auto">
              <template v-slot:item='{ item }'>
                <v-list-item-content class="pr-2">
                  <v-list-item-title v-text="item.name"></v-list-item-title>
                </v-list-item-content>
                <v-spacer></v-spacer>
                <v-chip v-if="item.code" right outlined>
                  {{ item.code }}
                </v-chip>
              </template>
            </v-autocomplete>
        </v-col>
        <v-col
          :cols="3">
          <v-text-field
            class="rounded-card"

            placeholder="Percentage"
            type="number"
            :value = "getPercentage(investment)"
            @blur = "setPercentage($event.target.value, investment)"
            @change = "addToChanged(investment)"
            dense outlined
            hide-details="auto"
            :rules="$rulePercTo100"
            suffix="%">
            <template v-slot:append-outer v-if="canEdit">
              <DeleteObj
                v-if="canEdit"
                :objectType="'modelInvestment'"
                :objectToDelete="investment"
                :portfolioID="portfolioID"
                @delete-object="deleteInvestment($event)"
                v-on="$listeners"
                :color="'primary'"
              />
            </template>
          </v-text-field>
        </v-col>
      </v-row>
    </v-form>
    <v-divider class="mt-4" v-if="canEdit && !_.isEmpty(selectedPortfolio)" />
    <v-row v-if="investments.length && canEdit">
      <v-col>
        <v-tooltip bottom v-if="checkHint()">
          <template v-slot:activator="{ on }">
            <v-icon v-on="on" color="red" large>
              mdi-alert-rhombus-outline
            </v-icon>
          </template>
          {{ checkHint()}}
        </v-tooltip>
        <span style="color: red">
          {{ checkHint() }}
        </span>
      </v-col>
      <v-spacer />
      <v-col class="text-right">

        <v-btn @click="onSubmit" class="primary-action-button">Update All</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { apiService } from "@/common/api.service.js";
import AddPortfolioName from "@/components/AddPortfolioName.vue";
import DeleteObj from "@/components/DeleteObj.vue";
import { rulePercTo100 } from "@/components/mixins/Rules.js";
import { mapGetters } from "vuex";
import {
  INVESTMENTNAME_ALL,
} from "@/store/actions.type";

export default {
  name: "PortfolioTable",
  mixins: [rulePercTo100],
  props: {
    portfolio: {
      type: Object,
      required: false,
    },
  },
  data() {
    return {
      isSaving: false,
      search: null,
      selectedPortfolio: {},
      investments: [],
      active: false,
      error: null,
      portfolios: [],
      changeList: [],
      newInvestment: {},
      editPortfolioName: false,
      newPortfolioName: '',
    };
  },
  components: {
    DeleteObj,
    AddPortfolioName,
  },
  watch: {
    portfolio: function () {
      this.getInvestments();
    },
    selectedPortfolio: function () {
      this.getInvestments();
    },
  },
  computed: {
    ...mapGetters(["activeUser", "investmentNames"]),
    portfolioIsSelected() {
      return !this._.isEmpty(this.selectedPortfolio);
    },
    lockMessage() {
      let msg = '';
      if (!this.isNotAFSLLimited) {
        msg += 'You cannot edit AFSL Model Portfolios'
      }
      else if (!this.isPracticeAdmin) {
        msg += 'You are not an admin of this Practice'
      }
      else if (!this.isNotMasterTemplate) {
        msg += 'You cannot edit this Model Portfolio'
      }
      return msg
    },
    portfolioID: function() {
      if (this.selectedPortfolio != null) {
        return this.selectedPortfolio.id;
      } else if (this.portfolio){
        return this.portfolio.id;
      } else {
        return null
      }
    },
    canEdit() {
      if (this.isPracticeAdmin && this.isNotAFSLLimited && this.isNotMasterTemplate ) {
        return true
      } else {
        return false
      }
    },
    isNotMasterTemplate() {
      if (this.selectedPortfolio.id) {
        if (this.selectedPortfolio.template && this.selectedPortfolio.master_template) {
          return false
        } else {
          return true
        }
      } else {
        return true
      }
    },
    isPracticeAdmin() {
      if (this.selectedPortfolio.id) {
        if (this.selectedPortfolio.active_practices.length > 0) {
          return this.selectedPortfolio.active_practices.some(item => this.activeUser.admin_practices.includes(item));
        } else {
          return true
        }
      } else {
        return true
      }
    },
    isNotAFSLLimited() {
      if (this.selectedPortfolio.id) {
        if (this._.isEmpty(this.selectedPortfolio.afsls)) {
          return true
        } else {
          return false
        }
      } else {
        return true
      }
    },
  },
  methods: {
    filterObject(item, queryText) {
        const textOne = item.name.toLowerCase()
        const searchText = queryText.toLowerCase()

        if (item.code) {
          const textTwo = item.code.toLowerCase()
          return textOne.indexOf(searchText) > -1 ||
            textTwo.indexOf(searchText) > -1
        } else {
          return textOne.indexOf(searchText) > -1
        }
    },
    checkHint() {
      if (!this.checkComplete()) {
        return "Allocations do not equal 100%"
      }
    },
    checkComplete() {
      let value = this.investments.reduce( function (a,b) {
        return parseFloat(a) + parseFloat(b.percentage);
      }, 0);
      if (value.toFixed(4) === '1.0000') {
        return true
      } else {
        return false
      }
    },
    updatePortfolioName() {
      this.editPortfolioName = !this.editPortfolioName;
      if (this.newPortfolioName != '') {
        let endpoint = `/api/portfoliotemplates/${this.selectedPortfolio.id}/`;
        apiService(endpoint, "PATCH", {
          name: this.newPortfolioName,
        }).then(data => {
          this.selectedPortfolio = data;
          this.newPortfolioName = "";
          const i = this.portfolios.findIndex(item => item.id === data.id);
          this.portfolios.splice(i,0,data);
        });
      }
    },
    addPortfolio(data){
      this.selectedPortfolio = data;
      this.getPortfolios();
    },
    deleteInvestment(data) {
      // Removes item from the investment list
      const deletedIndex = this.investments.findIndex(item => item.id === data.id);
      this.$delete(this.investments, deletedIndex)

      // Removes item from the changed list (if it's in it)
      const deletedChangedIndex = this.changeList.findIndex(item => item.id === data.id);
      if (deletedChangedIndex >= 0) {
        this.$delete(this.changeList, deletedChangedIndex)
      }
    },
    deletePortfolio(data) {
      const i = this.portfolios.findIndex(item => item.id === data.id);
      this.$delete(this.portfolios,i)
      this.investments = [];
    },
    setPercentage(event, investment) {
      if (investment.id) {
        //for existing investments
        const i = this.investments.findIndex(item => item.id === investment.id);
        this.investments[i].percentage = (event/100).toFixed(4);
      } else if (investment.percentage) {
        //for new investments that have a percentage property
        this.newInvestment.percentage = (event/100).toFixed(4)
      } else {
        //for new investments
        this.$set(this.newInvestment, 'percentage', (event/100).toFixed(4))
      }
    },
    getPercentage(investment) {
      if (investment.percentage) {
        return (investment.percentage*100).toFixed(2);
      } else {
        return null
      }
    },
    addToChanged(investment) {
      if (!(this.changeList.includes(investment))) {
        this.changeList.push(investment);
      } else {
        const i = this.changeList.findIndex(item => item.id === investment.id);
        this.changeList.splice(i, 1);
        this.changeList.push(investment);
      }
    },
    getPortfolios() {
      let endpoint = `/api/portfoliotemplates/`;
      apiService(endpoint).then(data => {
        this.portfolios = data.results;
      });
    },
    getInvestments() {
      if (this.portfolioID != null) {
        let endpoint = `/api/portfoliotemplates/${this.portfolioID}/investments/`;
        apiService(endpoint).then(data => {
          this.investments = data.results;
        });
      };
    },
    addInvestment() {
      if (this.$refs.addForm.validate()) {
        this.isSaving = true;
        // Set blank percentages to zero.
        if (!this.newInvestment.percentage) {
          this.newInvestment.percentage = 0;
        }
        let endpoint = `/api/portfoliotemplates/${this.portfolioID}/investments/`;
        apiService(endpoint, "POST", {
          investment_name_id: this.newInvestment.investment_name,
          portfolio: this.portfolioID,
          percentage: this.newInvestment.percentage,
        }).then(data => {
          this.investments.unshift(data);
          this.newInvestment.investment_name = null;
          this.newInvestment.percentage = null;
          this.isSaving = false;
        });
      }
    },
    onSubmit() {
      // If there is a new item in the add row, add it too.
      if (this.newInvestment.investment_name) {
        this.addInvestment();
      }
      if (this.changeList && this.$refs.mainForm.validate()) {
        for (let i=0; i < this.changeList.length; i++) {
          let endpoint = `/api/portfoliotemplates/${this.portfolioID}/investments/${this.changeList[i].id}/`;
          apiService(endpoint, "PATCH", {
            investment_name_id: this.changeList[i].investment_name.id,
            portfolio: this.portfolioID,
            percentage: this.changeList[i].percentage,
          })
        };
      };
    },
    getInvestmentNames() {
      if (this._.isEmpty(this.investmentNames)) {
        this.$store.dispatch(INVESTMENTNAME_ALL)
      }
    },
  },
  mounted() {
    this.getInvestmentNames();
    this.getPortfolios();
    this.getInvestments();
  }
};
</script>
