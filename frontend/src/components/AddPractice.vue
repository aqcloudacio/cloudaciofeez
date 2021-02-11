<template lang="html">
  <v-dialog v-model="dialog" width='600px'>
    <template v-slot:activator="{ on }">
      <v-btn icon  dark v-on="on" class="pr-0">
      <v-icon color="primary" class="pr-0">mdi-plus-circle</v-icon></v-btn>
    </template>
    <v-card class="small-text">
      <v-card-title class="dialog-header">
        Add Practice
        <v-spacer></v-spacer>
        <v-btn
          text
          @click="dialog = false" icon
        ><v-icon color="grey">mdi-close-circle-outline</v-icon></v-btn>
      </v-card-title>
      <v-container class="dialog-container">
        <v-form
          @submit.prevent="onSubmit"
          v-if="newPractice != null"
          ref="form">
          <v-row dense>
            <v-col>
              <v-text-field
                placeholder="Enter a name for the new practice."
                class="rounded-card" solo dense
                v-model="newPractice.name"
                :rules="[v => !!(v) || 'You must enter a name']"
                hide-details="auto"
              />
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
  name: "AddPractice",
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
      newPractice: {},
      dialog: false,
    };
  },
  methods: {
    getUserID() {
      if (this.userID != null) {
        return [this.userID];
      } else {
        return [];
      }
    },
    onSubmit() {
      if (this.$refs.form.validate()) {
        let endpoint = `/api/practices/`;
        apiService(endpoint, "POST", {
          name: this.newPractice.name,
          staff_id: this.getUserID(),
          admins_id: this.getUserID(),
          pending_staff_id: [],
        }).then(data => {
          this.$emit("add-practice", data);
          this.newPractice = null;
          this.dialog = false;
        });
      }
    }
  },
  // mounted() {
  //   this.getAFSLs();
  // }
};
</script>
