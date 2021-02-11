<template lang="html">
  <div>
    <v-toolbar color="secondary" dark dense prominent  class="shrink">
      <v-container style="width: 1012px; height:100%">
        <v-row >
          <v-col align-self="center" :cols="4" >
            <v-toolbar-title large class="pb-0">
              <v-img src="../assets/PRLogo.png">
              </v-img>
              </v-toolbar-title>
          </v-col>
          <v-col :cols="4" align="right" align-self="center">
            <v-autocomplete
            dense
              background-color="secondary lighten-2"
              rounded solo
              :items="scenarios"
              v-model="selectedScenario"
              no-data-text="Client not found"
              item-text="client"
              return-object
              hide-details
              ref="autocomplete"
              prepend-inner-icon="mdi-magnify"
              style="width: 300px"
              @change="goNewScenario"/>
          </v-col>
          <v-spacer />
            <v-card-actions>
              <v-btn icon dark @click="goProfile">
                <v-icon>mdi-account-outline</v-icon>

              </v-btn>
              <span v-if="!_.isEmpty(activeUser.name)" dark  @click="goProfile" class="scenarioLink">
                {{activeUser.name}}
              </span>
              <Notifications/>

              <!-- <v-divider inset vertical  class="mx-4" style="height:30px"/> -->
              <v-btn icon  small>
                <v-icon color="PRgrey">mdi-help-circle-outline</v-icon>
              </v-btn>
              <v-btn icon small @click="logout"  >
                <v-icon color="PRgrey">mdi-power</v-icon>
              </v-btn>
          </v-card-actions>

        </v-row>
      </v-container>
    </v-toolbar>
    <v-toolbar color="primary" short class="shrink">
      <v-container style="width: 1012px">
        <v-row>
          <v-col align-self="center">
            <v-toolbar-title>
              <v-btn icon @click="goHome" dark large>
                <v-icon>mdi-home-circle-outline</v-icon>
              </v-btn>
              <template v-if="activeScenario.id">
                <v-icon dark>mdi-chevron-right</v-icon>
                <span class="scenarioLink" @click="goScenario" style="color:white">  {{activeScenario.client}}</span>
              </template>
              <template v-if="activePlatform.id != null">
                <v-icon dark>mdi-chevron-right</v-icon>
                <span style="color:white">  {{customName}}</span>
              </template>
            </v-toolbar-title>
          </v-col>
          <!-- <v-col align="right"  >

        </v-col> -->
        <v-card-actions v-if="activeScenario.id">
          <v-spacer></v-spacer>
          <v-btn icon @click="goDocs" dark>
            <v-icon>mdi-file-document-outline</v-icon>
          </v-btn>
          <ShareScenario
            :scenario="activeScenario"
            :color="'white'"
          />
        </v-card-actions>
      </v-row>
      </v-container>
    </v-toolbar>
  </div>
</template>

<script>
import { apiService } from "@/common/api.service";
import Notifications from "@/components/Notifications.vue";
import { mapGetters } from "vuex";
import { SET_ACTIVE_SCENARIO } from "@/store/mutations.type";
import {
  ADVERTS_ALL,
  USER_LOGOUT,
} from "@/store/actions.type";
import ShareScenario from '@/components/ShareScenario.vue';

export default {
  components: {
    Notifications,
    ShareScenario,
  },
  data() {
    return {
      scenarios: [],
      selectedScenario: null,
    }
  },
  computed: {
    ...mapGetters(["activeScenario", "activeUser", "activePlatform", "adverts"]),
    customName() {
      if (this.activePlatform.name == null) {
        return this.activePlatform.custom_name;
      } else if (this.activePlatform.custom_name != null) {
        return this.activePlatform.custom_name;
      } else if (this.activePlatform.name) {
        return this.activePlatform.name.name;
      } else {
        return null;
      }
    },
  },
  methods: {
    getAdverts() {
      if (this._.isEmpty(this.adverts)) {
        this.$store.dispatch(ADVERTS_ALL)
      }
    },
    getScenarios() {
      let endpoint = "/api/scenarios/";
      apiService(endpoint).then(data => {
        this.scenarios = data.results;
      });
    },
    goHome() {
      const path = `/`
      if (this.$route.path !== path)  {
        this.$router.push({ name: 'home' });
      }
    },
    goNewScenario() {
      if (!this._.isEmpty(this.selectedScenario)) {
        this.$refs.autocomplete.blur();
        this.$nextTick(() => {
          this.$store.commit(SET_ACTIVE_SCENARIO, this.selectedScenario);
          // Empty API patch to update the last_edited field of the scenario
          let endpoint = `/api/scenarios/${this.selectedScenario.id}/`;
          apiService(endpoint, "PATCH", this.selectedScenario);
          // Nav to the scenario and reset the searchbar
          this.$router.push({ name: 'scenario', params: { id: this.selectedScenario.id } });
          this.selectedScenario = null;
        });
      }
    },
    goScenario() {
      const pathName = 'scenario'
      if (this.$route.name !== pathName) {
        this.$router.push({ name: 'scenario', params: { id: this.activeScenario.id } });
      }
    },
    goProfile() {
      const path = `/profile`
      if (this.$route.path !== path)  {
        this.$router.push({ name: 'profile' });
      }
    },
    goDocs() {
      const pathName = `reports`
      if (this.$route.name !== pathName)  {
        if (this.activeScenario.id != null) {
          this.$router.push({ name: 'reports', params: { scenarioId: this.activeScenario.id } });
        }
      }
    },
    logout() {
      this.$store.dispatch(USER_LOGOUT);
    },
  },
  mounted() {
    this.getScenarios();
    this.getAdverts();
  }
}
</script>
<style media="screen">
  .noTransition::after {
  transition: none !important;
  background-color: transparent !important;
  }
  .scenarioLink {
  cursor: pointer;
  }
</style>
