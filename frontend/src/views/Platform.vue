<template>
  <div>
    <v-container class="fullwidthrow pa-0" style="background: #e4e7f0">
      <v-container style="width:1012px" class="pb-0">
        <v-card v-if="!_.isEmpty(activePlatform)"  class="pa-8 mt-4 rounded-card-top-only nobottomshadow">
        <PlatformDetail
          :platformFees="platformFees"
          @add-portfolio="getActivePlatform"
          @modify-fees="getActivePlatform"
        />
        <PlatformAAChartSummary
          v-if="!_.isEmpty(activePlatform) && !_.isEmpty(activeScenario)"
          />
        </v-card>
      </v-container>
    </v-container>
    <v-container
      class="white px-4 pt-0">
      <v-card class="rounded-card px-4 py-4" color="#f1f3f7">
        <InvestmentSummary
          :platformFees="platformFees"
          v-if="!_.isEmpty(activePlatform)"
          @delete-object="getActivePlatform"
          :platformTotal="activePlatform.platform_total"
        />
      </v-card>
    </v-container>
  </div>
</template>

<script>
import { apiService } from "@/common/api.service.js";
import PlatformDetail from "@/components/PlatformDetail.vue";
import InvestmentSummary from "@/components/InvestmentSummary.vue";
import PlatformAAChartSummary from "@/components/PlatformAAChartSummary.vue";
import {
  CLEAR_ACTIVE_PLATFORM,
  CLEAR_ACTIVE_SCENARIO,
  CLEAR_ACTIVE_PLATFORM_AA,
} from "@/store/mutations.type";
import {
  SCENARIO_FETCH,
  PLATFORM_FETCH,
  PLATFORM_AA_FETCH,
  PLATFORMNAME_ALL,
} from "@/store/actions.type";
import { mapGetters } from "vuex";



export default {
  name: "Platform",
  provide() {
    return {
      platformId: this.id,
      scenarioId: this.scenarioId
    };
  },
  props: {
    scenarioId: {
      type: String,
      required: true
    },
    id: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      AAChartKey: 0,
      platform: {},
      platformFees: [],
      error: null,
    };
  },
  components: {
    InvestmentSummary,
    PlatformDetail,
    PlatformAAChartSummary,
  },
  computed: {
    ...mapGetters(["activeScenario", "activeUser", "activePlatform"]),
  },
  watch: {
    activeScenario() {
      // In case activeScenario needs to be fetched and is slow
      this.getActivePlatformAA()
    }
  },
  methods: {
    getPlatformFeeData() {
      if (this._.isEmpty(this.platformFees)) {
        let endpoint = `/api/scenarios/${this.scenarioId}/platforms/${this.id}/platformfees/`;
        apiService(endpoint).then(data => {
          this.platformFees = data.results;
        });
      }
    },
    setActiveScenario(){
      if (this._.isEmpty(this.activeScenario)) {
        this.$store.dispatch(SCENARIO_FETCH, this.scenarioId);
      }
    },
    setActivePlatform(){
      if (this._.isEmpty(this.activePlatform)) {
        this.getActivePlatform();
      }
    },
    getActivePlatform() {
      this.$store.dispatch(PLATFORM_FETCH, {
        'scenarioId': this.scenarioId,
        'platformId': this.id
      }).then(() => {
        this.getPlatformFeeData();
        this.setActivePlatformAA();
      })
    },
    setActivePlatformAA(){
      if (this._.isEmpty(this.activePlatformAA)) {
        this.getActivePlatformAA();
      }
    },
    getActivePlatformAA() {
      // Waits until activeScenario and activePlatform have been fetched
      if (!this._.isEmpty(this.activeScenario) && !this._.isEmpty(this.activePlatform)) {
        this.$store.dispatch(PLATFORM_AA_FETCH, {
          'scenarioId': this.activeScenario.id,
          'platformId': this.activePlatform.id,
        })
      }
    },
    getPlatformNames() {
      if (this._.isEmpty(this.platformNames)) {
        this.$store.dispatch(PLATFORMNAME_ALL, null)
      }
    },
  },
  mounted() {
    this.setActiveScenario();
    this.setActivePlatform();
    this.getPlatformFeeData();
    this.setActivePlatformAA();
    this.getPlatformNames();
  },
  beforeDestroy() {
    this.$store.commit(CLEAR_ACTIVE_PLATFORM);
    this.$store.commit(CLEAR_ACTIVE_PLATFORM_AA);
  },
  beforeRouteLeave(to, from, next) {
    if (to.name != "scenario") {
      this.$store.commit(CLEAR_ACTIVE_SCENARIO);
    }
    next()
  }
};
</script>
