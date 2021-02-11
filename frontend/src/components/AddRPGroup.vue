<template lang="html">
  <v-dialog v-model="dialog"  width='600px'>
    <template v-slot:activator="{ on }">
      <v-btn icon  dark v-on="on">
        <v-icon color="primary">mdi-plus-circle</v-icon>
      </v-btn>
    </template>
    <v-card class="small-text">
      <v-card-title class="dialog-header">
        Add Risk Profile Group
        <v-spacer></v-spacer>
        <v-btn
          text
          @click="dialog = false" icon
        ><v-icon color="grey">mdi-close-circle-outline</v-icon></v-btn>
      </v-card-title>
      <v-container class="dialog-container">
        <v-form
          @submit.prevent="onSubmit"
          v-if="newRPGroup != null"
          ref="form"
          >
          <v-row dense>
            <v-col>
              <v-text-field
                placeholder="Enter a name for your Risk Profile Group"
                class="rounded-card" solo dense
                v-model="newRPGroup.name"
                :rules="[v => !!(v) || 'You must enter a name']"
                hide-details="auto" />
            </v-col>
          </v-row>
          <v-row
           dense
            class="pa-4"
            v-if="userID === null">
            <v-col :cols="7">
              <v-autocomplete
                label="AFSL Limitation"
                single-line outlined dense
                :items="AFSLList"
                item-text="name"
                item-value="id"
                v-model="newRPGroup.AFSL_limitation"
             />
            </v-col>
            <v-col :cols="3">
              <v-checkbox
                label="Default Template?"
                single-line outlined dense
                v-model="newRPGroup.default" />
            </v-col>
          </v-row>
          <v-card-actions class="pr-0">
            <v-spacer />
            <v-btn  type="submit" class="primary-action-button">Save</v-btn>
          </v-card-actions>
        </v-form>
      </v-container>
    </v-card>
  </v-dialog>
</template>

<script>
import { apiService } from "@/common/api.service.js";
export default {
  name: "AddRPGroup",
  props: {
    userID: {
      type: Number,
      required: false,
    },
    template: {
      type: Boolean,
      required: false,
    },
  },
  data() {
    return {
      newRPGroup: {},
      dialog: false,
      AFSLList: [],
    };
  },
  computed: {
    getAFSLLimitation () {
      if (this.newRPGroup.AFSL_limitation) {
        return this.newRPGroup.AFSL_limitation;
      } else {
        return [];
      }
    }
  },
  methods: {
    getUserID() {
      if (this.userID != null) {
        return [this.userID];
      } else {
        return [];
      }
    },
    getAFSLs() {
      if (this.userID == null) {
        let endpoint = `/api/afsls/`;
        apiService(endpoint).then(data => {
          this.AFSLList = data.results;
        });
      }
    },
    onSubmit() {
      if (this.$refs.form.validate()) {
        let endpoint = `/api/riskprofilegroups/`;
        apiService(endpoint, "POST", {
          name: this.newRPGroup.name,
          allowed_users: this.getUserID(),
          default: this.newRPGroup.default,
          AFSL_limitation: this.getAFSLLimitation,
          template: this.template,
          active_practices: [],
        }).then(data => {
          this.$emit("add-rpgroup", data);
          this.newRPGroup = null;
          this.dialog = false;
        });
      }
    }
  },
  mounted() {
    this.getAFSLs();
  }
};
</script>
