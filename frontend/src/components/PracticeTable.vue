<template lang="html">
  <v-container class="pa-0 small-text">
    <v-form  @submit.prevent="onSubmit">
      <v-row align="center">
        <v-col
        :cols="6">
          <v-select
            class="rounded-card"
            v-if="!editPracticeName"
            :items="practices"
            item-text="name"
            return-object
            v-model="selectedPractice"
            label="Practice Name"
            placeholder="Select a Practice"
            outlined dense hide-details="auto">
            <template v-slot:append-outer v-if="isAdmin">
              <v-icon
                v-if="!editPracticeName"
                color="primary" icon
                @click="editPracticeName = !editPracticeName">mdi-pencil-circle</v-icon>
            </template>
          </v-select>
          <v-text-field
            v-else
            label="Practice Name"
            :value="selectedPractice.name"
            @change="newPracticeName = $event"
            dense outlined
            hide-details>
            <template v-slot:append-outer v-if="isAdmin">
              <v-icon
                v-if="editPracticeName"
                color="primary" icon
                @click="updatePracticeName()">mdi-check-circle</v-icon>
            </template>
          </v-text-field>
        </v-col>
        <v-col>
          <v-container class="pa-0 d-flex">

          <v-switch inset dense
            v-if="!_.isEmpty(selectedPractice)"
            v-model="activeSwitch"
            label="Active Practice"/>
          <v-spacer />
          <v-card-actions class="pr-0">
          <AddPractice
            v-if="!_.isEmpty(activeUser)"
            :userID="activeUser.id"
            @add-practice="addPractice($event)"/>
          </v-card-actions>
        </v-container>
      </v-col>
      </v-row>
      <v-divider class="mt-1 mb-4" v-if="!_.isEmpty(selectedPractice)"/>
      <v-row v-if="!_.isEmpty(selectedPractice)">
        <v-col
          :cols="6">
          <v-select
            style="align-items: start"
            height="140"
            class="half-rounded-card "
            ref="modelPortfolios"
            :readonly="!editModelPortfolios"
            :items="portfolios"
            item-text="name"
            item-value="id"
            :value="selectedPractice.model_portfolios"
            @change="newModelPortfolios = $event"
            label="Model Portfolios"
            outlined dense hide-details multiple chips>
            <template v-slot:append-outer v-if="isAdmin">
              <v-icon
                v-if="!editModelPortfolios"
                color="primary" icon
                @click="editModelPortfolios = !editModelPortfolios">
                  mdi-pencil-circle
              </v-icon>
              <v-icon
                v-else
                color="primary" icon
                @click="updateModelPortfolios()">
                mdi-check-circle
              </v-icon>
            </template>
          </v-select>
        </v-col>
        <v-col
        :cols="6">
          <v-row dense>
            <v-col>
              <v-select
                class="rounded-card "
                :readonly="!editAFSL"
                :items="AFSLArray"
                item-text="name"
                item-value="id"
                :value="selectedPractice.AFSL"
                @change="newAFSL = $event"
                label="AFSL"
                outlined dense hide-details clearable>
                <template v-slot:append-outer v-if="isAdmin">
                  <v-icon
                    v-if="!editAFSL"
                    color="primary" icon
                    @click="editAFSL = !editAFSL">
                      mdi-pencil-circle
                  </v-icon>
                  <v-icon
                    v-else
                    color="primary" icon
                    @click="updateAFSL()">
                      mdi-check-circle
                  </v-icon>
                </template>
              </v-select>
            </v-col>
          </v-row>
          <v-row dense>
            <v-col>
              <v-select
                class="rounded-card"
                :readonly="!editRiskProfileGroup"
                :items="riskProfileGroups"
                item-text="name"
                item-value="id"
                :value="selectedPractice.risk_profile_group"
                @change="newRiskProfileGroup = $event"
                label="Risk Profile Group"
                outlined dense hide-details clearable>
                <template v-slot:append-outer v-if="isAdmin">
                  <v-icon
                    v-if="!editRiskProfileGroup"
                    color="primary" icon
                    @click="editRiskProfileGroup = !editRiskProfileGroup">
                      mdi-pencil-circle
                  </v-icon>
                  <v-icon
                    v-else
                    color="primary" icon
                    @click="updateRiskProfileGroup()">
                      mdi-check-circle
                  </v-icon>
                </template>
              </v-select>
            </v-col>
          </v-row>
          <v-row dense>
            <v-col>
              <v-select
                class="rounded-card"
                :readonly="!editTheme"
                :items="themes"
                item-text="name"
                item-value="id"
                :value="selectedPractice.theme"
                @change="newTheme = $event"
                label="Theme"
                outlined dense hide-details clearable>
                <template v-slot:append-outer v-if="isAdmin">
                  <v-icon
                    v-if="!editTheme"
                    color="primary" icon
                    @click="editTheme = !editTheme">
                      mdi-pencil-circle
                  </v-icon>
                  <v-icon
                    v-else
                    color="primary" icon
                    @click="updateTheme()">
                      mdi-check-circle
                  </v-icon>
                </template>
              </v-select>
            </v-col>
          </v-row>
        </v-col>
      </v-row>
      <v-divider class="mt-3 mb-5" v-if="!_.isEmpty(selectedPractice)"/>
    </v-form>
    <StaffTable
      v-if="!_.isEmpty(selectedPractice)"
      :practice="selectedPractice"
      :isAdmin="isAdmin"
      @update-practice="updatePracticeEmit($event)"/>
  </v-container>
</template>

<script>
import { apiService } from "@/common/api.service.js";
import AddPractice from "@/components/AddPractice.vue";
import StaffTable from "@/components/StaffTable.vue";
import WithoutWatchers from "@/components/mixins/WithoutWatchers.js";

import { mapGetters } from "vuex";
import {
  USER_UPDATE
} from "@/store/actions.type";
import {
  SET_ACTIVE_USER_PROP
} from "@/store/mutations.type";


export default {
  name: "PracticeTable",
  mixins: [WithoutWatchers],
  props: {
    riskProfileGroups: {
      type: Array,
      required: false,
    },
  },
  data() {
    return {
      activeSwitch: false,
      error: null,
      editPracticeName: false,
      editRiskProfileGroup: false,
      editAFSL: false,
      editTheme: false,
      editModelPortfolios: false,
      selectedPractice: {},
      newPracticeName: '',
      newRiskProfileGroup: '',
      newAFSL: '',
      newTheme: '',
      newModelPortfolios: null,
      practices: null,
      portfolios: [],
      themes:[],
    };
  },
  components: {
    AddPractice,
    StaffTable,
  },
  computed: {
    ...mapGetters(["activeUser"]),
    isAdmin() {
      if (!this._.isEmpty(this.selectedPractice)) {
        if (this.selectedPractice.admins.filter(i => i.id === this.activeUser.id).length > 0) {
          return true;
        } else {
          return false;
        }
      } else {
        return false
      }
    },
    riskProfileGroupName() {
      if (this.selectedPractice.risk_profile_group) {
        return this.riskProfileGroups.find(e => e.id === this.selectedPractice.risk_profile_group).name
      } else {
        return '';
      }
    },
    selectedIsActive() {
      if (!this._.isEmpty(this.selectedPractice)) {
        if (this.selectedPractice.id === this.activeUser.active_practice) {
          return true;
        } else {
          return false;
        }
      } else {
        return false
      }
    },
    AFSLArray() {
      if (!this._.isEmpty(this.activeUser) && this.selectedPractice) {
        let ret = new Array();
        if (this.activeUser.AFSL) {
          ret.push(this.activeUser.AFSL);
        }
        if (this.selectedPractice.AFSL_full) {
          ret.push(this.selectedPractice.AFSL_full);
        }
        return ret;
      } else {
        return new Array();
      }
    },
  },
  watch: {
    selectedPractice: function () {
      this.setActiveSwitch()
    },
    activeSwitch: function () {
      this.setActivePractice()
    },
  },
  methods: {
    setActiveSwitch() {
      this.$withoutWatchers(() => {
        if (this.selectedIsActive) {
          this.activeSwitch = true;
        } else {
          this.activeSwitch = false;
        }
      })
    },
    getPracticeIndex(practice) {
      return this.practices.findIndex(item => item.id === practice.id);
    },
    updateRiskProfileGroup() {
      this.updatePractice('risk_profile_group', this.newRiskProfileGroup)
      this.editRiskProfileGroup = !this.editRiskProfileGroup
      this.newRiskProfileGroup = null;
    },
    updateAFSL() {
      this.updatePractice('AFSL', this.newAFSL)
      this.editAFSL= !this.editAFSL
      this.newAFSL = null;
    },
    updateTheme() {
      this.updatePractice('theme', this.newTheme)
      this.editTheme = !this.editTheme
      this.newTheme = null;
    },
    updatePracticeName() {
      this.updatePractice('name', this.newPracticeName)
      this.editPracticeName = !this.editPracticeName
      this.newPracticeName = null;
    },
    updateModelPortfolios() {
      this.$refs.modelPortfolios.blur();
      this.editModelPortfolios = !this.editModelPortfolios
      if (this.newModelPortfolios != null) {
        this.updatePractice('model_portfolios', this.newModelPortfolios)
        this.newModelPortfolios = null;
      }
    },
    updatePractice(prop,value) {
      let endpoint = `/api/practices/${this.selectedPractice.id}/`;
      if (value === undefined) {
        value = null;
      }
      apiService(endpoint, "PATCH", {
        [prop]: value,
      }).then(data => {
        this.practices[this.getPracticeIndex(data)] = data;
        this.selectedPractice[prop] = data[prop];
        this.selectedPractice = data;
        if (data.id === this.activeUser.active_practice) {
          this.setActivePractice();
        }
      });

    },
    updatePracticeEmit(data) {
      this.practices[this.getPracticeIndex(data)] = data;
      this.selectedPractice = data;
    },
    setActivePractice() {
      let setActive = null;
      if (this.activeSwitch) {
        setActive = this.selectedPractice.id;
      }
      this.$store.commit(SET_ACTIVE_USER_PROP, {
        'prop': 'active_practice',
        'value': setActive
      })
      this.$store.dispatch(USER_UPDATE);
    },
    addPractice(data) {
      this.practices.push(data);
      this.selectedPractice = data;
    },
    getPracticeData() {
      let endpoint = `/api/practices/`;
      apiService(endpoint).then(data => {
        this.practices = data.results;
        this.setSelectedPractice();
      });
    },
    getPortfolios() {
      let endpoint = `/api/portfoliotemplates/`;
      apiService(endpoint).then(data => {
        this.portfolios = data.results;
      });
    },
    getThemes() {
      let endpoint = `/api/themes/`;
      apiService(endpoint).then(data => {
        this.themes = data.results;
      });
    },
    setSelectedPractice() {
      if (this.activeUser.active_practice && this.practices) {
        this.selectedPractice = this.practices.find(e => e.id === this.activeUser.active_practice);
      }
    }
  },
  mounted() {
    this.getPracticeData();
    this.getPortfolios();
    this.getThemes();
    this.setActiveSwitch()
  }
};
</script>
