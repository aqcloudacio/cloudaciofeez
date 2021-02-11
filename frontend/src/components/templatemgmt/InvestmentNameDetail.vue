<template lang="html">
  <v-container >
  <v-form @submit.prevent="onSubmit">
    <v-card class="pa-2">
      <v-row>
        <v-col>
          <v-text-field
            dense solo hide-details
            v-model="investmentName.name"
            label="Name"
          />
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-btn type="submit" color="primary">
            Save
          </v-btn>
        </v-col>
      </v-row>
    </v-card>
  </v-form>
</v-container>
</template>

<script>
import { apiService } from "@/common/api.service.js";

export default {
  name: "InvestmentNameDetail",

  props: {
    investmentName: {
      type: Object,
      required: false,
    },
    template: {
      type: Boolean,
      required: false,
    },
    new: {
      type: Boolean,
      required: false,
    }
  },
  data() {
    return {
    };
  },
  methods: {
    onSubmit() {
      if (this.new == true) {
        let endpoint = `/api/investmentname/`;
        apiService(endpoint, "POST", this.investmentName).then(data => {
          this.$emit("disable-dialog", data);
        });
      } else {
        let endpoint = `/api/investmentname/${this.investmentName.id}/`;
        apiService(endpoint, "PATCH", this.investmentName).then(data => {
          this.$emit("disable-dialog", data);
        });
      }
    }
  }
};
</script>
