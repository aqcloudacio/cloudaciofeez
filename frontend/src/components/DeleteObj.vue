<!-- This is a generic component that deletes the object that is passed in, then
passes back the object so it can be removed from the displayed array. -->

<template>
  <v-dialog v-model="dialog" max-width="320" class="transparent">
    <template v-slot:activator="{ on }">
        <v-icon
          :color="color ? color : 'grey'"
          v-on="on"
          :small="small ? small : false">
          mdi-delete-outline
        </v-icon>
    </template>
    <v-card class="small-text">
      <v-card-title class="dialog-header">
        Delete {{ getObjectName(objectType) }}
        <v-spacer></v-spacer>
        <v-btn
          text
          @click="dialog = false" icon
          ><v-icon color="grey">mdi-close-circle-outline</v-icon></v-btn>
      </v-card-title>
      <v-container class="dialog-container">
        <v-card-text class="pa-0" style="font-size: 0.8em">
          Are you sure you want to permanently delete this {{ getObjectName(objectType) }}?
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn @click="dialog = false" small text>
            Cancel
          </v-btn>
          <v-btn @click="deleteObj" class="primary-action-button">
            Delete
          </v-btn>
        </v-card-actions>
      </v-container>
    </v-card>
  </v-dialog>
</template>

<script>
import { apiService } from "@/common/api.service.js";
export default {
  name: "DeleteObj",
  inject: {
    platformId: { default: "" },
    platformFeeId: { default: "" },
    scenarioId: { default: "" }
  },
  props: {
    objectToDelete: {
      type: Object,
      required: true
    },
    portfolioID: {
      type: Number,
      required: false
    },
    objectType: {
      type: String,
      required: true
    },
    shownRP: {
      type: Number,
      required: false
    },
    small: {
      type: Boolean,
      required: false,
    },
    color: {
      type: String,
      required: false,
    },
  },
  data() {
    return {
      error: null,
      dialog: false,
    };
  },
  methods: {
    async deleteObj() {
      if (this.objectType == "scenario") {
        let endpoint = `/api/scenarios/${this.objectToDelete.id}/`;
        await apiService(endpoint, "DELETE");
      } else if (this.objectType == "platform") {
        let endpoint = `/api/scenarios/${this.scenarioId}/platforms/${this.objectToDelete.id}/`;
        await apiService(endpoint, "DELETE");
      } else if (this.objectType == "investment") {
        let endpoint = `/api/scenarios/${this.scenarioId}/platforms/${this.platformId}/investments/${this.objectToDelete.id}/`;
        await apiService(endpoint, "DELETE");
      } else if (this.objectType == "riskprofile") {
        let endpoint = `/api/riskprofilegroups/${this.shownRP}/riskprofiles/${this.objectToDelete.id}/`;
        await apiService(endpoint, "DELETE");
      } else if (this.objectType == "riskprofilegroup") {
        let endpoint = `/api/riskprofilegroups/${this.objectToDelete.id}/`;
        await apiService(endpoint, "DELETE");
      } else if (this.objectType == "model portfolio") {
        let endpoint = `/api/portfoliotemplates/${this.objectToDelete.id}/`;
        await apiService(endpoint, "DELETE");
      } else if (this.objectType == "modelInvestment") {
        let endpoint = `/api/portfoliotemplates/${this.portfolioID}/investments/${this.objectToDelete.id}/`;
        await apiService(endpoint, "DELETE");
      } else if (this.objectType == "theme") {
        let endpoint = `/api/themes/${this.objectToDelete.id}/`;
        await apiService(endpoint, "DELETE");
      }
      this.$emit("delete-object", this.objectToDelete);
      this.dialog = false;
    },
    getObjectName(name) {
      if (name === 'riskprofile') {
        return 'risk profile'
      } else if (name === 'modelInvestment') {
        return 'investment'
      } else if (name === 'riskprofilegroup') {
        return 'risk profile group'
      } else {
        return name
      }
    }
  }
};
</script>
