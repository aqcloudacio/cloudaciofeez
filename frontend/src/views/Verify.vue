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
          Verify Account
        </v-card-title>
        <v-text-field
          outlined
          class="mx-8 mb-3"
          v-model="token"
          hide-details="auto"
          :rules="[v => !!(v) || 'Please enter a code']"
          placeholder="Verification Code"
          validate-on-blur
          :error-messages="error ? error : null"
          @change="error = null"
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
              Continue
            </v-btn>
            <v-btn
              v-else
              @click="resendCode()"
              color="warning"
              width="100%" >
              Resend Verification Code
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

import {
  USER_VERIFY,
  USER_RESEND_VERIFICATION_TOKEN,
 } from "@/store/actions.type";

export default {
  name: "VerifyReset",
  props: {
  },
  data() {
    return {
      token: this.$route.params.token,
      user: this.$route.params.user,
      wrongCred: true,
      error: null,
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
        this.$store.dispatch(USER_VERIFY, {
          'id': this.user,
          'verify_token': this.token,
        }).then(() => {
          this.goLogin();
        }).catch(() => {
          this.error = 'Verification code is invalid';
        })
      }
    },
    resendCode() {
      this.$store.dispatch(USER_RESEND_VERIFICATION_TOKEN, {
        'id': this.user,
      })
      this.snackbar = true;
      this.snackbarText = "Verification code has been sent to your email."
      let timer = setTimeout(() => {
        clearTimeout(timer);
        this.snackbar = false;
        this.snackbarText = ""
        //clear timer
      }, 6000)
    },
    goLogin() {
      this.snackbar = true;
      this.snackbarText = "Account successfully validated. Redirecting..."
      let timer = setTimeout(() => {
        clearTimeout(timer);
        this.$router.push({ name: 'login' })
        //clear timer
      }, 3000)
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
