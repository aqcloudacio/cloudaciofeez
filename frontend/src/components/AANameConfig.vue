<template lang="html">
  <v-dialog v-model="dialog" max-width="1000px">
    <template v-slot:activator="{ on }">
      <v-btn color="primary" dark v-on="on" icon>
        <v-icon>mdi-pencil-circle
        </v-icon>
      </v-btn>
    </template>
    <v-card>
      <v-card-title class="headline grey lighten-2 pr-3">
        Configure Risk Profile Asset Names
        <v-spacer></v-spacer>
        <v-btn
          color="secondary"
          text
          @click="dialog = false"
        >X</v-btn>
      </v-card-title>
      <v-container>
        <v-form
          @submit.prevent="onSubmit"
          ref="form">
          <v-row dense>
            <v-col
              :cols="2">
              <v-card dense>
                <v-card-title>
                  Asset Type
                </v-card-title>
              </v-card>
            </v-col>
            <v-col
              :cols="5">
              <v-card dense>
                <v-card-title>
                  Custom Asset Name
                </v-card-title>
              </v-card>
            </v-col>
            <v-col
              :cols="5">
              <v-card dense>
                <v-card-title>
                  Asset Description
                </v-card-title>
              </v-card>
            </v-col>
          </v-row>
          <v-row
            v-for="AAName in RPAANames"
            :key="AAName.id" dense>
            <v-col
              :cols="2">
                <v-select
                  @change="addToModified(AAName)"
                  v-model="AAName.asset_type"
                  :items="assetTypes"
                  outlined dense hide-details/>
            </v-col>
            <v-col
              :cols="5">
                <v-text-field
                  @keyup="addToModified(AAName)"
                  v-model="AAName.custom_name"
                  outlined dense
                  hide-details="auto"
                  validate-on-blur
                  :rules="[v => !!(v) || 'You must enter a name']"/>
            </v-col>
            <v-col
              :cols="5">
              <v-card dense class="pa-0">
                <v-card-text class="pa-2">
                  {{ AAName.name }}
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
          <v-card-actions class="pr-0">
            <v-spacer />
            <v-btn  type="submit" color="primary" text>Save</v-btn>
          </v-card-actions>
        </v-form>
      </v-container>
    </v-card>
  </v-dialog>
</template>

<script>
import { apiService } from "@/common/api.service.js";

export default {
  name: "AANameConfig",
  props: {
    RPAANames: {
      type: Array,
      required: true,
    }
  },
  data() {
    return {
      dialog: false,
      assetTypes: [
        "Defensive",
        "Growth",
        "Alternative"
      ],
      modifiedList: [],
    };
  },
  methods: {
    addToModified(item) {
      if (!(this.modifiedList.includes(item))) {
        this.modifiedList.push(item);
      }
    },
    onSubmit() {
      if (this.$refs.form.validate()) {
        for (let i=0; i< this.modifiedList.length; i++){
          let endpoint = `/api/riskprofilegroups/${this.modifiedList[i].group}/riskprofilenames/${this.modifiedList[i].id}/`;
          apiService(endpoint, "PATCH", {
            custom_name: this.modifiedList[i].custom_name,
            asset_type: this.modifiedList[i].asset_type,
          }).then(() => {
            this.dialog = false;
          })
        }
      }
    }
  },
  mounted() {
  }
};
</script>
