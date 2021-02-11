<template lang="html">
  <v-container >
  <v-form @submit.prevent="onSubmit">
    <v-card class="pa-2">
      <v-row>
        <v-col>
          {{ investmentName.name }}
        </v-col>
        <v-col>
          {{ total }}
        </v-col>
      </v-row>
      <v-row v-for="n in 12" :key="n" dense>
        <v-col>
          <v-autocomplete
            dense solo hide-details
            :value = "getAA(n, 'name')"
            @change = "setAA(n, $event, 'name')"
            :items="aaNames"
            return-object
            item-text="name"
          />
        </v-col>
        <v-col>
          <v-text-field
          number
            dense solo hide-details
            :value = "getAA(n, 'percentage')"
            @change = "setAA(n, $event, 'percentage')"
          />
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-btn type="submit" color="primary">
            Save
          </v-btn>
        </v-col>
      </v-row>
    </v-card>
  </v-form>
</v-container>
</template>

<script>
import { apiService } from "@/common/api.service.js";

export default {
  name: "AssetAllocationNameDetail",
  props: {
    investmentName: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      aaNames: [],
      aa: null,
      next: null,
      total: 0,
    };
  },
  watch: {
    investmentName() {
      this.getAANames();
      this.getAAList()
    },
    aa(){
      this.getTotal()
    },
  },
  methods: {
    getTotal() {
      if (this.aa) {
        let result = 0;
        for (let item of this.aa){
          if ('percentage' in item) {
            result += Number(item['percentage']);
          }
        }
        this.total = result;
      } else {
        this.total = 0;
      }
    },
    getAA(idx, field){
      if (this.aa) {
        if (this.aa.length >= idx) {
          return this.aa[idx-1][field]
        }
      }
      // else {
      //   return null
      // }
    },
    setAA(idx, event, field) {
      if (this.aa.length >= idx) {
        if (field === 'name'){
          this.aa[idx-1].name_id = event.id
        }
        this.aa[idx-1][field] = event;
      } else {
        let newItem = {}
        if (field === 'name'){
          newItem.name_id = event.id
        }
        newItem[field] = event;
        newItem['investment'] = this.investmentName.linked_inv;
        this.aa.push(newItem);
      }
      this.getTotal();
    },
    getAANames() {
      let endpoint = null
      if (this.next) {
        endpoint = this.next;
      } else {
        endpoint = `/api/aaname/`;
      }
      apiService(endpoint, "GET").then(data => {
        this.aaNames.push(...data.results);
        if (data.next) {
          this.next = data.next;
          this.getAANames();
        } else {
          this.next = null;
        }
      });
    },
    getAAList() {
      let endpoint = `/api/investmenttemplate/${this.investmentName.linked_inv}/aa/`;
      apiService(endpoint, "GET").then(data => {
        this.aa = data.results;
      });
    },
    onSubmit() {
      let endpoint = null
      let method = null
      for (let i=0; i<this.aa.length; i++) {
        if (this.aa[i].id) {
          endpoint = `/api/investmenttemplate/${this.investmentName.linked_inv}/aa/${this.aa[i].id}/`;
          method = "PATCH";
        } else {
          endpoint = `/api/investmenttemplate/${this.investmentName.linked_inv}/aa/`;
          method = "POST";
        }
        apiService(endpoint, method, this.aa[i]).then(data => {
          this.aa[i] = data;
          console.log("Saved: "+this.aa[i].name.name)
        });
      }
    }
  },
  mounted() {
    this.getAANames();
    this.getAAList()
  }
};

</script>
