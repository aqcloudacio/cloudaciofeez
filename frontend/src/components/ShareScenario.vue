<template lang="html">
  <div>
    <v-menu offset-y>
      <template v-slot:activator="{ on }">
        <v-btn icon v-on="on">
          <v-icon :color="color ? color : 'grey'">
            mdi-share
          </v-icon>
        </v-btn>
      </template>
      <v-list>
        <v-list-item
          @click='shareWithPractice'
          v-if="!scenario.practice && this.activeUser.active_practice"
        >
          <v-list-item-title>Share with {{this.activeUser.active_practice_name}}</v-list-item-title>
        </v-list-item>
        <v-list-item
          @click='dialog=true'
        >
          <v-list-item-title>Share Client</v-list-item-title>
        </v-list-item>
        <v-list-item
          @click='dialog=true'
          v-if="!_.isEmpty(scenario.allowed_users)"
        >
          <v-list-item-title>Sharing Settings</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
    <v-dialog
      max-width="500px"
      v-model="dialog">
      <v-card class="small-text">
        <v-card-title class="dialog-header">
          Sharing Settings
          <v-spacer></v-spacer>
          <v-btn
            text
            @click="dialog = false" icon
            ><v-icon color="grey">mdi-close-circle-outline</v-icon></v-btn>
        </v-card-title>

        <v-container class="dialog-container">
          <v-form
            ref="form">
            <v-text-field
              class='rounded-card'
              :placeholder="`Enter email address to share ${scenario.client} with`"
              v-model="newShareEmail"
              dense solo
              :error-messages="error ? error : null"
              :rules="$ruleEmail"
              hide-details="auto"
              :validate-on-blur="true"
              @click="error = null"
            ></v-text-field>
            <v-card-actions class='px-0 py-4'>
              <v-spacer />
              <v-btn class="primary-action-button"
              @click="addAllowedUser()">
                Share
              </v-btn>
            </v-card-actions>
            <template v-if="!_.isEmpty(scenario.allowed_users)">
              <v-divider  />
              <v-card-subtitle class="px-0">
                Shared Users
              </v-card-subtitle>
              <v-card-text class="d-flex flex px-0 py-1"   v-for="allowed_user in scenario.allowed_users"
                :key="allowed_user.id">
                {{ allowed_user.name ? allowed_user.name : allowed_user.email }}
                <v-spacer />
                <v-card-actions class="pa-0">
                  <v-tooltip right>
                    <template v-slot:activator="{ on }">
                      <v-btn icon small v-on="on">
                        <v-icon
                          :color="'danger'"
                          @click="removeAllowedUser(allowed_user)">
                          mdi-account-remove-outline
                        </v-icon>
                      </v-btn>
                    </template>
                    <span>Unshare</span>
                  </v-tooltip>
                </v-card-actions>
              </v-card-text>
            </template>
          </v-form>
        </v-container>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { apiService } from "@/common/api.service.js";
import { ruleEmail } from "@/components/mixins/Rules.js"
import { mapGetters } from "vuex";

export default {
  name: "ShareScenario",
  mixins: [ruleEmail],
  props: {
    scenario: {
      type: Object,
      required: true,
    },
    color: {
      type: String,
      required: false,
    }
  },
  data() {
    return {
      error: null,
      dialog: false,
      newShareEmail: null,
    };
  },
  computed: {
    ...mapGetters(["activeUser"]),
  },
  methods: {
    shareWithPractice() {
      let endpoint = `/api/scenarios/${this.scenario.id}/`;
      apiService(endpoint, "PATCH", {
        practice: this.activeUser.active_practice
        }).then(data => {
          this.$emit('update-scenarios', data);
          this.scenario.practice = data.practice
      });
    },
    addAllowedUser() {
      if (this.$refs.form.validate()) {
        let newAllowedUser = new Object();
        newAllowedUser.email = this.newShareEmail;
        this.scenario.allowed_users.push(newAllowedUser);
        let endpoint = `/api/scenarios/${this.scenario.id}/`;
        apiService(endpoint, "PATCH", {
          allowed_users: this.scenario.allowed_users
          }).then(data => {
            this.scenario.allowed_users = data.allowed_users;
          }).catch(error => {
            this.scenario.allowed_users.pop()
            this.error = error.data.message;
          })
        }
    },
    removeAllowedUser(allowed_user) {
      let newAllowedUsers = this.scenario.allowed_users.filter(function(el) { return el.id != allowed_user.id; }); ;
      let endpoint = `/api/scenarios/${this.scenario.id}/`;
      apiService(endpoint, "PATCH", {
        allowed_users: newAllowedUsers
        }).then(data => {
          this.$emit('update-scenarios', data);
          this.scenario.allowed_users = data.allowed_users;
      });
    },
  }
};
</script>
