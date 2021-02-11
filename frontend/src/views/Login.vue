<template lang="html">
  <v-container
  fluid
    class="justify-center align-center flex d-flex">
    <v-card
      min-width="500px"
      min-height="600px"
      class="pa-12 pb-4">
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
        <!-- Login wtih Google. -->
         <!-- Not right now -->
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
        <v-text-field
          outlined
          class="mx-8 mb-3"
          v-model="password"
          hide-details="auto"
          :rules="[v => !!(v) || 'Please enter a password']"
          placeholder="Password"
          :append-icon="showpw ? 'mdi-eye' : 'mdi-eye-off'"
          :type="showpw ? 'text' : 'password'"
          @click:append="showpw = !showpw"
          autocomplete="current-password"
          validate-on-blur
          :error-messages="error"

          />
        <v-row justify="center">
          <v-col
          class="mx-8"
            align="center"
          >
            <v-btn @click="onSubmit()" color="primary"  width="100%" >
              Continue
            </v-btn>
            <br><br>
            <v-btn @click="goForgotPW()" text x-small>
              Forgot password?
            </v-btn><br><br>
            <v-card-text>
              Don't have an account?
            </v-card-text>
            <v-btn color="primary" @click="goRego()" text>
              Create Account
            </v-btn>
          </v-col>
        </v-row>
      </v-form>
    </v-card>
  </v-container>
</template>

<script>
import { mapGetters } from "vuex";
import { ruleEmail } from "@/components/mixins/Rules.js"

import {
  USER_LOGIN,
 } from "@/store/actions.type";

export default {
  name: "Login",
  mixins: [ruleEmail],
  props: {
  },
  data() {
    return {
      email: null,
      password: null,
      showpw: false,
      wrongCred: false,
      error: null,
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
        this.$store.dispatch(USER_LOGIN, {
          'email': this.email,
          'password': this.password
        }).then(() => {
          this.wrongCred = false;
        }).catch(err => {
          this.error = err.data.detail;
          this.wrongCred = true;
        })
      }
    },
    goRego() {
      this.$router.push({ name: 'rego' })
    },
    goForgotPW() {
      this.$router.push({ name: 'resetPassword' })
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
