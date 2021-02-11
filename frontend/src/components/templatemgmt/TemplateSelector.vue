<template>
  <v-card>
    <v-row>
      <v-col :cols="8">
        <v-autocomplete
          v-model="selectedName"
          :items="nameList"
          :item-text="getItemText()"
          :return-object="true"
          outlined dense
          @change="objectRouteSelector()"
          hide-details
        />
      </v-col>
      <v-col :cols="2">
        <v-dialog v-model="modifyDialog">
          <template v-slot:activator="{ on }">
            <v-btn color="primary" v-on="on">
              <v-icon>
                mdi-magnify
              </v-icon>
            </v-btn>
          </template>
          <PlatformNameDetail
            v-if="templateType == 'Platform Names'"
            :platformName="selectedObject"
            :template="true"
            :new="false"
            @disable-dialog="modifyDialog = !modifyDialog"
          />
          <TemplatePlatformDetail
            v-if="templateType == 'Platforms'"
            :platform="selectedObject"
            :template="true"
            @modify-platform="modifyDialog = !modifyDialog"
          />
          <PlatformFeeSelector
            :key="platformFeeKey"
            v-if="templateType == 'Platform Fees'"
            :platform="selectedName.platform_template"
            :platformFees="selectedArray"
            :template="true"
            :investmentClassList="investmentClassList"
            @modify-fees="modifyDialog = !modifyDialog"
          />
          <PortfolioTable
            :portfolio="selectedObject"
            v-if="templateType == 'Portfolios'"
          />
          <InvestmentFeeDetail
            v-if="templateType == 'Investment Fees'"
            :platform="selectedObject"
            @modify-platform="modifyDialog = !modifyDialog"
          />
          <InvestmentNameDetail
            v-if="templateType == 'Investment Names'"
            :investmentName="selectedObject"
            :template="true"
            :new="newObj"
            @disable-dialog="modifyDialog = !modifyDialog"
          />
          <InvestmentDetail
            v-if="templateType == 'Investments'"
            @add-investment="modifyDialog = !modifyDialog"
            :custom="false"
            :template="true"
            :investment="selectedObject"
            :investmentClassList="investmentClassList"
            :RPAANames="RPNameList"
            :investmentNames="nameList"
          />
          <AssetAllocationDetail
            v-if="templateType == 'Asset Allocation'"
            :investmentName="selectedObject"
            @disable-dialog="modifyDialog = !modifyDialog"
          />
          <AssetAllocationNameDetail
            :AAName="selectedObject"
            :template="true"
            :new="newObj"
            v-if="templateType == 'Asset Allocation Names'"
            @disable-dialog="modifyDialog = !modifyDialog"
          />
          <RiskProfileTable
            :RPGroupID="selectedObject.id"
            v-if="templateType == 'Risk Profiles'"
            @disable-dialog="modifyDialog = !modifyDialog"
          />
          <AFSLNameDetail
            v-if="templateType == 'AFSLs'"
            :new="newObj"
            :AFSLObj="selectedObject"
            @disable-dialog="modifyDialog = !modifyDialog"
          />
        </v-dialog>
      </v-col>
      <v-col :cols="2">
        <v-dialog v-model="addDialog">
          <template v-slot:activator="{ on }">
            <v-btn
              color="primary"
              v-on="on"
              v-if="(templateType != 'Platforms') && (templateType != 'Investments')">
              <v-icon>
                mdi-plus
              </v-icon>
            </v-btn>
          </template>
          <PlatformNameDetail
            v-if="templateType == 'Platform Names'"
            :platformName="selectedObject"
            :template="true"
            :new="newObj"
            @disable-dialog="addDialog = !addDialog"
          />
          <PlatformFeeNameDetail
            v-if="templateType == 'Platform Fees'"
            :platform="selectedName.platform_template"
            :template="true"
            :new="newObj"
            @disable-dialog="(addDialog = !addDialog)"
          />
          <AddPortfolioName
            v-if="templateType == 'Portfolios'"
            @add-portfolio="addDialog = !addDialog"
          />
          <InvestmentNameDetail
            v-if="templateType == 'Investment Names'"
            :investmentName="selectedObject"
            :new="newObj"
            :template="true"
            @disable-dialog="addDialog = !addDialog"
          />
          <AssetAllocationNameDetail
            :AAName="selectedObject"
            :template="true"
            :new="newObj"
            v-if="templateType == 'Asset Allocation Names'"
            @disable-dialog="addDialog = !addDialog"
          />
          <AddRPGroup
            v-if="templateType == 'Risk Profiles'"
            :template="true"
            :new="newObj"
            @add-rpgroup="addDialog = !addDialog"
          />
          <AFSLNameDetail
            v-if="templateType == 'AFSLs'"
            :AFSLObj="selectedObject"
            :new="newObj"
            @disable-dialog="addDialog = !addDialog"
          />
        </v-dialog>
      </v-col>
    </v-row>
  </v-card >
</template>

<script>
import { apiService } from "@/common/api.service";
import TemplatePlatformDetail from "@/components/templatemgmt/TemplatePlatformDetail.vue";
import PlatformNameDetail from "@/components/templatemgmt/PlatformNameDetail.vue";
import PlatformFeeSelector from "@/components/templatemgmt/PlatformFeeSelector.vue";
import PlatformFeeNameDetail from "@/components/templatemgmt/PlatformFeeNameDetail.vue";
import PortfolioTable from "@/components/PortfolioTable.vue";
import AddPortfolioName from "@/components/AddPortfolioName.vue";
import AssetAllocationNameDetail from "@/components/templatemgmt/AssetAllocationNameDetail.vue";
import AddRPGroup from "@/components/AddRPGroup.vue";
import RiskProfileTable from "@/components/RiskProfileTable.vue";
import AFSLNameDetail from "@/components/templatemgmt/AFSLNameDetail.vue";
import InvestmentDetail from "@/components/InvestmentDetail.vue";
import InvestmentNameDetail from "@/components/templatemgmt/InvestmentNameDetail.vue";
import AssetAllocationDetail from "@/components/templatemgmt/AssetAllocationDetail.vue";
import InvestmentFeeDetail from "@/components/templatemgmt/InvestmentFeeDetail.vue";


export default {
  name: "TemplateSelector",
  data() {
    return {
      platformFeeKey: 1,
      RPNameList: [],
      selectedName: {},
      selectedObject: {},
      selectedArray: [],
      modifyDialog: false,
      addDialog: false,
      newObj: true,
      investmentClassList: [],
      next: null,
    };
  },
  props: {
    templateType: {
      type: String,
      required: true
    },
    nameList: {
      type: Array,
      required: true
    },
  },
  components: {
    TemplatePlatformDetail,
    PlatformNameDetail,
    PlatformFeeSelector,
    PlatformFeeNameDetail,
    PortfolioTable,
    AddPortfolioName,
    AssetAllocationNameDetail,
    AddRPGroup,
    RiskProfileTable,
    AFSLNameDetail,
    InvestmentFeeDetail,
    InvestmentDetail,
    InvestmentNameDetail,
    AssetAllocationDetail,
  },
  watch: {
    addDialog() {
      if (this.templateType === "Platform Fees") {
        this.objectRouteSelector();
      }
    }
  },
  methods: {
    getItemText() {
      if (this.nameList.length > 0) {
        if (this.nameList[0].extended_name) {
          return "extended_name"
        } else {
          return "name"
        }
      }
    },

    clearSelected() {
      this.selectedObject = {};
      this.selectedName = {};
      this.selectedArray = [];
      this.newObj = true;
    },
    objectRouteSelector() {
      let endpoint = null;
      if (this.templateType == "Platforms") {
        endpoint = `/api/platformtemplates/${this.selectedName.platform_template}/`;
      } else if (this.templateType == "Investment Fees") {
        endpoint = `/api/platformtemplates/${this.selectedName.platform_template}/`;
      } else if (this.templateType == "Platform Names") {
        endpoint = `/api/platformnames/${this.selectedName.id}/`;
      } else if (this.templateType == "Platform Fees") {
        endpoint = `/api/platformtemplates/${this.selectedName.platform_template}/fees/`;
      } else if (this.templateType == "Portfolios") {
        endpoint = `/api/portfoliotemplates/${this.selectedName.id}/`;
      } else if (this.templateType == "Investments") {
        endpoint = `/api/investmenttemplate/${this.selectedName.linked_inv}/`;
      } else if (this.templateType == "Asset Allocation") {
        endpoint = `/api/investmentname/${this.selectedName.id}/`;
      } else if (this.templateType == "Investment Names") {
        endpoint = `/api/investmentname/${this.selectedName.id}/`;
      } else if (this.templateType == "Asset Allocation Names") {
        endpoint = `/api/aaname/${this.selectedName.id}/`
      } else if (this.templateType == "Risk Profiles"){
        endpoint = `/api/riskprofilegrouptemplates/${this.selectedName.id}/`;
      } else if (this.templateType == "AFSLs"){
        endpoint = `/api/afsls/${this.selectedName.id}/`;
      };

      if (endpoint != null) {
        this.getObjectData(endpoint);
      }
    },
    getObjectData(endpoint) {
      apiService(endpoint).then(data => {
        if (this.templateType != "Platform Fees") {
          this.selectedObject = data;
        } else {
          this.selectedArray = data.results;
        }
        this.newObj = false;
      });
    },
    getInvestmentClassList() {
      if ((this.templateType === "Investments") || (this.templateType === 'Platform Fees')) {
        let endpoint = `/api/investmentclass/`;
        apiService(endpoint, "GET").then(data => {
          this.investmentClassList = data.results;
        });
      }
    },
    getRPNameData() {
      if (this.templateType === "Investments") {
        let endpoint = `/api/activeriskprofilenames/`;
        apiService(endpoint).then(data => {
          this.RPNameList = data.results;
        });
      }
    },
  },
  mounted() {
    // this.nameRouteSelector();
    this.getInvestmentClassList();
    this.getRPNameData();
  }
};
</script>
