<template lang="html">
  <v-container
    fluid
    class="justify-center align-center flex d-flex">
    <v-card
      min-width="500px"
      min-height="600px"
      class="pa-12">
      <v-form submit.prevent="onSubmit" ref="form">
        <v-img
          src="http://127.0.0.1:8000/media/logo.PNG"
          position="center"
          width="300px"
          class="mx-auto"
          />
        <v-card-subtitle
          class="text-center">
          The King of Product Recommendations
        </v-card-subtitle>
        <v-card-title
          class="justify-center">
          Reset Password
        </v-card-title>
        <v-text-field
          outlined
          class="mx-8 my-2"
          v-model="email"
          hide-details="auto"
          :rules="$ruleEmail"
          placeholder="Email address"
          validate-on-blur
          autocomplete="email"
        />
        <v-row justify="center">
          <v-col
          class="mx-8"
            align="center"
          >
            <v-btn
              v-if="!error"
              @click="onSubmit()"
              color="primary"
              width="100%" >
              Reset
            </v-btn>
          </v-col>
        </v-row>
      </v-form>
    </v-card>
    <v-snackbar
      v-model="snackbar"
      >
      {{snackbarText}}
    </v-snackbar>
  </v-container>
</template>

<script>
import { mapGetters } from "vuex";
import { ruleEmail } from "@/components/mixins/Rules.js"

import {
  USER_RESET_PASSWORD,
 } from "@/store/actions.type";

export default {
  name: "ResetPassword",
  mixins: [ruleEmail],
  props: {
  },
  data() {
    return {
      wrongCred: true,
      error: null,
      email: null,
      snackbar: false,
      snackbarText: '',
    };
  },
  components: {
  },
  computed: {
    ...mapGetters(["activeUser", "loggedIn"]),
  },
  methods: {
    onSubmit() {
      if (this.$refs.form.validate()) {
        this.error = null;
        this.snackbar = true;
        this.snackbarText = `An email has been sent to ${this.email} with further instructions.`
        this.$store.dispatch(USER_RESET_PASSWORD, {
          'email': this.email,
        }).then(() => {
          let timer = setTimeout(() => {
            clearTimeout(timer);
            this.snackbar = false;
            this.snackbarText = ""
            //clear timer
          }, 8000)
        }).catch(() => {
          let timer = setTimeout(() => {
            clearTimeout(timer);
            this.snackbar = false;
            this.snackbarText = ""
            //clear timer
          }, 8000)
        })
      };
    },
    checkLoggedIn() {
      if (this.loggedIn) {
        this.$router.push({ name: 'home' })
      }
    },
  },
  mounted() {
    this.checkLoggedIn();
  },
};
</script>

<style lang="css" scoped>
</style>
