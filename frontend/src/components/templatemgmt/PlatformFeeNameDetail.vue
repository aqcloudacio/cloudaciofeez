<template lang="html">
  <v-container >
  <v-form @submit.prevent="onSubmit">
    <v-card class="pa-2">
      <v-row>
        <v-col>
          <v-text-field
            dense solo hide-details
            v-model="feeName"
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
  name: "PlatformFeeNameDetail",

  props: {
    platform: {
      type: Number,
      required: true,
    },
    template: {
      type: Boolean,
      required: false,
    },
  },
  data() {
    return {
      feeName: "",
    };
  },
  methods: {
    onSubmit() {
      let endpoint = `/api/platformtemplates/${this.platform}/fees/`;
      apiService(endpoint, "POST", {
        description: this.feeName,
        platform: this.platform,
      }).then(data => {
        this.$emit("disable-dialog", data);
      });
    }
  },
};

</script>
