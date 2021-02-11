<template lang="html">
  <v-dialog v-model="dialog" width='600px'>
    <template v-slot:activator="{ on }">
      <v-tooltip bottom @click.stop v-on="on">
        <template v-slot:activator="{ on }">
         <v-btn icon v-on="on">
           <v-icon
             color="primary" icon
             @click="dialog = !dialog">
             mdi-key-change
           </v-icon>
         </v-btn>
       </template>
       <span>
         Change Password
       </span>
     </v-tooltip>
    </template>
      <v-card class="small-text">
        <v-card-title class="dialog-header">
          Change Password
          <v-spacer></v-spacer>
          <v-btn
            text
            @click="dialog = false" icon
          ><v-icon color="grey">mdi-close-circle-outline</v-icon></v-btn>
        </v-card-title>
      <v-container class="dialog-container">
        <v-form ref="form" @submit.prevent="onSubmit">
          <v-text-field
            class="rounded-card mb-3" solo dense
            v-model="currentPassword"
            hide-details="auto"
            placeholder="Current password"
            :append-icon="showpw ? 'mdi-eye' : 'mdi-eye-off'"
            :type="showpw ? 'text' : 'password'"
            @click:append="showpw = !showpw"
            autocomplete="current-password"
            :error-messages="error"
          />
          <v-text-field
            class="rounded-card mb-3" solo dense
            v-model="password1"
            hide-details="auto"
            :rules="$rulePassword"
            placeholder="New password"
            :append-icon="showpw ? 'mdi-eye' : 'mdi-eye-off'"
            :type="showpw ? 'text' : 'password'"
            @click:append="showpw = !showpw"
            autocomplete="new-password"
            validate-on-blur
          />
          <v-text-field
            class="rounded-card mb-3" solo dense
            v-model="password2"
            hide-details="auto"
            :rules="repeatPassword"
            placeholder="Confirm password"
            :append-icon="showpw ? 'mdi-eye' : 'mdi-eye-off'"
            :type="showpw ? 'text' : 'password'"
            @click:append="showpw = !showpw"
            autocomplete="new-password"
            :error-messages="error2"
            validate-on-blur
          />
          <v-card-actions class="pr-0">
            <v-card-text v-if="message">{{message}}</v-card-text>
            <v-spacer />
            <v-btn  type="submit" class="primary-action-button">Change Password</v-btn>
          </v-card-actions>
        </v-form>
      </v-container>
    </v-card>
  </v-dialog>
</template>

<script>
import { mapGetters } from "vuex";
import {
  USER_CHECK_CREDENTIALS,
  USER_CHANGE_PASSWORD,
 } from "@/store/actions.type";
 import { rulePassword } from "@/components/mixins/Rules.js"

export default {
  name: "ChangePassword",
  mixins: [rulePassword],
  props: {
  },
  data() {
    return {
      dialog: false,
      currentPassword: null,
      password1: null,
      password2: null,
      showpw: false,
      error: null,
      error2: null,
      message: null,
    };
  },
  computed: {
    ...mapGetters(["activeUser"]),
    repeatPassword() {
      let ret = [this.password1 === this.password2 || 'Passwords must match.'];
      ret.push(...this.$rulePassword);
      return ret
    }
  },
  methods: {
    onSubmit() {
      this.error = null;
      // PROBABLY WANT TO ADD A LOADING ICON HERE - THE CREATE IS QUITE INTENSIVE
      if (this.$refs.form.validate()) {
        this.$store.dispatch(USER_CHECK_CREDENTIALS, {
          'email': this.activeUser.email,
          'password': this.currentPassword
        }).then(() => {
          this.changePW();
        }).catch(() => {
          this.error = "Incorrect password";
        })
      }
    },
    changePW() {
      this.$store.dispatch(USER_CHANGE_PASSWORD, {
        'id': this.activeUser.id,
        'password': this.password1,
      }).then(() => {
        this.message = "Password successfully changed."
        let timer = setTimeout(() => {
          clearTimeout(timer);
          this.message = null;
          this.dialog = false;
          //clear timer
        }, 4000)
      }).catch((err) => {
        this.error2 = err.data;
      })
    }
  },
};
</script>
