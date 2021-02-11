<template lang="html">
  <v-dialog v-model="dialog" width='600px'>
    <template v-slot:activator="{ on }">
      <v-btn icon   dark v-on="on">
        <v-icon  color="primary">mdi-plus-circle</v-icon>
      </v-btn>
    </template>
      <v-card class="small-text">
        <v-card-title class="dialog-header">
          Add Theme
          <v-spacer></v-spacer>
          <v-btn
            text
            @click="dialog = false" icon
          ><v-icon color="grey">mdi-close-circle-outline</v-icon></v-btn>
        </v-card-title>
      <v-container class="dialog-container">
        <v-form  ref="form" @submit.prevent="onSubmit">
          <v-row dense>
            <v-col>
              <v-text-field
                placeholder="Enter a name for the new theme."
                class="rounded-card" solo dense
                v-model="newTheme"
                hide-details="auto"
                :rules="themeNameRules" />
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
  name: "AddTheme",
  props: {
  },
  data() {
    return {
      newTheme: '',
      dialog: false,
    };
  },
  computed: {
    ...mapGetters(["activeUser"]),
    themeNameRules() {
      const rules = []

      const haveValue =
        v => !!(v) ||
          'You must enter a name'

      rules.push(haveValue);

      const lt50Chars =
        v => v.length <= 50 ||
          'Must be less than 50 characters'
      rules.push(lt50Chars);

      return rules;
    }
  },
  methods: {
    onSubmit() {
      // PROBABLY WANT TO ADD A LOADING ICON HERE - THE CREATE IS QUITE INTENSIVE
      if (this.$refs.form.validate()) {
        let endpoint = `/api/themes/`;
        apiService(endpoint, "POST", {
          name: this.newTheme,
          user: this.activeUser.id,
          template: true,
        }).then(data => {
          this.$emit("add-theme", data);
          this.dialog = false;
          this.$refs.form.resetValidation();
          this.newTheme = ''
        });
      }
    }
  },
};
</script>
