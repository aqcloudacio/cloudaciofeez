<template>
  <div>
    <AddScenario
      v-if="activeUser"
      :riskProfiles="riskProfiles"
      @add-scenario="addScenario" />
    <v-spacer><br>
    </v-spacer>
    <ScenarioSummary
      v-if="activeUser"
      :scenarios="scenarios"
      :riskProfiles="riskProfiles" />
    <v-dialog
      v-if="sponsoredItem"
      persistent
      max-width="700px"
      v-model="dialog">
      <v-card>
        <v-img :src="sponsoredItem.image">
        </v-img>
        <v-card-subtitle class="pa-0" align="end">
          Sponsored Content
        </v-card-subtitle>
      </v-card>
      <v-btn @click="dialog=false" :href="sponsoredItem.link" target="_blank">
        Tell me more
      </v-btn>
      <v-btn @click="dialog=false" :disabled="closeDisabled">
        Close
      </v-btn>
      <v-progress-linear
        class="modal-progress"
        :buffer-value="100"
        :value="timeLimit">
      </v-progress-linear>
    </v-dialog>
  </div>
</template>

<script>
import { apiService } from "@/common/api.service";
import ScenarioSummary from "@/components/ScenarioSummary.vue";
import AddScenario from "@/components/AddScenario.vue";

import {
  CLEAR_ACTIVE_SCENARIO
} from "@/store/mutations.type";
import {
  ADVERTS_ALL
} from "@/store/actions.type";
import { mapGetters } from "vuex";

export default {
  name: "home",
  data() {
    return {
      scenarios: [],
      next: null,
      loadingScenarios: false,
      requestUser: null,
      objectToDelete: null,
      riskProfiles: [],
      dialog: false,
      timeLimit: 0,
      timeMax: 5000,
      interval: 0,
      closeDisabled: true,
    };
  },
  components: {
    AddScenario,
    ScenarioSummary
  },
  computed: {
    ...mapGetters(["activeUser", "adverts"]),
    sponsoredItem() {
      let item = [];
      item = this.adverts.filter(x => x.type_name === "popover");
      return item[0]
    },
  },
  watch: {
    activeUser: function () {
      this.getRiskProfiles();
    },
  },
  methods: {
    getScenarios() {
      let endpoint = "/api/scenarios/";
      if (this.next) {
        endpoint = this.next;
      }
      this.loadingScenarios = true;
      apiService(endpoint).then(data => {
        this.scenarios = data.results;
        this.loadingScenarios = false;
        if (data.next) {
          this.next = data.next;
        } else {
          this.next = null;
        }
      });
    },
    getRiskProfiles() {
      if (this.activeUser.active_rp) {
        let endpoint = `/api/riskprofilegroups/${this.activeUser.active_rp}/riskprofiles/`;
        apiService(endpoint).then(data => {
          this.riskProfiles = data.results;
        });
      }
    },
    addScenario(newScenario) {
      this.scenarios.unshift(newScenario);
    },
    getAdverts() {
      if (this._.isEmpty(this.adverts)) {
      // Gets the ad info then calls the popover modal.
        this.$store.dispatch(ADVERTS_ALL).then(() => {
          this.loadModal();
        })
      } else {
        this.loadModal();
      }
    },
    loadModal() {
      this.startTimer();
      var nextPopup = localStorage.getItem( 'nextModalAd' );

      if (nextPopup > new Date()) {
        this.dialog = false;
      } else {
        this.dialog = true;
        window.setTimeout(() => {
          // Store the expiration date of the current popup in localStorage.
		      var expires = new Date();
		      expires = expires.setHours(expires.getHours() + 24);
		      localStorage.setItem( 'nextModalAd', expires );
          this.closeDisabled = false;
        }, this.timeMax);
      }
    },
    startTimer() {
      this.interval = setInterval(function() {

        if (this.timeLimit < 100) {
          this.timeLimit += 0.5;
        } else {
          clearInterval(this.interval)
          return;
        }
      }.bind(this), 25);
    },
    clearActiveScenario() {
      this.$store.commit(CLEAR_ACTIVE_SCENARIO);
    }
  },
  mounted() {
    this.getRiskProfiles();
    this.getScenarios();
    this.getAdverts();
    this.clearActiveScenario();
    document.title = "ProductRex";
  }
};
</script>

<style media="screen">
  .modal-progress {
   transition: none !important
  }
</style>
