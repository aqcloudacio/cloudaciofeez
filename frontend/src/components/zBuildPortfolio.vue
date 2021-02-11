<template lang="html">
  <v-container>
      <!-- <v-row>
        <v-col
        :cols="10">
          <v-select
              :items="portfolios"
              @change="forceRerender()"
              item-text="name"
              item-value="id"
              v-model="selectedPortfolio"
              outlined dense>
          </v-select>
        </v-col>
        <v-col
        :cols="2">
          <AddPortfolioName
            :userID="userID"
            @add-portfolio="addPortfolio"/>
        </v-col>
      </v-row> -->
      <PortfolioTable
        :portfolioID="selectedPortfolio"
        :key="portfolioKey"
        v-if="selectedPortfolio" />
  </v-container>
</template>

<script>

import { apiService } from "@/common/api.service";
import PortfolioTable from "@/components/PortfolioTable.vue";
import AddPortfolioName from "@/components/AddPortfolioName.vue";


export default {
  name: "BuildPortfolio",
  data() {
    return {
      portfolios: [],
      active: false,
      portfolioKey:0,
      selectedPortfolio: 0,
    };
  },
  props: {
    userID: {
      type: Number,
      required: true,
    }
  },
  components: {
    PortfolioTable,
    AddPortfolioName,
  },
  methods: {
    forceRerender(){
      this.portfolioKey += 1;
    },
    addPortfolio(data){
      console.log(data)
      this.forceRerender();
      this.getPortfolios();
    },
    getPortfolios() {
      let endpoint = `/api/portfoliotemplates/`;
      apiService(endpoint).then(data => {
        this.portfolios = data.results;
      });
    },
  },
  mounted() {
    this.getPortfolios();
  }
}
</script>
