<template lang="html">
  <v-form  @submit.prevent="onSubmit">
    <v-container class="pa-0  small-text  checkbox-small-labels">
      <v-row>
        <v-col :cols="10">
          <v-select
            :items="listElements"
            item-text="friendly"
            class="rounded-card"
            return-object
            v-model="selectedElement"
            label="Select element to style"
            outlined dense hide-details/>
        </v-col>
        <v-col :cols="2">
          <v-btn
            width="100%"
            rounded
            v-if="canEdit"
            @click="onSubmit"
            color="primary">
            <span class="font-weight-light">
              Save
            </span>
          </v-btn>
        </v-col>
      </v-row>
      <v-divider class="mt-5"/>
        <v-row dense>
          <v-col>
            <v-row dense>
              <v-col>
                <v-card-title class="pa-2">
                  Font Options
                </v-card-title>
              </v-col>
            </v-row>
            <v-row dense>
              <v-col>
                <v-text-field
                  :disabled="!canEdit"
                  label="Font Name"
                  v-model="selectedElement.font_name"
                  dense outlined
                  hide-details/>
              </v-col>
              <v-col>
                <v-text-field
                  :disabled="!canEdit"
                  label="Font Colour"
                  v-model="selectedElement.font_color"
                  :rules="colorRules"
                  dense outlined
                  hide-details="auto">
                  <template v-slot:prepend-inner>
                    <v-icon>#</v-icon>
                  </template>
                </v-text-field>
              </v-col>
              <v-col>
                <v-text-field
                  :disabled="!canEdit"
                  label="Font Size"
                  v-model="selectedElement.font_size"
                  type="number"
                  dense outlined
                  hide-details>
                  <template v-slot:append>
                    <v-card-text class="pa-0">
                      pt
                    </v-card-text>
                  </template>
                </v-text-field>
              </v-col>
            </v-row>
            <v-row dense>
              <v-col >
                <v-checkbox
                  :disabled="!canEdit"
                  label="Bold"
                  class='mt-2'
                  v-model="selectedElement.font_bold"
                  dense outlined
                  hide-details/>
              </v-col>
              <v-col>
                <v-checkbox
                  :disabled="!canEdit"
                  label="Italics" class='mt-2'
                  v-model="selectedElement.font_italic"
                  dense outlined
                  hide-details/>
              </v-col>
              <v-col>
                <v-checkbox
                  :disabled="!canEdit"
                  label="Underline" class='mt-2'
                  v-model="selectedElement.font_underline"
                  dense outlined
                  hide-details/>
              </v-col>

              <v-col>
                <v-checkbox
                  :disabled="!canEdit"
                  label="Small Caps" class='mt-2'
                  v-model="selectedElement.font_small_caps"
                  dense outlined
                  hide-details/>
              </v-col>
              <v-col>
                <v-checkbox
                  :disabled="!canEdit"
                  label="Bullets" class='mt-2'
                  v-model="selectedElement.font_bullet_items"
                  dense outlined
                  hide-details/>
              </v-col>
            </v-row>
            <v-row dense>
              <v-col>
                <v-card-title  class="pa-2">
                  Border and Fill Options
                </v-card-title>
              </v-col>
            </v-row>
            <v-row dense>
              <v-col>
                <v-text-field
                  :disabled="!canEdit"
                  label="Border Colour"
                  v-model="selectedElement.border_color"
                  :rules="colorRules"
                  hide-details="auto"
                  dense outlined>
                  <template v-slot:prepend-inner>
                    <v-icon>#</v-icon>
                  </template>
                </v-text-field>
              </v-col>
              <v-col>
                <v-text-field
                  :disabled="!canEdit"
                  label="Border Width"
                  v-model="selectedElement.border_width"
                  dense outlined
                  type="number"
                  hide-details>
                  <template v-slot:append>
                    <v-card-text class="pa-0">
                      pt
                    </v-card-text>
                  </template>
                </v-text-field>
              </v-col>
              <v-col>
                <v-select
                  :disabled="!canEdit"
                  label="Border Sides"
                  :items="borderSides"
                  :value="selectedBorderSides"
                  multiple
                  dense outlined hide-details
                />
              </v-col>
            </v-row>
            <v-row dense v-if="selectedElement.style">
              <v-col :cols='4' >
                <v-text-field
                  :disabled="!canEdit"
                  label="Fill Colour"
                  v-model="selectedElement.background_color"
                  :rules="colorRules"
                  hide-details="auto"
                  dense outlined
                >
                <template v-slot:prepend-inner>
                  <v-icon>#</v-icon>
                </template>
              </v-text-field>
              </v-col>
            </v-row>
          </v-col>
        </v-row>
    </v-container>
  </v-form>
</template>

<script>
import { apiService } from "@/common/api.service.js";
// import DeleteStaff from "@/components/DeleteStaff.vue";

export default {
  name: "ThemeStyler",
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
      selectedElement: {},
      elements: null,
      style: null,
      colorRules: [
        v => /^$|^[0-9A-F]{6}$/i.test(v) || !v || 'Must be a 6-digit hexadecimal code',
      ],
      sides: [
        ["Top", "top"],
        ["Bottom", "bottom"],
        ["Left", "start"],
        ["Right", "end"],
        ["Inside Vertical", "insideV"],
        ["Inside Horizontal", "insideH"],
      ],
    };
  },
  computed: {
    listElements() {
      if (this.style && this.elements) {
        let listItems = [];
        let style = this.style;
        style.friendly = "Entire Table";
        listItems.push(style);
        for (let e of this.elements) {
          e.friendly = e.type.replace('row','')
          listItems.push(e);
        }
        return listItems
      } else {
        return []
      }
    },
    borderSides(){
      return this.sides.map(function(x) {
          return x[0];
      });
    },
    selectedBorderSides() {
      if (this.selectedElement.border_sides) {
        let borderSides = []
        for (let side of this.sides) {
          if (this.selectedElement.border_sides.includes(side[1])) {
            borderSides.push(side[0]);
          }
        }
        return borderSides
      } else {
        return []
      }
    }
  },
  components: {
    // DeleteStaff,
  },
  watch: {
    theme() {
      this.getStyleData();
    }
  },
  methods: {
    onSubmit() {
      let endpoint = ''
      if (this.selectedElement.style) {
        endpoint = `/api/themes/${this.theme.id}/styles/${this.style.id}/elements/${this.selectedElement.id}/`;
      } else {
        endpoint = `/api/themes/${this.theme.id}/styles/${this.selectedElement.id}/`;
      }
      apiService(endpoint, "PATCH", this.selectedElement)
    },
    getStyleData() {
      let endpoint = `/api/themes/${this.theme.id}/styles/`;
      apiService(endpoint).then(data => {
        // only one style per theme
        this.style = data.results[0];
        this.getElementData(data.results[0].id);
        this.selectedElement = this.style;
      });
    },
    getElementData(style) {
      let endpoint = `/api/themes/${this.theme.id}/styles/${style}/elements/`;
      apiService(endpoint).then(data => {
        this.elements = data.results;
      });
    }
  },
  mounted() {
    this.getStyleData();
  }
};
</script>
