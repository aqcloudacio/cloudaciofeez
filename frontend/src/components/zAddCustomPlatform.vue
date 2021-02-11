<template lang="html">
  <v-row>
  <v-dialog v-model="dialog">

    <v-card>
      <v-form @submit.prevent="onSubmit"
              class="pa-4">
        <v-row>
          <v-col :cols="10">
            <v-text-field
              dense solo hide-details
              v-model="platformName"
            />
          </v-col>
          <v-col :cols="2">
            <v-btn type="submit" color="primary" dense>Save</v-btn>
          </v-col>
        </v-row>
        <v-row>
            <v-col>
            <PlatformDetail
              v-if="showDetail == true"
              :platform="platform"
              :key="platformKey"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <PlatformFeeSummary
              v-if="showDetail == true"
              :platformFee="platformFee"
              :platform="platform.id"
              :key="platformKey"
            />
          </v-col>
        </v-row>
      </v-form>
    </v-card>
  </v-dialog>
</v-row>
</template>

<script>
import { apiService } from "@/common/api.service.js";
import PlatformDetail from "@/components/PlatformDetail.vue";
import PlatformFeeSummary from "@/components/PlatformFeeSummary.vue";

export default {
  name: "AddCustomPlatform",
  inject: ["scenarioId"],
  components: {
    PlatformDetail,
    PlatformFeeSummary
  },
  props: {
    dialog: {
      type: Boolean,
      required: true
    },
    status: {
      type: String,
      required: false,
    },
  },
  data() {
    return {
      platformName:"",
      platformFee: {},
      platform: null,
      showDetail: false,
      platformKey: 0,
    };
  },
  methods: {
    forceRerender(){
      this.platformKey += 1;
    },
    onSubmit() {
      if (this.platformName) {
        let endpoint = `/api/scenarios/${this.scenarioId}/platforms/`;
        apiService(endpoint, "POST", {
          name_id: null,
          custom_name: this.platformName,
          scenario: this.scenarioId,
          edited: true,
          status: this.status,
        }).then(data => {
          this.$emit("add-platform", data);
          console.log(data);
          this.platform = data;
          this.showDetail = true;
          this.forceRerender();
          this.getPlatformFeeData()
        });
        if (this.error) {
          this.error = null;
        }
      } else {
        this.error = "You must enter a platform name";
      }
    },
    getPlatformFeeData() {
      let endpoint = `/api/scenarios/${this.scenarioId}/platforms/${this.platform.id}/platformfees/`;
      apiService(endpoint).then(data => {
        this.platformFee = data.results[0];
      });
    }
  }
}
</script>

<style lang="css" scoped>
</style>
