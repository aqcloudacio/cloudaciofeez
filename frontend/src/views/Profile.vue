<template>
  <v-container class="fullwidthrow pa-0" style="background: #e4e7f0; height:100%" v-if="user">
    <v-container style="width:1012px" class="pb-0">
    <v-card class="pa-8 mt-8 rounded-card">
      <v-form ref="form">
        <v-row dense>
          <v-col dense >
            <v-card-text v-if="!editUser" class="pa-0">
              <span v-if="user.name" class="display-1 font-weight-bold">
                {{user.name}} <br>
              </span>
                <v-icon small>mdi-email-outline</v-icon> {{user.email}} <br>
              <span v-if="user.role">
                <v-icon small>mdi-briefcase-outline</v-icon> {{user.role}} <br>
              </span>
            </v-card-text>
            <v-text-field
              label="Name"
              placeholder="Enter your name"
              class=" px-4 py-2 "
              hide-details="auto"
              v-if="editUser"
              :value="user.name"
              @change="setUserName($event)">
            </v-text-field>
            <v-text-field
              label="Email"
              class="  px-4 py-2"
              hide-details="auto"
              v-if="editUser"
              v-model="user.email"
              :rules="$ruleEmail"
              validate-on-blur>
            </v-text-field>
            <v-combobox
              label="Role"
              placeholder="Enter your role"
              class="  px-4 p2"
              v-if="editUser"
              v-model="user.role"
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
          </v-col>
          <v-divider  vertical/>
          <v-col class="align-self-center">
            <v-container class="pa-0 d-flex">
              <v-card-text class="pa-0"
                v-if="!editUser && !profileHasAFSL"
                >
                No AFSL has been set.
              </v-card-text>
              <v-card-text class="py-0" v-else-if="!editUser && profileHasAFSL">
                <span v-if="user.AFSL_approved">
                  AFSL: {{user.AFSL.name}} <br>
                </span>
                <span v-else>
                  AFSL Linking Pending Approval <br>
                </span>
                <span v-if="user.AFSL">
                  AFSL Number: {{user.AFSL.AFSL_number}} <br>
                </span>
                <span v-if="user.linked_ARN">
                  Linked ARN: {{user.linked_ARN}} <br>
                </span>
              </v-card-text>
             <template v-else>
               <v-container class="pa-0 ma-0">
                 <v-text-field
                   class="px-4 pb-2 mt-0"
                   hide-details="auto"
                   v-if="editUser"
                   :value="profileHasAFSL ? user.AFSL.AFSL_number : null"
                   @change="user.AFSL ? user.AFSL.AFSL_number = $event : setUserAFSL($event)"
                   label="AFSL Number"
                   placeholder="Enter AFSL Number"
                   type="number">
                 </v-text-field>
                 <v-text-field
                   class=" px-4 py-2"
                   v-if="editUser"
                   :value="user.linked_ARN"
                   @change="$event ? user.linked_ARN = $event : user.linked_ARN = null"
                   hint="If you are not an adviser, enter the ARN of the principal adviser"
                   persistent-hint
                   required
                   hide-details="auto"
                   label="Authored Rep Number"
                   placeholder="Enter an Authorised Rep Number"
                   type="number"
                   :error="!!(error)"
                   :error-messages="error">
                 </v-text-field>
               </v-container>
             </template>
             <v-spacer />
              <v-card-actions class="d-block pa-0 ma-0" >
                <v-tooltip bottom @click.stop>
                  <template v-slot:activator="{ on }">
                   <v-btn icon v-on="on">
                     <v-icon
                       v-if="!editUser"
                       color="green" icon
                       @click="editUser = !editUser">
                       mdi-pencil-circle
                     </v-icon>
                     <v-icon
                       v-else
                       color="green" icon
                       @click="updateUser()">
                       mdi-check-circle
                     </v-icon>
                   </v-btn>
                 </template>
                 <span>
                   Edit Personal Details
                 </span>
               </v-tooltip>
               <ChangePassword />
             </v-card-actions>
           </v-container>
          </v-col>
        </v-row>
      </v-form>

    <v-row class="mt-6" >
      <v-col :cols="3">
        <v-card
          height="100%"
          :class="user.active_theme_name ? 'grey1 text-center pa-3 half-rounded-card' : 'grey1 d-flex justify-center  half-rounded-card'"
          @click="active='themes'">
          <v-card-title class="justify-center">
            Theme
          </v-card-title>
          <v-chip
            v-if="user.active_theme_name"
            class="mb-3 rounded-card" small label
            color="primary"
            >
            <span class="wrapclass">
              {{user.active_theme_name}}
            </span>
          </v-chip>
        </v-card>
      </v-col>
      <v-col :cols="3">
        <v-card
          height="100%"
          :class="user.active_practice_name ?  'grey1 text-center pa-3 half-rounded-card' : 'grey1 d-flex justify-center  half-rounded-card'"
          @click="active='practices'">
          <v-card-title class="justify-center">
            Practice
          </v-card-title>
          <v-chip
            v-if="user.active_practice_name"
            class="mb-3 rounded-card" small label
            color="primary"
            >
            <span class="wrapclass">
              {{user.active_practice_name}}
            </span>
          </v-chip>
        </v-card>
      </v-col>
      <v-col :cols="3">
        <v-card
          height="100%"
          :class="activeRPName ?  'grey1 text-center pa-3 half-rounded-card' : 'grey1 d-flex justify-center  half-rounded-card'"
          @click="active='riskProfile'">
          <v-card-title class="justify-center">
            Risk Profiles
          </v-card-title>
          <v-chip
            v-if="activeRPName"
            class="mb-3 rounded-card" small label
            color="primary">
            <span class="wrapclass">
              {{activeRPName}}
            </span>
          </v-chip>
        </v-card>
      </v-col>
      <v-col :cols="3">
        <v-card
          height="100%"
          class="grey1 d-flex justify-center  half-rounded-card"
          @click="active='portfolio'">
          <v-card-title>
            Model Portfolios
          </v-card-title>
        </v-card>
      </v-col>
    </v-row>
      <v-container class="pa-0">
        <ThemeTable
          v-if="active == 'themes'"
          />
        <PortfolioTable
          v-if="active == 'portfolio'"
          />
        <PracticeTable
          v-if="active == 'practices'"
          :riskProfileGroups="riskProfileGroups"
          />
        <RiskProfileTable
          v-if="active == 'riskProfile'"
          :riskProfileGroups="riskProfileGroups"
          @add-rpgroup="addRPGroup($event)"
          @update-rpgroup="updateRPGroup($event)"
          @delete-rpgroup="removeRPGroup($event)"
         />
      </v-container>
  </v-card>

  </v-container>

  </v-container>
</template>

<script>
import { apiService } from "@/common/api.service";
import RiskProfileTable from "@/components/RiskProfileTable.vue";
import ThemeTable from "@/components/ThemeTable.vue";
import PortfolioTable from "@/components/PortfolioTable.vue";
import PracticeTable from "@/components/PracticeTable.vue";
import ChangePassword from "@/components/ChangePassword.vue";

import { ruleEmail } from "@/components/mixins/Rules.js"

import { mapGetters } from "vuex";
import {
  SET_ACTIVE_USER
} from "@/store/mutations.type";
import {
  USER_UPDATE
} from "@/store/actions.type";

export default {
  name: "profile",
  mixins: [ruleEmail],
  props: {
    shortcut: {
      type: String,
      required: false
    },
  },
  data() {
    return {
      user: null,
      riskProfileGroups: null,
      active: 'themes',
      editUser: false,
      roleList: [
        "Adviser",
        "Practice Manager",
        "Paraplanner",
        "Administrator",
        "Support"
      ],
      dialog: false,
    };
  },
  components: {
    RiskProfileTable,
    PortfolioTable,
    PracticeTable,
    ThemeTable,
    ChangePassword,
  },
  computed: {
    ...mapGetters(["activeUser"]),
    profileHasAFSL() {
      return this.user.AFSL
    },
    practices() {
      if (this.user.practice_names) {
        return this.user.practice_names
      } else {
        return null
      }
    },
    activeRPName() {
      if (this.riskProfileGroups && this.user) {
        const result = this.riskProfileGroups.find(
            x => x.id === this.user.active_rp)
            if (result) {
              //for some reason splicing the array causes this to temporarily
              // not find the riskProfileGroup array. This If statement avoids
              // a warning message.
              return result.name
            } else {
              return null
            }
      } else {
        return null
      }
    },
    error() {
      if (this.user.AFSL) {
        if (this.user.AFSL.AFSL_number && !this.user.linked_ARN) {
          return "You must link an ARN"
        } else {
          return null
        }
      } else {
        return null
      }
    }
  },
  watch: {
    activeUser() {
      this.setUser();
    }
  },
  methods: {
    setUserName(value){
      let first_name = value.substr(0,value.indexOf(' '));
      let last_name = value.substr(value.indexOf(' ')+1);
      this.user.name = value;
      this.user.first_name = first_name;
      this.user.last_name = last_name;
    },
    blurComboBox() {
      // Blurs the combobox when users creates custom role.
      this.$refs.combobox.blur();
      // this.$nextTick(() => {
      //   this.profileRole();
      // })
    },
    setUser() {
      this.user = this.activeUser
    },
    setUserAFSL($event) {
      this.user.AFSL = new Object();
      this.user.AFSL.AFSL_number = $event;
    },
    updateUser() {
      if (this.$refs.form.validate() && !this.error) {
        this.$store.commit(SET_ACTIVE_USER, this.user);
        this.editUser = !this.editUser;
        this.$store.dispatch(USER_UPDATE);
      }
    },
    addRPGroup() {
      this.getRPGroups();
    },
    removeRPGroup(data) {
      const i = this.riskProfileGroups.findIndex(item => item.id === data.id);
      this.$delete(this.riskProfileGroups, i);
    },
    updateRPGroup(data) {
      const i = this.riskProfileGroups.findIndex(item => item.id === data.id);
      this.riskProfileGroups.splice(i,0,data);
    },
    getRPGroups() {
      let endpoint = `/api/riskprofilegroups/`;
      apiService(endpoint).then(data => {
        this.riskProfileGroups = data.results;
      });
    },
    checkShortcut() {
      if (this.shortcut) {
        this.active = this.shortcut;
      }
    }
  },
  mounted() {
    this.getRPGroups();
    this.checkShortcut();
    this.setUser();
  }
};
</script>
<style media="screen">
.smallFont {
  font-size: 0.9em;
}
.smallFont label {
  font-size: 1em;
}
.wrapclass {
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
