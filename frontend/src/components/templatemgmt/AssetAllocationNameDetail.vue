<template lang="html">
  <v-container >
  <v-form @submit.prevent="onSubmit">
    <v-card class="pa-2">
      <v-row>
        <v-col>
          <v-text-field
            dense solo hide-details
            v-model="AAName.name"
            label="Name"
          />
        </v-col>
        <v-col>
          <v-select
            dense solo hide-details
            v-model="AAName.rp_aaname_link"
            :items="RPList"
            item-value="id"
            item-text="name"
            :multiple="true"
            label="Link to Risk Profile AA"
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
  name: "AssetAllocationNameDetail",

  props: {
    AAName: {
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
      RPList: [],
    };
  },
  methods: {
    createDummy(){
      if (!this.AAName) {
        this.AAName.name = "";
      }
    },
    getRPList() {
      let endpoint = `/api/riskprofiledefaultnametemplates/`;
      apiService(endpoint, "GET").then(data => {
        this.RPList = data.results;
      });
    },
    onSubmit() {
      if (this.new == true) {
        let endpoint = `/api/aaname/`;
        apiService(endpoint, "POST", this.AAName).then(data => {
          this.$emit("disable-dialog", data);
        });
      } else {
        let endpoint = `/api/aaname/${this.AAName.id}/`;
        apiService(endpoint, "PATCH", this.AAName).then(data => {
          this.$emit("disable-dialog", data);
        });
      }
    }
  },
  mounted() {
    this.getRPList();
  }
};

</script>
