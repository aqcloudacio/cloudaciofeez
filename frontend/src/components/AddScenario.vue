<template lang="html">
  <v-container class="fullwidthrow pa-0" style="background: #e4e7f0">
    <v-container style="width:500px" >
      <v-card-title class="justify-center pb-0"
      style="font-size: 18pt">WELCOME</v-card-title>
      <v-form
        v-model="valid"
        class="pa-4"
        ref="form">
        <v-row
          justify="center"
         >
          <v-col
            align="center"
            >

            <v-text-field
              solo rounded
              v-model="newScenario"
              label="Enter the client's name"
              hide-details="auto"
              :rules="[v => !!v || 'You must enter a client name']"
              validate-on-blur
              text-align="center"/>
              <br>
            <v-select
              solo rounded
              v-model="riskProfile"
              :items="riskProfiles"
              label="Select a risk profile"
              :rules="[v => !!v || 'You must enter a risk profile']"
              hide-details="auto"
              validate-on-blur
              item-value="id"
              item-text="name"/>
            <v-checkbox
              class="checkbox-small-label pl-4 pt-0"
              v-if="activeUser.active_practice"
              v-model="shareWithPractice"
              :label="`Share with ${activeUser.active_practice_name}`"
              hide-details dense
            />
            <v-btn
              class="mt-4"
              type="submit"
              color="primary"
              rounded
              width="100%"
              @click.prevent="onSubmit"
              dense large dark>
              Begin
            </v-btn>
          </v-col>
        </v-row>
      </v-form>
    </v-container>
  </v-container>
</template>

<script>
import { apiService } from "@/common/api.service";
import { mapGetters } from "vuex";

export default {
  name: "AddScenario",
  data() {
    return {
      valid: false,
      newScenario: null,
      riskProfile: null,
      shareWithPractice: true,
      error: null,
    };
  },
  props: {
    riskProfiles: {
      type: Array,
      required: true,
    }
  },
  computed: {
    ...mapGetters(["activeUser"]),
    scenarioPractice() {
      if (this.shareWithPractice) {
        return this.activeUser.active_practice
      } else {
        return null
      }
    }
  },
  methods: {
    onSubmit() {
      // Validates the form before POST to API.
      if (this.$refs.form.validate()) {
        let endpoint = `/api/scenarios/`;
        apiService(endpoint, "POST", {
          client: this.newScenario,
          risk_profile_id: this.riskProfile,
          user: this.activeUser.id,
          practice: this.scenarioPractice,
          theme: this.activeUser.active_theme
        }).then(data => {
          this.$emit("add-scenario", data);
          this.newScenario = null;
          this.riskProfile = null;
        });
      }
    }
  }
};
</script>

<style scoped>
  .fullwidthrow {
    width: 100vw;
    max-width:3000px;
    margin-left: calc(-50vw + 50%);
  }
</style>
