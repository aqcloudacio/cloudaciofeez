<template lang="html">
  <v-container class="pa-0 small-text">
    <v-form  @submit.prevent="onSubmit">
      <template v-if="!scenario">
        <v-row align="center">
          <v-col
          :cols="6">
            <v-select
              class="rounded-card"
              v-if="!editThemeName"
              :items="themes"
              item-text="name"
              return-object
              v-model="selectedTheme"
              label="Theme Name"
              placeholder="Select a Theme"
              outlined dense hide-details>
              <template v-slot:append-outer v-if="canEdit" style="margin-top: 0px">
                <v-icon
                  v-if="!editThemeName && themeIsSelected"
                  color="primary" icon
                  @click="editThemeName = !editThemeName">mdi-pencil-circle</v-icon>
              </template>
              <template v-slot:append-outer v-else-if="!canEdit && themeIsSelected">
                <v-tooltip bottom>
                   <template v-slot:activator="{ on }">
                      <v-icon
                        v-on='on'
                        color="primary" icon
                        >mdi-lock</v-icon>
                  </template>
                  <span>{{lockMessage}}</span>
                </v-tooltip>
              </template>
            </v-select>
            <v-text-field
              v-else
              label="Theme Name"
              :value="selectedTheme.name"
              @change="newThemeName = $event"
              dense outlined
              hide-details>
              <template v-slot:append-outer v-if="canEdit && themeIsSelected">
                <v-icon
                  v-if="editThemeName"
                  color="green" icon
                  @click="updateThemeName()">mdi-check-circle</v-icon>
              </template>
            </v-text-field>
          </v-col>
          <v-col
          >
          <v-container class="pa-0 d-flex">
            <v-switch
              inset
              v-if="!_.isEmpty(selectedTheme)"
              v-model="activeSwitch"
              label="Active Theme"/>
          <v-spacer />
          <v-card-actions class="pr-0">
            <DeleteObj
              v-if="canEdit && themeIsSelected"
              :objectType="'theme'"
              :objectToDelete="selectedTheme"
              @delete-object="deleteTheme($event)"
              :color="'primary'"
            />

            <AddTheme
              @add-theme="addTheme($event)"/>
          </v-card-actions>
        </v-container>
          </v-col>
        </v-row>
      </template>
      <v-divider class="mt-1 mb-4" v-if="themeIsSelected"/>
      <v-row v-if="!_.isEmpty(selectedTheme)">
        <v-col :cols="4">
          <v-card
            :class="getCardClass('setup')"
            @click="active='setup'">
            <v-card-title
              :class="getCardTextClass('setup')">
            Document Preferences
            </v-card-title>
          </v-card>
        </v-col>
        <v-col :cols="4">
          <v-card
            color="primary"
            :class="getCardClass('builder')"
            @click="active='builder'">
            <v-card-title :class="getCardTextClass('builder')">
              Table Builder
            </v-card-title>
          </v-card>
        </v-col>
        <v-col :cols="4">
          <v-card
            color="primary"
            :class="getCardClass('styler')"
            @click="active='styler'">
            <v-card-title  :class="getCardTextClass('styler')">
              Theme Styler
            </v-card-title>
          </v-card>
        </v-col>
      </v-row>
      <v-row v-if="themes &&!_.isEmpty(selectedTheme)">
        <v-col>
          <ThemeStyler
            v-if="active==='styler' && !_.isEmpty(selectedTheme)"
            :theme="selectedTheme"
            :canEdit="canEdit"
          />
          <ThemeBuilder
            v-if="active==='builder' && !_.isEmpty(selectedTheme)"
            :theme="selectedTheme"
            :canEdit="canEdit"
          />
          <ThemeSetup
            v-if="active==='setup' && !_.isEmpty(selectedTheme)"
            :theme="selectedTheme"
            :canEdit="canEdit"
          />
        </v-col>
      </v-row>
    </v-form>
  </v-container>
</template>

<script>
import { apiService } from "@/common/api.service.js";
import AddTheme from "@/components/AddTheme.vue";
import WithoutWatchers from "@/components/mixins/WithoutWatchers.js";
import ThemeStyler from "@/components/ThemeStyler.vue";
import ThemeBuilder from "@/components/ThemeBuilder.vue";
import ThemeSetup from "@/components/ThemeSetup.vue";
import DeleteObj from "@/components/DeleteObj.vue"
import { mapGetters } from "vuex";
import {
  USER_UPDATE
} from "@/store/actions.type";
import {
  SET_ACTIVE_USER_PROP
} from "@/store/mutations.type";

export default {
  name: "ThemeTable",
  mixins: [WithoutWatchers],
  props: {
    scenario: {
      type: Object,
      required: false,
    },
  },
  data() {
    return {
      activeSwitch: false,
      error: null,
      editThemeName: false,
      selectedTheme: {},
      newThemeName: '',
      themes: null,
      active: 'setup',
    };
  },
  components: {
    AddTheme,
    ThemeStyler,
    ThemeBuilder,
    ThemeSetup,
    DeleteObj,
  },
  computed: {
    ...mapGetters(["activeUser"]),
    lockMessage() {
      let msg = '';
      if (!this.isNotAFSLLimited) {
        msg += 'You cannot edit AFSL Themes'
      }
      else if (!this.isPracticeAdmin) {
        msg += 'You are not an admin of this Practice'
      }
      return msg
    },
    canEdit() {
      if (this.isPracticeAdmin && this.isNotAFSLLimited && this.isNotDefaultTemplate) {
        return true
      } else {
        return false
      }
    },
    isNotDefaultTemplate() {
      if (this.themes && !this._.isEmpty(this.selectedTheme)) {
        if (this.selectedTheme.template && this.selectedTheme.default) {
          return false
        } else {
          return true
        }
      } else {
        return true
      }
    },
    isPracticeAdmin() {
      if (this.themes && !this._.isEmpty(this.selectedTheme)) {
        if (this.selectedTheme.active_practices.length > 0) {
          return this.selectedTheme.active_practices.some(item => this.activeUser.admin_practices.includes(item));
        } else {
          return true
        }
      } else {
        return true
      }
    },
    isNotAFSLLimited() {
      if (this.themes && this.selectedTheme) {
        if (this._.isEmpty(this.selectedTheme.afsls)) {
          return true
        } else {
          return false
        }
      } else {
        return true
      }
    },
    selectedIsActive() {
      if (this.selectedTheme) {
        if (this.selectedTheme.id === this.activeUser.active_theme) {
          return true;
        } else {
          return false;
        }
      } else {
        return false
      }
    },
    scenarioTheme(){
      if (this.scenario) {
        return this.scenario.theme;
      } else {
        return null;
      }
    },
    themeIsSelected() {
      return (!this._.isEmpty(this.selectedTheme) && !this.scenario)
    }
  },
  watch: {
    selectedTheme: function () {
      this.setActiveSwitch()
    },
    activeSwitch: function () {
      this.setActiveTheme()
    },
    scenarioTheme: function() {
      this.setSelectedTheme();
    }
  },
  methods: {
    getCardClass(card) {
      if (card === this.active) {
        return 'primary rounded-card active-card'
      } else {
        return 'grey1 rounded-card'
      }
    },
    getCardTextClass(card) {
      if (card === this.active) {
        return 'justify-center subtitle-2 font-weight-medium white--text'
      } else {
        return 'justify-center subtitle-2 font-weight-light'
      }
    },
    deleteTheme(data) {
      this.selectedTheme = {};
      const i = this.themes.findIndex(item => item.id === data.id);
      this.$delete(this.themes,i)
    },
    setActiveSwitch() {
      this.$withoutWatchers(() => {
        if (this.selectedIsActive) {
          this.activeSwitch = true;
        } else {
          this.activeSwitch = false;
        }
      })
    },
    getThemeIndex(theme) {
      return this.themes.findIndex(item => item.id === theme.id);
    },
    updateThemeName() {
      this.updateTheme('name', this.newThemeName)
      this.editThemeName = !this.editThemeName
      this.newThemeName = null;
    },
    updateTheme(prop,value) {
      if (value) {
        let endpoint = `/api/themes/${this.selectedTheme.id}/`;
        apiService(endpoint, "PATCH", {
          [prop]: value,
        }).then(data => {
          this.selectedTheme[prop] = data[prop];
          this.themes[this.getThemeIndex(data)] = data;
          if (data.id === this.activeUser.active_theme) {
            this.setActiveTheme();
          }
        });
      }
    },
    setActiveTheme() {
      let setActive = null;
      if (this.activeSwitch) {
        setActive = this.selectedTheme.id;
      }
      this.$store.commit(SET_ACTIVE_USER_PROP, {
        'prop': 'active_theme',
        'value': setActive
      })
      this.$store.dispatch(USER_UPDATE);
    },
    addTheme(data) {
      this.themes.push(data);
      this.selectedTheme = data;
    },
    getThemeData() {
      let endpoint = `/api/themes/`;
      apiService(endpoint).then(data => {
        this.themes = data.results;
        this.setSelectedTheme();
        this.$emit('load-themes', data.results);
      });
    },
    setSelectedTheme() {
      if (!this._.isEmpty(this.scenario)) {
        this.selectedTheme = this.themes.find(e => e.id === this.scenarioTheme);
      } else if (this.activeUser.active_theme && this.themes){
        this.selectedTheme = this.themes.find(e => e.id === this.activeUser.active_theme);
      }
    },
  },
  mounted() {
    this.getThemeData();
    this.setActiveSwitch()
  }
};
</script>
<style media="screen">
  .active-card:before {
    background: none !important;
  }
</style>
