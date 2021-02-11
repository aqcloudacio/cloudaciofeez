<template lang="html">
  <v-form >
    <v-combobox
      outlined
      dense
      class="rounded-card small-text"
      v-model="newPlatform"
      :items="platformNames"
      @keyup.enter="delaySubmit"
      placeholder="Add a new platform"
      item-text="name"
      no-data-text="Create a custom platform"
      ref="combobox"
      :search-input.sync="search"
      allow-overflow
      hide-details="auto"
      >

      <template v-slot:prepend-item v-if="statusToShow.includes(status) && sponsoredItem">
        <v-list-item @click="selectSponsored">
          <v-tooltip left>
            <template v-slot:activator="{ on }">
              <v-list-item-icon class="my-3 mr-2"  v-on="on">
                <v-icon color="yellow">mdi-star</v-icon>
              </v-list-item-icon>
            </template>
            <span>Sponsored Product</span>
          </v-tooltip>
          <v-list-item-content>
            <v-list-item-title>{{sponsoredItem.platform_name}}</v-list-item-title>
          </v-list-item-content>
          <v-list-item-action class="ml-2 my-2">
            <v-btn icon @click.stop :href="sponsoredItem.link" target="_blank">
              <v-icon color="grey lighten-1">mdi-information</v-icon>
            </v-btn>
          </v-list-item-action>
        </v-list-item>
      </template>
      <template v-slot:append>
        <v-slide-x-reverse-transition
           mode="out-in"
           >
          <v-icon
            :key="`icon-${isSaving}`"
            ref="submit"
            @click="delaySubmit"
            color="primary"

            v-text="'mdi-plus-circle'"
            :disabled="isDisabled"
            >
          </v-icon>
        </v-slide-x-reverse-transition>
      </template>
      <template v-slot:no-data>
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title>
              No platforms match "<strong>{{ search }}</strong>". Press <kbd>enter</kbd> to create a custom platform.
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </template>
    </v-combobox>
  </v-form>
</template>

<script>
import { apiService } from "@/common/api.service.js";
import { mapGetters } from "vuex";

export default {
  name: "AddPlatform",
  props: {
    status: {
      type: String,
      required: false,
    },
    currentType: {
      type: String,
      required: false,
    },
  },
  data() {
    return {
      search: null,
      next: null,
      newPlatform: null,
      error: null,
      isSaving: false,
    };
  },
  computed: {
    ...mapGetters(["activeScenario", "platformNames", "adverts"]),
    isDisabled() {
      return this.newPlatform === null && this.search === null
    },
    sponsoredItem() {
      let item = [];
      if (this.currentType == "Investment") {
        item =  this.adverts.filter(x => x.type_name === "starred_invwrap");
      } else if (this.currentType == "Pension") {
        item = this.adverts.filter(x => x.type_name === "starred_pension");
      } else if (this.currentType == "Accumulation") {
        item = this.adverts.filter(x => x.type_name === "starred_super");
      }
      return item[0]
    },
    statusToShow() {
      if (this.sponsoredItem && this.sponsoredItem.show_in_alternative) {
        return ["Recommended", "Alternative"];
      } else {
        return ["Recommended"];
      }
    },
    platformStrings() {
      if (!this._.isEmpty(this.platformNames)) {
        return this.platformNames.map(x => x.name);
      } else {
        return [];
      }
    }
  },
  methods: {
    selectSponsored(){
      this.search = this.sponsoredItem.platform_name;
      this.newPlatform = this.sponsoredItem.platform_name;
      this.$refs.combobox.isMenuActive = false;
    },
    getPlatformID(platform) {
      if (platform.id != null) {
        return platform.id
      } else if (this.platformStrings.includes(platform)){
        let result = this.platformNames.filter(obj => {
          return obj.name === platform;
        })
        return result[0].id;
      } else {
        return null;
      }
    },
    delaySubmit() {
      // Resolves a combobox bug where it does not update props until blur/tick
      this.isSaving = true;
      this.$refs.combobox.blur();
      this.$nextTick(() => {
        if (this.newPlatform != null) {
          this.onSubmit();
        } else {
          this.isSaving = false;
        }
      })
    },
    onSubmit() {
      let endpoint = `/api/scenarios/${this.activeScenario.id}/platforms/`;
      if (this.platformNames.includes(this.newPlatform)
          || this.platformStrings.includes(this.newPlatform)
          || this.platformStrings.includes(this.newPlatform.name)) {
            let name_id = this.getPlatformID(this.newPlatform);
        apiService(endpoint, "POST", {
          name_id: name_id,
          scenario: this.activeScenario.id,
          status: this.status,
        }).then(data => {
          this.$emit("add-platform", data);
          this.newPlatform = null;
          this.isSaving = false;
        });
        if (this.error) {
          this.error = null;
        }
      } else {
        apiService(endpoint, "POST", {
          name_id: null,
          custom_name: this.newPlatform,
          scenario: this.activeScenario.id,
          edited: true,
          status: this.status,
        }).then(data => {
          this.$emit("add-platform", data);
          this.newPlatform = null;
          this.isSaving = false;


        });
        if (this.error) {
          this.error = null;
        }
      }
    }
  },
};
</script>
<style media="screen">
  .v-btn:not(.v-btn--text):not(.v-btn--outlined):hover:before {
    opacity: 0!important;
  }
  .v-text-field--outlined > .v-input__control > .v-input__slot {
    /* min-height: 40px !important; */
    /* max-height: 40px !important;
    display: flex!important;
  align-items: center!important */
  }
</style>
