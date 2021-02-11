<template lang="html">
  <v-container >
  <v-form @submit.prevent="onSubmit">
    <v-card class="pa-2">
      <v-row>
        <v-col>
          <v-text-field
            dense solo hide-details
            v-model="platformName.name"
            label="Name"
          />
        </v-col>
        <v-col>
          <v-text-field
            dense solo hide-details
            v-model="platformName.USI"
            label="USI"
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
  name: "PlatformNameDetail",

  props: {
    platformName: {
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
        let endpoint = `/api/platformnames/`;
        apiService(endpoint, "POST", this.platformName).then(data => {
          this.$emit("disable-dialog", data);
        });
      } else {
        let endpoint = `/api/platformnames/${this.platformName.id}/`;
        apiService(endpoint, "PATCH", this.platformName).then(data => {
          this.$emit("disable-dialog", data);
        });
      }
    }
  }
};
</script>
