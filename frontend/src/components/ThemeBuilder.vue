<template lang="html">
  <v-form  @submit.prevent="onSubmit">
    <v-container class="pa-0 small-text  checkbox-small-label">
      <v-row>
        <v-col :cols="10">
          <v-select
            :items="tableTypes"
            :item-value="[0]"
            return-object
            class="rounded-card"
            v-model="selectedTableType"
            label="Select table to build"
            outlined dense hide-details>
            <template v-slot:item="{ item }">
              {{item[1]}}
            </template>
            <template v-slot:selection="{ item }">
              {{item[1]}}
            </template>
          </v-select>
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
        <v-data-table
          :disabled="!canEdit"
          :headers="headers"
          :items="selectedContent"
          hide-default-footer
          disable-pagination
          sort-by.sync="order">
          <template v-slot:item.handle>
            <v-tooltip bottom @click.stop>
              <template v-slot:activator="{ on }">
                <v-icon v-on="on" style="max-width: 28px;" class="handle" v-if="canEdit">mdi-reorder-horizontal</v-icon>
              </template>
              <span>
                Drag to reorder
              </span>
            </v-tooltip>
          </template>
          <template v-slot:item.name="{item}">
              <v-text-field v-model="item.name" :disabled="!canEdit">
              </v-text-field>
          </template>
          <template v-slot:item.element="{item}">
            <v-select
              :disabled="!canEdit"
              :value="item.element_name"
              @change="item.element = $event.id"
              :items="elements"
              item-text="type"
              return-object>
              <template v-slot:item="{item}">
                {{item.type.replace('row','')}}
              </template>
              <template v-slot:selection="{item}">
                {{item.type.replace('row','')}}
              </template>
            </v-select>
          </template>
          <template v-slot:item.visible="{item}">
              <v-checkbox :disabled="!canEdit" v-model="item.visible"/>
          </template>
      </v-data-table>
    </v-container>
  </v-form>
</template>

<script>
import { apiService } from "@/common/api.service.js";
import Sortable from "sortablejs";

export default {
  name: "ThemeBuilder",
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
      selectedTableType: null,
      content: [],
      next: null,
      headers: [
          { text: '', value: 'handle'},
          { text: 'Item', value: 'type' },
          { text: 'Name', value: 'name' },
          { text: 'Style', value: 'element' },
          { text: 'Visible', value: 'visible' },
        ],
      elements: null,
    };
  },
  computed: {
    selectedContent() {
      if (this.selectedTableType) {
        return this.content.filter(i => i.table_type === this.selectedTableType[0])
      } else {
        return []
      }
    },
    tableTypes() {
      if (this.content[0]) {
        return this.content[0].content_type_list
      } else {
        return []
      }
    }
  },
  components: {
  },
  watch: {
    theme() {
      this.getContentData();
      this.setSortable();
      this.getElementData()
    }
  },
  methods: {
    onSubmit() {
      let endpoint = ''
      for (let content of this.selectedContent) {
        endpoint = `/api/themes/${this.theme.id}/content/${content.id}/`
        apiService(endpoint, "PATCH", content)
      }
    },
    getContentData() {
      let endpoint = `/api/themes/${this.theme.id}/content/`;
      if (this.next) {
        endpoint = this.next;
      }
      apiService(endpoint).then(data => {
        this.content.push(...data.results);
        if (data.next) {
          this.next = data.next;
          this.getContentData()
        } else {
          this.next = null;
        }
      });
    },
    resetContentOrder(_self) {
      for (let i = 0; i < _self.selectedContent.length; i++) {
        const idx = this.content.findIndex(item => item.id === this.selectedContent[i].id);
        this.content[idx].order = i
      }
    },
    setSortable() {
      let table = document.querySelector(".v-data-table tbody");
      const _self = this;
      Sortable.create (table,  {
        handle: ".handle",
        onEnd({newIndex, oldIndex}) {
          const rowSelected = _self.selectedContent.splice(oldIndex,1) [0]
          _self.selectedContent.splice(newIndex, 0, rowSelected);
          _self.resetContentOrder(_self)
        }
      });
    },
    getElementData() {
      let endpoint = `/api/themes/${this.theme.id}/styles/${this.theme.styles[0]}/elements/`;
      apiService(endpoint).then(data => {
        this.elements = data.results;
      });
    }
  },
  mounted() {
    this.getContentData();
    this.setSortable();
    this.getElementData()
  }
};
</script>
 <style>
   .handle {
    cursor: move !important;
    cursor: -webkit-grabbing !important;
  }
</style>
