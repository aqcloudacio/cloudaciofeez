<template lang="html">
  <v-container >
  <v-form @submit.prevent="onSubmit">
    <v-card class="pa-2">
      <v-row>
        <v-col>
          <v-text-field
            dense solo hide-details
            v-model="AFSLObj.name"
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
  name: "AFSLNameDetail",

  props: {
    AFSLObj: {
      type: Object,
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
    // createDummy(){
    //   if (!this.platformName) {
    //     this.platformName.name = "";
    //     this.platformName.USI = "";
    //   }
    // },
    onSubmit() {
      if (this.new == true) {
        let endpoint = `/api/afsls/`;
        apiService(endpoint, "POST", this.AFSLObj).then(data => {
          this.$emit("disable-dialog", data);
        });
      } else {
        let endpoint = `/api/afsls/${this.AFSLObj.id}/`;
        apiService(endpoint, "PATCH", this.AFSLObj).then(data => {
          this.$emit("disable-dialog", data);
        });
      }
    }
  }
};
</script>
