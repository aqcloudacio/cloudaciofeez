<template lang="html">
  <v-container
  fluid
    class="justify-center align-center flex d-flex">
    <v-card
      v-if="!verified"
      min-width="500px"
      min-height="600px"
      class="pa-12">
      <v-form submit.prevent="onSubmit" ref="verifyForm">
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
          Verify Password Reset
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
    <v-card
      v-if="verified"
      min-width="500px"
      min-height="600px"
      class="pa-12">
      <v-form submit.prevent="changePassword" ref="changeForm">
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
          Enter New password
        </v-card-title>
        <v-text-field
          outlined
          class="mx-8 mb-3"
          v-model="password1"
          hide-details="auto"
          :rules="$rulePassword"
          placeholder="Password"
          :append-icon="showpw ? 'mdi-eye' : 'mdi-eye-off'"
          :type="showpw ? 'text' : 'password'"
          @click:append="showpw = !showpw"
          autocomplete="new-password"
          validate-on-blur
        />
        <v-text-field
          outlined
          class="mx-8 mb-3"
          v-model="password2"
          hide-details="auto"
          :rules="repeatPassword"
          placeholder="Confirm password"
          :append-icon="showpw ? 'mdi-eye' : 'mdi-eye-off'"
          :type="showpw ? 'text' : 'password'"
          @click:append="showpw = !showpw"
          autocomplete="new-password"
          validate-on-blur
        />
        <v-row justify="center">
          <v-col
          class="mx-8"
            align="center"
          >
            <v-btn
              @click="changePassword()"
              color="primary"
              width="100%" >
              Set Password
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
import { rulePassword } from "@/components/mixins/Rules.js"

import {
  USER_VERIFY,
  USER_RESEND_VERIFICATION_TOKEN,
  USER_CHANGE_PASSWORD,
 } from "@/store/actions.type";

export default {
  name: "Verify",
  mixins: [rulePassword],
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
      verified: false,
      password1: null,
      password2: null,
      showpw: false,
      userObj: null
    };
  },
  components: {
  },
  computed: {
    ...mapGetters(["activeUser", "loggedIn"]),
    repeatPassword() {
      let ret = [this.password1 === this.password2 || 'Passwords must match.'];
      ret.push(...this.$rulePassword);
      return ret
    }
  },
  methods: {
    onSubmit() {
      if (this.$refs.verifyForm.validate()) {
        this.error = null;
        this.$store.dispatch(USER_VERIFY, {
          'id': this.user,
          'verify_token': this.token,
        }).then(() => {
          this.verified = true;
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
    changePassword() {
      if (this.$refs.changeForm.validate()) {
        this.$store.dispatch(USER_CHANGE_PASSWORD, {
          'id': this.user,
          'password': this.password1,
        }).then(() => {
          this.snackbar = true;
          this.snackbarText = "Password changed. Please login with your new password. Redirecting..."
          let timer = setTimeout(() => {
            clearTimeout(timer);
            this.$router.push({ name: 'login' })
            //clear timer
          }, 4000)
        }).catch((err) => {
          console.log(err);
        })
      }
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
