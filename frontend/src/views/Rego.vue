<template lang="html">
  <v-container
  fluid
    class="justify-center align-center flex d-flex">
    <v-card
      width="570px"
      min-height="770px"
      class="pa-12 pb-4">
      <template v-if="!success">
        <v-img
          src="http://127.0.0.1:8000/media/logo.PNG"
          position="center"
          width="300px"
          class="mx-auto"
          />
        <!-- <v-card-subtitle
          class="text-center">
          The King of Product Recommendations
        </v-card-subtitle> -->
        <v-card-title
          class="justify-center">
          Create an Account
        </v-card-title>
        <v-stepper
          alt-labels
          v-model="stepper">
          <v-stepper-header>
            <v-stepper-step
              step="1"
              :complete="stepper > 1"
            >
              Account
            </v-stepper-step>
            <v-divider></v-divider>
            <v-stepper-step
              step="2"
              :complete="stepper > 2"
            >
              Personal
            </v-stepper-step>
            <v-divider></v-divider>
            <v-stepper-step
              step="3"
              :complete="stepper > 3"
              >
              AFSL
            </v-stepper-step>
          </v-stepper-header>
            <v-stepper-content step="1">
              <v-form ref="form1">
                <!-- <v-card-subtitle class="text-center">
                  So you know how to log in
                </v-card-subtitle> -->
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
              </v-form>
            </v-stepper-content>

            <v-stepper-content step="2">
              <v-form ref="form2">
                <!-- <v-card-subtitle class="text-center">
                  So we know who you are
                </v-card-subtitle> -->
                <v-text-field
                  outlined
                  class="mx-8 mb-3"
                  v-model="firstName"
                  hide-details="auto"
                  :rules="$ruleRequired"
                  placeholder="First name"
                  autocomplete="first-name"
                  validate-on-blur
                />
                <v-text-field
                  outlined
                  class="mx-8 mb-3"
                  v-model="lastName"
                  hide-details="auto"
                  :rules="$ruleRequired"
                  placeholder="Surname"
                  autocomplete="last-name"
                  validate-on-blur
                />
                <v-text-field
                  outlined
                  class="mx-8 my-2"
                  v-model="phone"
                  type="number"
                  hide-details="auto"
                  :rules="$ruleMobile"
                  placeholder="Mobile phone number"
                  validate-on-blur
                >
                <template v-slot:append>
                  <v-tooltip right @click.stop>
                    <template v-slot:activator="{ on }">
                      <v-icon v-on="on">
                        mdi-information
                      </v-icon>
                    </template>
                    <span>
                      In case you ever forget your password.
                    </span>
                  </v-tooltip>
                </template>
              </v-text-field>
              <v-combobox
                outlined
                class="mx-8 my-2"
                placeholder="Practice Role"
                v-model="role"
                :items="roleList"
                ref="combobox"
                @keyup.space.prevent
                @click.stop
                hide-details="auto"
                @keyup.enter="blurComboBox()">
                <template v-slot:no-data>
                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-title>
                        Press <kbd>Enter</kbd> to create a custom role.
                      </v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </template>
              </v-combobox>
            </v-form>
          </v-stepper-content>

          <v-stepper-content step="3">
            <v-form ref="form3">
              <v-card-subtitle class="text-center">
                Entering these details allows us to link your AFSL's <br>document themes and risk profiles.
              </v-card-subtitle>
              <v-text-field
                outlined
                class="mx-8 my-2"
                hide-details="auto"
                v-model="AFSLNumber"
                placeholder="AFSL Number"
                type="number">
              </v-text-field>
              <v-text-field
                outlined
                class="mx-8 my-2"
                v-model="authRepNo"
                hint="If you are not an adviser, enter the ARN of the principal adviser"
                persistent-hint
                hide-details="auto"
                placeholder="Authorised Rep Number"
                type="number"
              >
              </v-text-field>
            </v-form>
          </v-stepper-content>
          <template v-if="stepper===4">
            <v-container class="text-wrap">
              <v-card-title>
                Welcome Aboard!
              </v-card-title>
              <v-card-text class="text-wrap">
                You have successfully created your ProductRex account.
                <br><br>
                By now, you should have received an email with instructions detailing how to activate your account.
                <br><br>
                Please check your inbox and follow the link in that email to get started.
              </v-card-text>
            </v-container>
          </template>
          <div class="text-center">
            <v-card-text v-if="error" class="red--text">{{_.capitalize(error)}}</v-card-text>
          </div>
          <v-card-actions>
            <v-btn
              v-if="4 < stepper > 1"
              @click="backStep()"
              color="secondary"
              width="50%" text>
              Back
            </v-btn>
            <v-btn
              v-if="!loading && stepper != 4"
              @click="nextStep()"
              color="primary"
              :width="stepper > 1 ? '50%' : '100%'" text
              >
              {{ submitText }}
            </v-btn>
            <template   v-if="loading">
              <v-container class="text-center" width="100%">
                <v-progress-circular
                  indeterminate
                  color="primary"
                />
                <v-btn
                  text
                  color="primary"
                >Creating Account...
                </v-btn>
              </v-container>
            </template>
          </v-card-actions>
        </v-stepper>
        <v-row justify="center">
          <v-col
            class="mx-8"
            align="center"
          >

            <v-card-text class="pb-2">
              Already have an account?        <v-btn color="primary" @click="goLogin()" text>
                        Login
                      </v-btn>
            </v-card-text>
          </v-col>
        </v-row>
      </template>
    </v-card>
  </v-container>
</template>

<script>
import { mapGetters } from "vuex";
import { ruleEmail, rulePassword, ruleRequired, ruleMobile } from "@/components/mixins/Rules.js"

import {
  USER_REGISTER,
  USER_REGISTER_DETAILS,
 } from "@/store/actions.type";

export default {
  name: "Rego",
  mixins: [ruleEmail, rulePassword, ruleRequired, ruleMobile],
  props: {
  },
  data() {
    return {
      email: null,
      phone: null,
      password1: null,
      password2: null,
      showpw: false,
      success: false,
      error: null,
      stepper: 4,
      firstName: null,
      lastName: null,
      role: null,
      roleList: [
        "Adviser",
        "Practice Manager",
        "Paraplanner",
        "Administrator",
        "Support"
      ],
      AFSLNumber: null,
      authRepNo: null,
      user: null,
      loading: false,
    };
  },
  components: {
  },
  computed: {
    ...mapGetters(["activeUser", "loggedIn"]),
    submitText() {
      if (this.stepper === 3) {
        return 'Finish';
      } else {
        return 'Continue';
      }
    },
    repeatPassword() {
      let ret = [this.password1 === this.password2 || 'Passwords must match.'];
      ret.push(...this.$rulePassword);
      return ret
    }
  },
  methods: {
    blurComboBox() {
      this.$refs.combobox.blur();
    },
    backStep() {
      this.stepper -= 1;
    },
    nextStep() {
      const form = 'form'+this.stepper;
      if (this.$refs[form].validate()) {
        if (this.stepper === 1) {
          this.createAccount();
        } else if (this.stepper === 3){
          this.updateAccount();
        } else {
          this.stepper += 1;
        }
      }
    },
    createAccount() {
      this.loading = !this.loading;
      this.$store.dispatch(USER_REGISTER, {
        'email': this.email,
        'password': this.password1,
      }).then(data => {
        this.user = data;
        this.stepper += 1;
        this.loading = !this.loading;
      }).catch(err => {
        this.error = this.handleErr(err);
        this.loading = !this.loading;
      })
    },
    updateAccount() {
      this.$store.dispatch(USER_REGISTER_DETAILS, {
        'id': this.user.user_id,
        'first_name': this.firstName,
        'last_name': this.lastName,
        'phone': this.phone,
        'role': this.role,
        'linked_ARN': this.authRepNo,
        'AFSL': {
          'AFSL_number': this.AFSLNumber
        },
      }).then(() => {
        this.success = true;
        this.stepper += 1;
      }).catch(err => {
        this.error = this.handleErr(err);
      })
    },
    handleErr(err) {
      if (err.data.email) {
        return err.data.email[0];
      } else {
        return err.data.detail;
      }
    },
    goLogin() {
      this.$router.push({ name: 'login' })
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
