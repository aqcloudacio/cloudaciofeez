<template lang="html">
  <v-dialog v-model="dialog" max-width="600px">
    <template v-slot:activator="{ on }">
      <v-btn color="primary" icon dark v-on="on">
        <v-icon color="primary">mdi-plus-circle</v-icon>
      </v-btn>
    </template>
    <v-card class="small-text">
      <v-card-title class="dialog-header">
        Add Model Portfolio
        <v-spacer></v-spacer>
        <v-btn
          text
          @click="dialog = false" icon
        ><v-icon color="grey">mdi-close-circle-outline</v-icon></v-btn>
      </v-card-title>
      <v-container class="dialog-container">
        <v-form ref="form" @submit.prevent="onSubmit">
          <v-row dense>
            <v-col>
              <v-text-field
                placeholder="Enter a name for the new model portfolio"
                hide-details="auto"
                :rules="[v => !!(v) || 'You must enter a name']"
                class="rounded-card" solo dense
                v-model="newPortfolio" />
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
import { mapGetters } from "vuex";

export default {
  name: "AddPortfolioName",
  data() {
    return {
      newPortfolio: "",
      dialog: false,
    };
  },
  props: {
  },
  compuited: {
    ...mapGetters(["activeUser"]),
  },
  methods: {
    getUserID() {
      if (this.activeUser.id != null) {
        return [this.activeUser.id];
      } else {
        return [];
      }
    },
    onSubmit() {
      if (this.$refs.form.validate()) {
        let endpoint = `/api/portfoliotemplates/`;
        apiService(endpoint, "POST", {
          name: this.newPortfolio,
          auto_created: false,
          template: true,
          allowed_users: this.getUserID(),
          practices: [],
        }).then(data => {
          this.$emit("add-portfolio", data);
          this.newPortfolio = null;
          this.dialog = false;
        });
        if (this.error) {
          this.error = null;
        }
      } else {
        this.error = "You must enter a name for the new portfolio.";
      }
    }
  },
};
</script>
