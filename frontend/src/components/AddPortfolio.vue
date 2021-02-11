<template lang="html">
  <v-dialog v-model="dialog" width="700px"  class="transparent">
    <template v-slot:activator="{ on }">
      <v-btn
        width="100%"
        v-on="on"
        small
        rounded
        color="primary"
        dark>
        <span class="font-weight-light">Add Portfolio</span>
      </v-btn>
    </template>
  <v-card class="small-text">
    <v-card-title class="dialog-header">
      Add Portfolio
      <v-spacer></v-spacer>
      <v-btn
        text
        @click="dialog = false" icon
      ><v-icon color="grey">mdi-close-circle-outline</v-icon></v-btn>
    </v-card-title>
    <v-container class="dialog-container">
        <v-form
          @submit.prevent="onSubmit"
          ref="form">
          <v-row dense>
            <v-col :cols="9">
              <v-autocomplete
                v-model="newPortfolio"
                :items="filteredPortfolios"
                item-text="name"
                item-value="id"
                ref="autocomplete"
                class="rounded-card" solo dense
                hide-details="auto"
                placeholder="Select a portfolio by typing its name"
                :rules="[v => !!v || 'You must select a Model Portfolio']"
                :validate-on-blur="true"
                >

                <template v-slot:prepend-item>
                  <v-list-item @click="selectSponsored">
                    <v-tooltip left>
                      <template v-slot:activator="{ on }">
                        <v-list-item-icon class="my-3 mr-2" v-on="on">
                          <v-icon color="yellow">mdi-star</v-icon>
                        </v-list-item-icon>
                      </template>
                      <span>Sponsored Product</span>
                    </v-tooltip>
                    <v-list-item-content>
                      <v-list-item-title>{{sponsoredItem.name}}</v-list-item-title>
                    </v-list-item-content>
                    <v-list-item-action class="ml-2 my-2">
                      <v-btn icon @click.stop :href="sponsoredItem.link" target="_blank">
                        <v-icon color="grey lighten-1">mdi-information</v-icon>
                      </v-btn>
                    </v-list-item-action>
                  </v-list-item>
                </template>
              </v-autocomplete>
            </v-col>
            <v-col :cols="3">
              <v-text-field
                placeholder="Amount"
                single-line
                class="rounded-card" solo dense
                hide-details="auto"
                type="number"
                v-model="portfolioAmount"
                :rules="[v => v > 0 || 'Enter an amount']"
                :validate-on-blur="true"

              />
            </v-col>
          </v-row>
          <v-row dense>
            <v-col class="text-right pt-4" dense>
              <v-btn type="submit" color="primary" small rounded class="font-weight-light">Add To {{activePlatform.str_name}}</v-btn>
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

export default {
  name: "AddPortfolio",
  inject: ["platformId", "scenarioId"],
  data() {
    return {
      dialog: false,
      newPortfolio: {},
      portfolioAmount: null,
      portfolioList: [],
      sponsoredItem: {
        id: 48,
        name: "A fourth portfolio",
        link: "https://www.google.com",
      },
    };
  },
  watch: {
    dialog() {
      if (this.$refs.form) {
        this.$refs.form.reset()
      } else {
        //pass
      }
    }
  },
  computed: {
    ...mapGetters(["activePlatform"]),
    filteredPortfolios() {
      return this.portfolioList.filter(i => (i.allowed_platforms.includes(this.activePlatform.name.id) || this._.isEmpty(i.allowed_platforms)))
    }
  },
  methods: {
    selectSponsored(){
      this.search = this.sponsoredItem.name;
      this.newPortfolio = this.sponsoredItem.id;
      this.$refs.autocomplete.isMenuActive = false;
    },
    getPortfolioList() {
      let endpoint = `/api/portfoliotemplates/`;
      apiService(endpoint, "GET").then(data => {
        this.portfolioList = data.results;
      });
    },
    onSubmit() {
      if (this.$refs.form.validate()) {
        let endpoint = `/api/scenarios/${this.scenarioId}/platforms/${this.platformId}/portfolios/`;
        apiService(endpoint, "POST", {
          name: "override",
          template_id: this.newPortfolio,
          platform: this.platformId,
          model_value: this.portfolioAmount,
          auto_created: false,
        }).then(data => {
          this.$emit("add-portfolio", data);
          this.newPortfolio = null;
          this.portfolioAmount = null;
          this.dialog = false;
        });
        if (this.error) {
          this.error = null;
        }
      }
    }
  },
  mounted() {
    this.getPortfolioList();
  }
};
</script>
