<template>
  <div>
    <v-container class="fullwidthrow pa-0" style="background: #e4e7f0">
      <v-container style="width:1012px" class="pb-0">
        <v-card v-if="activeScenario"  class="pt-8 px-8 mt-4 rounded-card-top-only nobottomshadow">
          <v-row>
            <v-col dense :cols="4">
              <span class="display-1 font-weight-medium"><strong>{{ activeScenario.client }}</strong></span>
            </v-col>
            <v-divider vertical inset/>
            <v-col>
              <Healthcheck
                :currentPlatforms="currentList"
                :recommendedPlatforms="recommendedList"
                :alternativePlatforms="alternativeList"
              />
            </v-col>
          </v-row>
            <v-row>
              <v-col :cols="4">
                <FeeChartSummary
                  :currentPlatforms="currentList"
                  :recommendedPlatforms="recommendedList"
                  :alternativePlatforms="alternativeList"
                />
              </v-col>
              <v-col :cols="8">
                <ScenarioAAChartSummary
                  :riskProfile="riskProfile"
                  :key="AAChartKey"
                />
              </v-col>
            </v-row>
            <v-row>
              <template
                v-for="status in statuses">
                <v-col
                  :key="status">
                  <v-card-title
                    class="justify-center py-0 subtitle-1 font-weight-medium">
                  {{ status }}
                  </v-card-title>
                </v-col>
              </template>
            </v-row>
        </v-card>
      </v-container>
    </v-container>

    <v-container
      class="white px-4 pt-0">
      <v-row>
        <v-col class="pt-0">
          <v-divider style="height:4px; max-height:4px" class="primary" />

          <v-card class="px-4 half-rounded-card-bottom-only" elevation="4">
            <v-row>
              <v-col>
                <AddPlatform
                  :status="'Current'"
                  :currentType="currentType"
                  @add-platform="addPlatform" />
              </v-col>
            </v-row>
            <v-row>
              <v-col class="pt-0">
                <v-row>
                  <draggable
                    class="dragList"
                    v-model="currentList"
                    group="statusLists"
                    @start="drag=true"
                    @end="drag=false"
                    @change="updateStatus('Current', $event)"
                    :emptyInsertThreshold="5"
                    >
                    <v-col
                      v-for="platform in currentList"
                      :key="platform.id">
                      <PlatformSummary
                        :scenario="activeScenario"
                        :platform="platform"
                        @delete-object="deleteObj"
                        @clone-platform="clonePlatform"
                      />
                    </v-col>
                  </draggable>
                </v-row>
              </v-col>
            </v-row>
          </v-card>
        </v-col>
        <v-col class="pt-0">

          <v-divider style="height:4px; max-height:4px" class="primary" />

          <v-card class="px-4 half-rounded-card-bottom-only" elevation="4">
            <v-row>
              <v-col>
                <AddPlatform
                  :status="'Recommended'"
                  :currentType="currentType"
                  @add-platform="addPlatform" />
              </v-col>
            </v-row>
            <v-row>
            <v-col class="pt-0">
              <v-row>
                <draggable
                  class="dragList"
                  v-model="recommendedList"
                  group="statusLists"
                  @start="drag=true"
                  @end="drag=false"
                  @change="updateStatus('Recommended', $event)"
                  :emptyInsertThreshold="5">
                  <v-col
                    v-for="platform in recommendedList"
                    :key="platform.id">
                    <PlatformSummary
                      :scenario="activeScenario"
                      :platform="platform"
                      @delete-object="deleteObj"
                      @clone-platform="clonePlatform"
                    />
                  </v-col>
                </draggable>
              </v-row>
            </v-col>
          </v-row>
        </v-card>

      </v-col>
      <v-col class="pt-0">
        <v-divider style="height:4px; max-height:4px" class="primary" />

        <v-card class="px-4 half-rounded-card-bottom-only" elevation="4">
          <v-row>
            <v-col>
              <AddPlatform
                :status="'Alternative'"
                :currentType="currentType"
                @add-platform="addPlatform" />
            </v-col>
          </v-row>
          <v-row>
            <v-col class="pt-0">
              <v-row>
                <draggable
                  class="dragList"
                  v-model="alternativeList"
                  group="statusLists"
                  @start="drag=true"
                  @end="drag=false"
                  @change="updateStatus('Alternative', $event)"
                  :emptyInsertThreshold="5">
                  <v-col
                    v-for="platform in alternativeList"
                    :key="platform.id">
                    <PlatformSummary
                      :scenario="activeScenario"
                      :platform="platform"
                      @delete-object="deleteObj"
                      @clone-platform="clonePlatform"
                    />
                  </v-col>
                </draggable>
              </v-row>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>

    </v-container>
  </div>
</template>

<script>
import { apiService } from "@/common/api.service.js";
import AddPlatform from "@/components/AddPlatform.vue";
import PlatformSummary from "@/components/PlatformSummary.vue";
import Healthcheck from "@/components/Healthcheck.vue";
import FeeChartSummary from "@/components/FeeChartSummary.vue";
import ScenarioAAChartSummary from "@/components/ScenarioAAChartSummary.vue";
import draggable from 'vuedraggable'
import { mapGetters } from "vuex";
import { SCENARIO_FETCH } from "@/store/actions.type";
import {
  CLEAR_ACTIVE_SCENARIO,
} from "@/store/mutations.type";
import {
  PLATFORMNAME_ALL
} from "@/store/actions.type";

export default {
  name: "Scenario",
  provide() {
    return {
      scenarioId: this.id
    };
  },
  props: {
    id: {
      type: String,
      required: true
    }
  },
  components: {
    AddPlatform,
    PlatformSummary,
    draggable,
    Healthcheck,
    FeeChartSummary,
    ScenarioAAChartSummary,
  },
  data() {
    return {
      AAChartKey: 0,
      scenario: null,
      platforms: [],
      error: null,
      next: null,
      currentList: [],
      recommendedList: [],
      alternativeList: [],
      clone: {},
      statuses: [
        "Current",
        "Recommended",
        "Alternative"
      ],
    };
  },
  watch: {
    id() {
      this.setActiveScenario();
    },
  },
  computed: {
    ...mapGetters(["activeScenario", "activeUser", "platformNames"]),
    currentType() {
      // Returns the platform type of the first item added to the current list.
      // This is passed to platformSummary for targeted sponsored products
      if (this.currentList.length > 0) {
        const result = this.currentList.reduce((r, o) =>
          o.create_date < r.create_date  ? o : r);
        return result.platform_type
      } else {
        return null
      }
    },
    riskProfile() {
      if (!this._.isEmpty(this.activeScenario.risk_profile)) {
        return this.activeScenario.risk_profile;
      } else {
        return {}
      }
    },
  },
  methods: {
    forceRerender() {
      // Forces the AA Chart to call the API data when a platform is moved.
      this.AAChartKey += 1;
    },
    allocateToList(platform) {
      if (platform.status == "Current") {
        this.currentList.push(platform);
      } else if (platform.status == "Recommended") {
        this.recommendedList.push(platform);
      } else if (platform.status == "Alternative") {
        this.alternativeList.push(platform);
      }
    },
    sortPlatforms() {
      this.platforms.forEach((platform) => {
        this.allocateToList(platform);
      })
    },
    checkNull(list) {
      if (list.length > 0) {
        return list;
      }
    },
    setPageTitle(title) {
      document.title = title;
    },
    getScenarioPlatforms() {
      let endpoint = `/api/scenarios/${this.id}/platforms/`;
      if (this.next) {
        endpoint = this.next;
      }
      apiService(endpoint).then(data => {
        this.platforms.push(...data.results);
        this.sortPlatforms();
        if (data.next) {
          this.next = data.next;
          this.getScenarioPlatforms();
        } else {
          this.next = null;
        }
      });
    },
    addPlatform(platform) {
      this.platforms.push(platform);
      this.allocateToList(platform);
    },
    deleteObj(objectToDelete) {
      if (objectToDelete.status == "Current") {
        this.currentList.splice(this.currentList.indexOf(objectToDelete),1);
      } else if (objectToDelete.status == "Recommended") {
        this.recommendedList.splice(this.recommendedList.indexOf(objectToDelete),1);
      } else if (objectToDelete.status == "Alternative") {
        this.alternativeList.splice(this.alternativeList.indexOf(objectToDelete),1);
      } else {
        console.log(objectToDelete);
      }
      let deletedPlatform = this.platforms.indexOf(objectToDelete)
      this.$delete(this.platforms, deletedPlatform);
      this.forceRerender()
    },
    updateStatus(status, {added}) {
      if (added != undefined) {
        let changedPlatform = this.platforms[this.platforms.indexOf(added.element)];
        changedPlatform.status = status;
        this.patchPlatformStatus(changedPlatform);
      }
    },
    clonePlatform(clone) {
      this.addPlatform(clone);
      this.forceRerender()
    },
    patchPlatformStatus(platform) {
      let endpoint = `/api/scenarios/${this.id}/platforms/${platform.id}/`;
      apiService(endpoint, "PATCH", {status: platform.status}).then(() =>
        this.forceRerender()
      )
    },
    setActiveScenario(){
      if (this._.isEmpty(this.activeScenario)) {
        this.$store.dispatch(SCENARIO_FETCH, this.id);
      }
    },
    getPlatformNames() {
      if (this._.isEmpty(this.platformNames)) {
        this.$store.dispatch(PLATFORMNAME_ALL, null)
      }
    },
  },
  mounted() {
    this.getScenarioPlatforms();
    this.setActiveScenario();
    this.getPlatformNames();
  },
  beforeRouteLeave(to, from, next) {
    if (to.name != "platform" && to.name != "reports") {
      this.$store.commit(CLEAR_ACTIVE_SCENARIO);
    }
    next()
  }
};
</script>
<style media="screen">
  .dragList {
    width: 100%;
    min-height: 300px;
  }
</style>
