<template lang="html">
  <v-container class="fullwidthrow pa-0 grey1" style="height:100%">
    <v-container style="width:1012px">
      <v-row>
        <v-col>
          <v-card class="pa-6 rounded-card">
            <v-row dense>
              <v-col :cols="8">
                <v-row class="text-center">
                  <v-col>
                    <v-btn x-large rounded color="primary" @click="getReport" class="pl-4 pa-2 mt-2">
                      Get ProductRex<v-btn class="ml-4" small fab depressed dark color="rgb(48,133,89)" @click="getReport"><v-icon>mdi-download</v-icon></v-btn>
                    </v-btn>

                  </v-col>
                </v-row>
                <span color="danger" v-if="error">
                  {{error}}
                </span>
                <v-row>
                  <v-col>
                    <v-container class="pl-0 pt-8 pb-6 pr-4" v-if="sponsoredItem">
                      <v-img class="half-rounded-card" :src="sponsoredItem.image"></v-img>
                      <v-card-subtitle style="font-size: 0.8em" class="pa-0" align="end">
                        <em>Sponsored</em>
                      </v-card-subtitle>
                    </v-container>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col>
                    <v-select
                      class="rounded-card pr-4 small-text"
                      :value="activeScenario.theme"
                      @change="changeTheme($event)"
                      :items="themes"
                      item-text="name"
                      item-value="id"
                      label="Theme"
                      outlined hide-details dense>
                      <template v-slot:append-outer>
                        <v-icon
                          v-if="themeChanged"
                          color="green" icon
                          @click="saveTheme()">mdi-check-circle</v-icon>
                        <v-icon
                          v-if="!themeChanged"
                          color="green" icon
                          @click="toggleThemeSettings()">mdi-wrench</v-icon>
                      </template>
                    </v-select>
                  </v-col>
                </v-row>
              </v-col>
              <!-- <v-divider vertical /> -->
              <template v-if="reports">
                <v-col :cols="4">
                  <v-card class="half-rounded-card grey2 pa-6 pt-4" flat>
                    <v-list dense class="py-1 overflow-y-auto transparent" style="max-height:315px">
                      <v-list-item
                        class="px-0"
                        v-if="loading"
                        dense
                        two-line>
                        <v-list-item-content>
                          <v-list-item-title>{{ loadingText }}
                          </v-list-item-title>
                        </v-list-item-content>
                      </v-list-item>
                      <v-divider v-if="loading"></v-divider>
                      <!-- <template v-for="(report, index) in reports.slice(0, reportsToLoad)"> -->
                      <template v-for="report in reports.slice(0, reportsToLoad)">
                        <v-list-item
                          dense
                          two-line
                          :key="report.id"
                          :href="report.file">
                          <v-list-item-content>
                            <v-list-item-title>ProductRex for {{activeScenario.client}}
                            </v-list-item-title>
                            <v-list-item-subtitle style="font-size: 0.75em">Created: {{report.created_at}}
                            </v-list-item-subtitle>
                          </v-list-item-content>
                        </v-list-item>
                        <!-- <v-divider
                          v-if="index != reports.length-1 && index != reportsToLoad-1"
                          :key="index">
                        </v-divider> -->
                      </template>
                    </v-list>
                    <v-btn
                      style="width:100%"
                      rounded
                      small
                      class="grey1"
                      elevation="0"
                      @click="reportsToLoad += 5"
                      v-if="reports.length > 5 && reportsToLoad < reports.length">
                      View More
                    </v-btn>
                  </v-card>
                </v-col>
              </template>
            </v-row>
            <v-divider
              class="mb-4 mt-8"
              v-show="activeScenario && showThemeSettings && !themeChanged"/>
            <v-row v-show="activeScenario && showThemeSettings && !themeChanged">
              <v-col>
                <ThemeTable
                  v-if="activeScenario"
                  :user="activeUser"
                  :scenario="activeScenario"
                  @load-themes="loadThemes($event)"/>
              </v-col>
            </v-row>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-container>
</template>

<script>
import { apiService } from "@/common/api.service.js";
import ThemeTable from "@/components/ThemeTable.vue";
import { mapGetters } from "vuex";
import {
  SCENARIO_UPDATE_PROP,
  SCENARIO_FETCH,
 } from "@/store/actions.type";
 import {
   CLEAR_ACTIVE_SCENARIO,
 } from "@/store/mutations.type";

export default {
  name: "Output",
  props: {
    scenarioId: {
      type: String,
      required: true,
    }
  },
  data() {
    return {
      reportsToLoad: 5,
      error: null,
      reports: null,
      themes: [],
      showThemeSettings: false,
      newTheme: null,
      loading: false,
      timer: null,
      loadingText: 'Creating Report',
      text: [
        "Reticulating Splines",
        "Adjusting Bell Curves",
        "Aligning Covariance Matrices",
        "Asserting Packed Exemplars",
        "Growing Data Trees",
        "Attemping to Lock Back-Buffer",
        "Compounding Inert Tessellations",
        "Computing Optimal Bin Packing",
        "Containing Existential Buffer",
        "Decomposing Singularities",
        "Extracting Resources",
        "Integrating Curves",
        "Iterating Cellular Automata",
        "Lecturing Errant Subsystems",
        "Obfuscating Quigley Matrix",
        "Realigning Alternate Timeframes",
        "Reverse Engineering Image Consultant",
        "Sequencing Particles",
        "Time-Compressing Simulator Clock",
      ]
    };
  },
  components: {
    ThemeTable,
  },
  computed: {
    ...mapGetters(["activeScenario", "activeUser", "adverts"]),
    themeChanged() {
      if (this.newTheme === null) {
        return false
      } else {
        return !(this.newTheme === this.activeScenario.theme)
      }
    },
    sponsoredItem() {
      let item = [];
      item = this.adverts.filter(x => x.type_name === "document_cta");
      return item[0]
    },
  },
  methods: {
    generateText() {
      let _self = this;
      this.timer = setInterval(function() {
        let max = _self.text.length;
        let i = Math.floor(Math.random() * Math.floor(max));
        _self.loadingText =  _self.text[i];
      }, 1500);
    },
    changeTheme(event) {
      this.newTheme = event;
    },
    toggleThemeSettings(){
      this.showThemeSettings = !this.showThemeSettings;
    },
    loadThemes(event){
      this.themes = event;
    },
    saveTheme(){
      if (this.showThemeSettings) {
        this.toggleThemeSettings();
      }
      if (this.newTheme != this.activeScenario.theme) {
        this.$store.dispatch(SCENARIO_UPDATE_PROP, {
          'prop': 'theme',
          'value': this.newTheme
        }).then(() => {
          this.newTheme = null
        })
      }
    },
    getAllReports() {
      let endpoint = `/api/scenarios/${this.activeScenario.id}/reports/`;
      apiService(endpoint).then(data => {
        this.reports = data.results;
        clearInterval(this.timer);
        this.loading = false;
      });
    },
    getReport() {
      if (this.error) {
        this.error = null;
      }
      if (!this.activeScenario.theme) {
        this.error = "You must select a Theme from the dropdown below"
      } else {
        this.loading = true;
        this.generateText();
        let endpoint = `/api/scenarios/${this.activeScenario.id}/reports/`;
        apiService(endpoint, "POST", {scenario: this.activeScenario.id}).then(data => {
          this.reports.unshift(data)
          clearInterval(this.timer);
          this.loading = false;
        }).catch(() => {
          this.error = "The document could not be generated.";
          this.loading = false;
        })
      }
    },
    setActiveScenario(){
      if (this._.isEmpty(this.activeScenario) && this.scenarioId) {
        this.$store.dispatch(SCENARIO_FETCH, this.scenarioId).then(() => {
          this.getAllReports();
        });
      } else {
        this.getAllReports()
      }
    },
  },
  mounted() {
    this.setActiveScenario();
  },
  beforeRouteLeave(to, from, next) {
    if (to.name != "scenario") {
      this.$store.commit(CLEAR_ACTIVE_SCENARIO);
    }
    next()
  }
};
</script>

<style scoped>
.v-list-item {
  padding:0
}
</style>
