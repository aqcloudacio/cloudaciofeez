<template lang="html">
  <v-form
    @submit.prevent="onSubmit"
    :disabled="true">
    <v-container class="pa-0  small-text  checkbox-small-label">
      <v-row>
        <v-col :cols="10">
          <v-select
            class="rounded-card"
            :items="tableTypes"
            v-model="selectedTableType"
            label="Select section to set preferences"
            outlined dense hide-details>
          </v-select>
        </v-col>
        <v-col :cols="2" >
          <v-btn
          rounded
          width="100%"
            v-if="canEdit"
            @click="onSubmit"
            color="primary">
            <span class="font-weight-light">
              Save
            </span>
          </v-btn>
        </v-col>
      </v-row>
      <v-divider class="mt-5" v-if="selectedTableType"/>
      <v-container v-if="selectedTableType=='Entire Document'">
        <v-row dense>
          <v-col>
            <v-card-title class="pa-2">
              General Preferences
            </v-card-title>
          </v-col>
        </v-row>
        <v-row dense>
          <v-col :cols="6">
            <v-checkbox
              :disabled="!canEdit"
              class="mt-1"
              hide-details="auto"
              label='Style "Subheader #1" is full width of tables'
              v-model="structure.full_width_subheader1" />
          </v-col>
          <v-col :cols="6">
            <v-checkbox
              :disabled="!canEdit"
              class="mt-1"
              hide-details="auto"
              label='Style "Subheader #2" is full width of tables'
              v-model="structure.full_width_subheader2" />
          </v-col>
        </v-row>
      </v-container>

      <v-container v-if="selectedTableType=='Fee Tables'">
        <v-row dense>
          <v-col>
            <v-card-title class="pa-2">
              General Preferences
            </v-card-title>
          </v-col>
        </v-row>
        <v-row dense>
          <v-col :cols="6">
            <v-checkbox
              :disabled="!canEdit"
              class="mt-1"
              hide-details="auto"
              label='Display alternative platforms in fee tables'
              v-model="structure.display_alternative_platform" />
          </v-col>
          <v-col :cols="6">
            <v-checkbox
              :disabled="!canEdit"
              class="mt-1"
              hide-details="auto"
              label='Split platform types across tables'
              v-model="structure.split_platform_types" />
          </v-col>
        </v-row>
        <v-row dense>
          <v-col>
            <v-card-title class="pa-2 pt-4">
              Page Orientation Preferences
            </v-card-title>
          </v-col>
        </v-row>
        <v-row dense>
          <v-col :cols="6">
            <v-text-field
              :disabled="!canEdit"
              type="number"
              label='Maximum columns on portrait page'
              v-model="structure.portrait_overflow_limit"
              dense outlined
              hide-details="auto"
              :rules="$ruleGTZero"
              />
          </v-col>
          <v-col :cols="6">
            <v-checkbox
              :disabled="!canEdit"
              class="mt-1"
              hide-details="auto"
              label='Change to landscape if maximum exceeded'
              v-model="structure.change_orientation_if_overflow" />
          </v-col>
        </v-row>
        <v-row dense v-if="structure.change_orientation_if_overflow">
          <v-col :cols="6">
            <v-text-field
              :disabled="!canEdit"
              class="mt-2"
              type="number"
              label='Maximum columns on landscape page'
              v-model="structure.landscape_overflow_limit"
              dense outlined
              hide-details="auto"
              :rules="$ruleGTZero"
              />
          </v-col>
        </v-row>
        <v-row dense>
          <v-col>
            <v-card-title class="px-2 pt-4 pb-0">
              Content Preferences
            </v-card-title>
          </v-col>
        </v-row>
        <v-row dense>
          <v-col :cols="6">
            <v-checkbox
              :disabled="!canEdit"
              class="mt-1"
              hide-details="auto"
              label='Display percentage calculation for subtotals'
              v-model="structure.display_percentage_subtotal"
              />
          </v-col>
          <v-col :cols="6">
            <v-checkbox
              :disabled="!canEdit"
              class="mt-1"
              hide-details="auto"
              label='Display percentage calculation for totals'
              v-model="structure.display_percentage_total"
              />
          </v-col>
        </v-row>
        <v-row dense>
          <v-col :cols="6">
            <v-checkbox
              :disabled="!canEdit"
              class="mt-1"
              hide-details="auto"
              label='Display "N/A" in lieu of "%" for flat fees'
              v-model="structure.display_NA_flat_fees" />
          </v-col>
          <v-col :cols="6">
            <v-checkbox
              :disabled="!canEdit"
              class="mt-1"
              hide-details="auto"
              label='Display rows with no applicable fees'
              v-model="structure.display_null_rows" />
          </v-col>
        </v-row>
        <v-row dense>
          <v-col :cols="6">
            <v-select
              :disabled="!canEdit"
              class="mt-2"
              dense outlined
              hide-details="auto"
              :items="percentagePositions"
              label='Positioning of percentage calculations'
              v-model="structure.percentage_position" />
          </v-col>
        </v-row>
      </v-container>

      <v-container v-if="selectedTableType=='Product Advice Tables'">
        <v-row dense>
          <v-col>
            <v-card-title class="pa-2">
              General Preferences
            </v-card-title>
          </v-col>
        </v-row>
        <v-row dense>
          <v-col :cols="6">
            <v-checkbox
              :disabled="!canEdit"
              class="mt-1"
              hide-details="auto"
              label='Hide "Allocation" column'
              v-model="structure.hide_percentage" />
          </v-col>
          <v-col :cols="6">
            <v-checkbox
              :disabled="!canEdit"
              class="mt-1"
              hide-details="auto"
              label='Hide "ICR" column'
              v-model="structure.hide_ICR" />
          </v-col>
        </v-row>
      </v-container>

      <v-container v-if="selectedTableType=='Asset Allocation Tables'">
        <v-row dense>
          <v-col>
            <v-card-title class="pa-2">
              General Preferences
            </v-card-title>
          </v-col>
        </v-row>
        <v-row dense>
          <v-col :cols="6">
            <v-checkbox
              :disabled="!canEdit"
              class="mt-1"
              hide-details="auto"
              label='Hide "Variance" column'
              v-model="structure.hide_variance" />
          </v-col>
          <v-col :cols="6">
            <v-checkbox
              :disabled="!canEdit"
              class="mt-1"
              hide-details="auto"
              label='Hide bar charts'
              v-model="structure.hide_bar_chart" />
          </v-col>
        </v-row>
        <v-row dense>
          <v-col>
            <v-card-title class="pa-2 pt-4">
              Table Inclusions
            </v-card-title>
          </v-col>
        </v-row>
        <v-row dense>
          <v-col :cols="6">
            <v-checkbox
              :disabled="!canEdit"
              class="mt-1"
              hide-details="auto"
              label='Include "Current vs Risk Profile'
              v-model="structure.include_cur_vs_rp" />
          </v-col>
          <v-col :cols="6">
            <v-checkbox
              :disabled="!canEdit"
              class="mt-1"
              hide-details="auto"
              label='Include "Recommended vs Risk Profile'
              v-model="structure.include_rec_vs_rp" />
          </v-col>
        </v-row>
        <v-row dense>
          <v-col :cols="6">
            <v-checkbox
              :disabled="!canEdit"
              class="mt-1"
              hide-details="auto"
              label='Include "Current vs Risk Profile vs Recommended'
              v-model="structure.include_cur_vs_rp_vs_rec" />
          </v-col>
          <v-col :cols="6">
            <v-checkbox
              :disabled="!canEdit"
              class="mt-1"
              hide-details="auto"
              label='Include "Current vs Recommended'
              v-model="structure.include_cur_vs_rec" />
          </v-col>
        </v-row>
      </v-container>
    </v-container>
  </v-form>
</template>

<script>
import { apiService } from "@/common/api.service.js";
import { ruleGTZero } from "@/components/mixins/Rules.js";

export default {
  name: "ThemeSetup",
  mixins: [ruleGTZero],
  props: {
    canEdit: {
      type: Boolean,
      required: true,
    },
    theme: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      isDisabled: true,
      selectedTableType: null,
      structure: null,
      tableTypes: [
        "Entire Document",
        "Fee Tables",
        "Product Advice Tables",
        "Asset Allocation Tables"
      ],
      percentagePositions: [
        "Left",
        "Right",
        "Bottom",
      ],
    };
  },
  computed: {
  },
  components: {
  },
  watch: {
    theme: function () {
      this.getStructureData()
    },
  },
  methods: {
    onSubmit() {
      let endpoint = `/api/themes/${this.theme.id}/structures/${this.structure.id}/`;
      apiService(endpoint, "PATCH", this.structure).then(data => {
        this.structure = data;
      })
    },
    getStructureData() {
      let endpoint = `/api/themes/${this.theme.id}/structures/`;
      // There is only one structure per theme
      apiService(endpoint).then(data => {
        this.structure = data.results[0];
      });
    }
  },
  mounted() {
    this.getStructureData()
  }
};
</script>
