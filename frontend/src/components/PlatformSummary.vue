<template lang="html">
  <v-card
    class="half-rounded-card"
    color="#f1f3f7"
    elevation="0"
    @click="selectPlatform(platform)">
    <v-row dense>
      <v-col dense class="pb-0">
        <v-card-title class="pr-0 pb-0">
          <v-tooltip top>
            <template v-slot:activator="{ on }">
              <span
                ref="title"
                v-on="on"
                class="block text-truncate  font-weight-bold"
                style="max-width:170px; font-size:16px">
                {{ platform.custom_name ? platform.custom_name : platform.name.name}}
              </span>
            </template>
            {{ platform.custom_name ? platform.custom_name : platform.name.name}}
          </v-tooltip>
        </v-card-title>
      </v-col>
      <v-col class="text-right pr-4 pt-4 pl-0 pb-0" dense>
        <v-tooltip top>
          <template v-slot:activator="{ on }">
            <v-btn
              v-on="on"
              small
              icon
              @click="clonePlatform()"
              @click.stop >
             <v-icon color="grey" :small="true">
               mdi-content-copy
             </v-icon>
           </v-btn>
         </template>
         Duplicate
       </v-tooltip>
       <v-btn icon small >
         <DeleteObj
          @click.stop
          :small="true"
          :objectType="'platform'"
          :objectToDelete="platform"
          v-on="$listeners"/>
        </v-btn>
      </v-col>
    </v-row>
    <v-card-subtitle v-if="platform.account_number" class="pt-0 pb-2">
        {{ platform.account_number }}
    </v-card-subtitle>
    <v-card-text class="pt-2">
      <span class="black--text font-weight-medium">Balance: </span><span class="accent--text font-weight-medium">{{ platform.platform_total | toCurrency }}</span><br>
      <span class="black--text font-weight-medium">Fees: </span><span class="gray--text font-weight-medium">{{ platform.platform_total_fees | toCurrency }}</span>
    </v-card-text>
  </v-card>
</template>

<script>
import { apiService } from "@/common/api.service.js";
import DeleteObj from "@/components/DeleteObj.vue";
import {
  SET_ACTIVE_PLATFORM
} from "@/store/mutations.type";

export default {
  name: "PlatformSummary",
  inject: ["scenarioId"],
  props: {
    scenario: {
      type: Object,
      required: true
    },
    platform: {
      type: Object,
      required: true
    }
  },
  components: {
    DeleteObj
  },
  data() {
    return {
      error: null,
    };
  },
  methods: {
    selectPlatform(platform) {
      if (platform != null ) {
        this.$store.commit(SET_ACTIVE_PLATFORM, platform);
        this.$router.push({ name: 'platform',
             params: { scenarioId: this.scenarioId, id: platform.id }})
      }
    },
    clonePlatform() {
      const clone = Object.assign({}, this.platform);
      clone.id = null;
      clone.cloned = true;
      clone.clone_link = this.platform.id;
      if (clone.name) {
        clone.name_id = clone.name.id;
      } else {
        clone.name_id = null;
      }
      let endpoint = `/api/scenarios/${this.scenario.id}/platforms/`;
      apiService(endpoint, "POST", clone)
        .then(data => {
          this.$emit("clone-platform",data);
      })
    },
  },
};
</script>
