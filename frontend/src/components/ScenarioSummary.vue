<template lang="html">
  <v-container
    class="pt-0"
    fluid>
    <v-card
      :class="isExpanded(scenario) ? 'openCardStyle my-6 rounded-card' : 'closedCardStyle my-6 rounded-card primaryhalf'"
      v-for="scenario in scenarios.slice(0, scenariosToLoad)"
      :key="scenario.id"
      @click="selectScenario(scenario)">
      <v-container :class="isExpanded(scenario) ? expandedContainer : unexpandedContainer">
          <v-card-title :class="isExpanded(scenario) ? expandedHeaderClass : unexpandedHeaderClass"  >
            <template
              v-if="!isEditing(scenario.id)">
            {{ scenario.client }}
            </template>
            <v-text-field
              v-else
              @click.stop
              class="pb-2"
              v-model="scenario.client"
              hide-details="auto"
              :rules="[v => !!v || 'You must enter a client name']"/>
             <v-spacer/>
            <v-card-actions @click.stop>
              <v-btn
                icon
                small
                @click="editScenario(scenario)">
                <v-icon :color="(isEditing(scenario.id) || isExpanded(scenario)) ? 'white' : 'grey'">
                  mdi-circle-edit-outline
                </v-icon>
              </v-btn>
              <v-btn
                icon
                small
                @click="goReports(scenario)">
                <v-icon :color="isExpanded(scenario) ? 'white' : 'grey'">
                  mdi-file-document-outline
                </v-icon>
              </v-btn>
              <ShareScenario
                :scenario="scenario"
                @update-scenarios="updateScenarios($event)"
                :color="isExpanded(scenario) ? 'white' : 'grey'"
              />
              <v-btn icon small>
                <DeleteObj
                  :objectToDelete="scenario"
                  :objectType="'scenario'"
                  @delete-object="deleteObj"
                  :color="isExpanded(scenario) ? 'white' : 'grey'"
                />
              </v-btn>
            </v-card-actions>
            <v-btn
              @click.stop
              v-if="!isExpanded(scenario)"
              icon
              @click="addToExpanded(scenario)">
              <v-icon color="primary">
                mdi-plus
              </v-icon>
            </v-btn>
            <v-btn
              @click.stop
              v-else
              icon
              @click="removeFromExpanded(scenario)">
              <v-icon color="white">
                mdi-close
              </v-icon>
            </v-btn>
          </v-card-title>
        </v-container>
      <template v-if="isExpanded(scenario) || isEditing(scenario.id)">
        <v-row >
          <v-col :cols="2">
            <v-card-subtitle class="py-0">Balance:</v-card-subtitle>
            <v-card-text
              class="accent--text pb-0" style="font-size:14pt">
              {{ scenario.scenario_total | toCurrency }}
            </v-card-text>

          </v-col>
          <v-col :cols="2" @click.stop>
            <v-card-subtitle class="py-0">Risk Profile:</v-card-subtitle>
            <v-card-text
              v-if="!isEditing(scenario.id)"
              class="primary--text pb-0"  style="font-size:14pt">
              {{ scenario.risk_profile_name }}
            </v-card-text>
            <v-select

              class="pl-4 pt-0 mt-0"
              v-else
              :value="scenario.risk_profile"
              @input="scenario.risk_profile_id = $event"
              :items="riskProfiles"
              item-value="id"
              item-text="name"
              dense
              hide-details/>
          </v-col>

        </v-row>
        <v-divider class="mx-4 mt-0"/>
        <v-container>
          <v-row dense v-for="(status, index) in statuses" :key="index">
            <v-col dense :cols="2">
              <v-card-subtitle class="px-2 py-0 pt-1">
                {{status}}
              </v-card-subtitle>
            </v-col>
            <v-col :cols="10"  v-if="!_.isEmpty(scenario.platforms)">
              <v-chip
               small
                @click.stop
                v-for="platform in scenario.platforms.filter(i => i[2] === status)"
                :key="platform[0]"
                class="ma-1"
                color="primary"
                text-color="black"
                outlined
                :to="{ name: 'platform', params: { scenarioId: scenario.id, id: platform[0] } }">
                {{ platform[1] }}
              </v-chip>
            </v-col>
          </v-row>
        </v-container>
      </template>
    </v-card>

    <v-dialog
      v-if="clicked"
      max-width="500px"
      v-model="dialog">
      <v-card>
        <v-card-title class="headline grey lighten-2 pr-3">
          Mismatched Risk Profile Group
          <v-spacer></v-spacer>
          <v-btn
            color="secondary"
            text
            @click="dialog = false"
          >X</v-btn>
        </v-card-title>
        <v-container class="pa-3">
          <v-card-text>
          The risk profile assigned to this scenario is not part of your
          currently active Risk Profile Group.<br>
          <br>
          <strong>Currently Active Risk Profile Group:</strong> <br>{{activeUser.active_rp_name}}
          <br><br>
          <strong>Scenario's Risk Profile Group:</strong> <br>{{clicked.risk_profile_group_name}}
          <br><br>
          Please select one of the actions below:
          </v-card-text>
          <v-divider />
          <v-card-actions class="pb-0">
            <v-btn @click="abortChange()" text>
              Do nothing
            </v-btn>
          </v-card-actions>
          <v-card-actions class="py-0">
            <v-btn @click="changeRiskProfiler()" text>
              Change active Risk Profile Group
            </v-btn>
          </v-card-actions>
          <v-card-actions class="py-0">
            <v-btn @click="changeRiskProfile()" text>
              Change scenario's Risk Profile
            </v-btn>
          </v-card-actions>
        </v-container>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import DeleteObj from "@/components/DeleteObj.vue";
import { apiService } from "@/common/api.service.js";
import ShareScenario from "@/components/ShareScenario.vue";
import {
  SET_ACTIVE_SCENARIO
} from "@/store/mutations.type";
import { mapGetters } from "vuex";

export default {
  name: "ScenarioSummary",
  props: {
    scenarios: {
      type: Array,
      required: true
    },
    riskProfiles: {
      type: Array,
      required: true,
    },
  },
  components: {
    DeleteObj,
    ShareScenario,
  },
  data() {
    return {
      scenariosToLoad: 5,
      error: null,
      href: null,
      route: null,
      navigate: null,
      edit: [],
      proceed: true,
      dialog: false,
      clicked: null,
      expanded: [],
      statuses: [
        'Current',
        'Recommended',
        'Alternative',
      ],
      unexpandedHeaderClass: "pt-1 pb-1 ",
      expandedHeaderClass: "pt-1 pb-1  white--text ",
      unexpandedContainer: "ma-0 pa-0",
      expandedContainer: "ma-0 pa-0 openContainerStyle primary rounded-card-top-only",
    };
  },
  watch: {
    dialog() {
      // Allows other scenarios to be clicked if the dialog is closed by
      // clicking outside the box.
      if (!this.dialog) {
        this.clicked = null;
        this.proceed = true;
      }
    }
  },
  computed: {
    ...mapGetters(["activeUser"]),
  },
  methods: {
    addToExpanded(scenario) {
      if (!this.isExpanded(scenario.id)) {
        this.expanded.push(scenario.id)
      }
    },
    removeFromExpanded(scenario) {
      this.expanded = this.expanded.filter(i => i !== scenario.id);
      // Cancels the edit if closed while editing.
      if (this.isEditing(scenario.id)){
        this.edit.splice(this.edit.indexOf(scenario.id));
      }
    },
    isExpanded(scenario) {
      return this.expanded.includes(scenario.id)
    },
    checkRiskProfile(scenario) {
      // Checks that the risk profile for this scenario is in the active risk
      // profile group. If it isn't prompts the user to change as this causes
      // issues with the asset allocation charts.
      if (this.activeUser.active_rp != scenario.risk_profile.group && !this.dialog){
        this.proceed = false;
        this.dialog = true;
        this.clicked = scenario;
      }
    },
    changeRiskProfiler(){
      // Sends user to profile screen with a shortcut to risk profiles
      this.dialog = false;
      this.$router.push({ name: 'profile', params: { shortcut: 'riskProfile'} });
    },
    changeRiskProfile(){
      // Activates the edit functions for the scenario that has been clicked
      // so that the user can change the risk profile.
      this.dialog = false;
      this.editScenario(this.clicked);
      this.clicked = null;
    },
    abortChange() {
      this.dialog = false;
      this.clicked = null;
      this.proceed = true;
    },
    selectScenario(scenario) {
      this.checkRiskProfile(scenario);
      if (scenario != null && this.proceed ) {
        this.setActiveScenario(scenario);
        this.$router.push({ name: 'scenario', params: { id: scenario.id } })
      }
    },
    goReports(scenario) {
      this.setActiveScenario(scenario);
      this.$router.push({ name: 'reports', params: { scenarioId: scenario.id } })
    },
    setActiveScenario(scenario){
      this.$store.commit(SET_ACTIVE_SCENARIO, scenario);
      // Empty API patch to update the last_edited field of the scenario
      let endpoint = `/api/scenarios/${scenario.id}/`;
      apiService(endpoint, "PATCH", scenario);
    },
    deleteObj(objectToDelete) {
      this.$delete(this.scenarios, this.scenarios.indexOf(objectToDelete));
    },
    isEditing(scenario) {
      return this.edit.includes(scenario)
    },
    editScenario(scenario){
      // Adds the clicked scenario to the edit list (so they can edit multiple)
      // scenarios at once
      if (this.isEditing(scenario.id)) {
        this.edit.splice(this.edit.indexOf(scenario.id));
        this.onSubmit(scenario);
      } else {
        this.addToExpanded(scenario)
        this.edit.push(scenario.id);
      }
    },
    updateScenarios(scenario) {
      let idx = (this.scenarios.findIndex(i => i.id === scenario.id));
      this.scenarios[idx] = scenario;

    },
    onSubmit(scenario){
      if (scenario.client) {
        let endpoint = `/api/scenarios/${scenario.id}/`;
        apiService(endpoint, "PATCH", scenario
          ).then(data => {
          this.updateScenarios(data);
          this.proceed = true;
          this.removeFromExpanded(data)
        });
      }
    }
  }
};
</script>
<style scoped>
  /* .openHeaderStyle {
    box-sizing: border-box !important;
    border-collapse: collapse !important;
    border-spacing: 0 !important;
    box-sizing: border-box !important;

  }
  .openContainerStyle {
    background-color: #47b27a !important;
    border-collapse:  collapse !important;
    border-spacing: 0 !important;
    box-sizing: border-box !important;

  } */
  .openCardStyle {
    box-shadow: inset 0px 0px 0px 2px #47b27a !important;
    /* border-color: #47b27a !important; */
    /* border-style: solid; */
    border-collapse:  collapse !important;
    border-spacing: 0 !important;
    box-sizing: border-box !important;
  }
  .closedCardStyle {
    box-shadow: 0px 0px 0px 0px !important;
  }
</style>
