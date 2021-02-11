<template>
  <v-card>
    <v-container fluid class="grey lighten 5">
      <v-card>
        <v-card-title>
          Template Management
        </v-card-title>
      </v-card>
      <v-card
        v-for="(templateType, index) in templateTypes"
        :key="index"
        class="pa-2">
        {{templateType[0]}}
        <TemplateSelector
          :nameList="getNameList(templateType)"
          :templateType="templateType[0]"
        />
      </v-card>
    </v-container>
  </v-card >
</template>

<script>
import { apiService } from "@/common/api.service";

import TemplateSelector from "@/components/templatemgmt/TemplateSelector.vue";

export default {
  name: "Templates",
  data() {
    return {
      platformNames: [],
      portfolioTemplates: [],
      investmentNames: [],
      aaNames: [],
      riskProfileGroupTemplates: [],
      afsls: [],
      themes: [],
      templateTypes: [
        ["Platforms", "platformNames"],
        ["Platform Names","platformNames"],
        ["Platform Fees","platformNames"],
        ["Portfolios","portfolioTemplates"],
        ["Investment Fees","platformNames"],
        ["Investments","investmentNames"],
        ["Investment Names","investmentNames"],
        ["Asset Allocation","investmentNames"],
        ["Asset Allocation Names","aaNames"],
        ["Risk Profiles","riskProfileGroupTemplates"],
        ["Themes","themes"],
        ["AFSLs","afsls"],
      ],
      endpoints: [
        [`/api/platformnames/`, "platformNames"],
        [`/api/portfoliotemplates/`, "portfolioTemplates"],
        [`/api/investmentname/`, "investmentNames"],
        [`/api/aaname/`, "aaNames"],
        [`/api/themes/`, "themes"],
        [`/api/riskprofilegrouptemplates/`, "riskProfileGroupTemplates"],
        [`/api/afsls/`, "afsls"],
      ],
    };
  },
  components: {
    TemplateSelector,
  },
  methods: {
    getNameList(templateType) {
      return this[templateType[1]];
    },
    cycleEndpoints(){
      for (let endpoint of this.endpoints) {
        this.getNameData(endpoint);
      }
    },
    getNameData(endpoint) {
      // console.log(this);
      // console.log(endpoint[1]);
      let dataField = endpoint[1];
      // console.log(this[dataField]);
      // console.log(this[endpoint[1]]);
      apiService(endpoint[0]).then(data => {
        this[dataField].push(...data.results);
        if (data.next) {
          this.next = data.next;
          this.getNameData([this.next, endpoint[1]])
        }
      });
    },
  },
  mounted() {
    this.cycleEndpoints()
  }
};
</script>
