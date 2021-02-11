<template lang="html">
  <v-card v-if="chartData != null" class="rounded-card no-box-shadow-thin-border">
    <!-- <link rel="preconnect" href="https://fonts.gstatic.com">
    <link href="https://fonts.googleapis.com/css2?family=Poppins&display=swap" rel="stylesheet"> -->
    <v-container height="200px">
      <AABarChart
        :chartData="chartData"
        :options="chartOptions"
        ref="AABarChart"
        :height="200"

      >
      </AABarChart>
    </v-container>
  </v-card>
</template>

<script>
import AABarChart from "@/components/AABarChart.vue";
import { apiService } from "@/common/api.service.js";
import { mapGetters } from "vuex";
import MergeRPAllocations from "@/components/mixins/MergeRPAllocations.js"
import MergeAAAllocations from "@/components/mixins/MergeAAAllocations.js"

export default {
  name: "ScenarioAAChartSummary",
  mixins: [MergeRPAllocations, MergeAAAllocations],
  props: {
    riskProfile: {
      type: Object,
      required: false
    },
  },
  data() {
    return {
      AASummary: [],
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            yAxes: [{
              gridLines: {
                drawBorder: false,
              },
              ticks: {
                fontColor: 'rgba(77,77,80)',
                // fontFamily: "'Poppins', sans-serif",
                beginAtZero: true,
                maxTicksLimit: 6,
                callback: function (value) {
                  return value.toLocaleString('en-US', {style:'percent'});
                }
              }
            }],
            xAxes: [{
                gridLines: {
                  display: false,
                },
                ticks: {
                  fontColor: 'rgba(77,77,80)',
                  maxRotation: 0,
                  callback: function (value) {
                    let matches = value.match(/\b(\w)/g);
                    let acronym = matches.join('');
                    return acronym
                  }
                },
            }],
          onHover: function(e) {
            e.target.style.cursor = 'pointer';
          },
        },
        tooltips: {
          callbacks: {
            label: function(tooltipItem, data) {
              let label = data.datasets[tooltipItem.datasetIndex].label || '';
              if (label.length > 0) {
                // label = this._.capitalize(label)
                label += ': ';
                label = label[0].toUpperCase() + label.slice(1).toLowerCase();
              }
              let val = tooltipItem.yLabel;
              val = val.toLocaleString('en-US', {style:'percent', minimumFractionDigits:2});
              label += val
              return label
            }
          }
        },
        title: {
          display: true,
          text: "Asset Allocation",

        },
        legend: {
          position: 'top',
          labels: {
            fontColor: 'PRgrey',
            fontSize: 10,
            usePointStyle: true,
          },
          onHover: function(e) {
            e.target.style.cursor = 'pointer';
          },
          onClick: function(e, legendItem) {
            var index = legendItem.datasetIndex;
            var ci = this.chart;
            var meta = ci.getDatasetMeta(index);

              if (meta.hidden == true) {
                meta.hidden = false
              } else {
                meta.hidden = true;
              }
            ci.update();
          }
        },
        hover: {
         onHover: function(e) {
            var point = this.getElementAtEvent(e);
            if (!point.length) e.target.style.cursor = 'default';
         }
       }
      }
    };
  },
  watch: {
    activeScenario() {
      this.getAASummary();
    },
  },
  components: {
    AABarChart
  },
  computed: {
    ...mapGetters(["activeScenario"]),
    RPArray() {
      if (!this._.isEmpty(this.riskProfile)) {
        return this.$mergeRPAllocations(this.AANames, this.activeScenario.risk_profile.allocations)
      } else {
        return []
      }
    },
    AANames() {
      let custom_names = this.AASummary.map(a => a.custom_name);
      let aanames = [...new Set(custom_names)];
      return aanames
    },
    currentAAArray() {
      return this.$mergeAAAllocations(this.AANames, this.AASummary,'cur_total_perc')
    },
    recommendedAAArray() {
      return this.$mergeAAAllocations(this.AANames, this.AASummary,'rec_total_perc')
    },
    alternativeAAArray() {
      return this.$mergeAAAllocations(this.AANames, this.AASummary,'alt_total_perc')
    },
    chartData(){
      return {
        labels: this.AANames,
        datasets: [
          {
            data: this.RPArray,
            backgroundColor: 'rgba(0,168,93)',
            borderColor: 'rgba(0,168,93)',
            borderWidth: 1,
            label: "RISK PROFILE"
          },
          {
            data: this.currentAAArray,
            backgroundColor: 'rgba(222, 72, 108)',
            borderColor: 'rgba(222, 72, 108)',
            borderWidth: 1,
            label: "CURRENT"
          },
          {
            data: this.recommendedAAArray,
            backgroundColor: 'rgba(68,136,220)',
            borderColor: 'rgba(68,136,220)',
            borderWidth: 1,
            label: "RECOMMENDED"
          },
          {
            data: this.alternativeAAArray,
            backgroundColor: 'rgba(238,205,75)',
            borderColor: 'rgba(238,205,75)',
            borderWidth: 1,
            label: "ALTERNATIVE",
          },
        ]
      }
    },
  },
  methods: {
    getAASummary() {
      if (!this._.isEmpty(this.activeScenario)) {
        let endpoint = `/api/scenarios/${this.activeScenario.id}/aasummary/`;
        apiService(endpoint).then(data => {
          this.AASummary = data.results;
        });
      }
    },
  },
  mounted() {
    this.getAASummary();
  }
};
</script>
<style media="screen">
.fontPreloader{
  font-family: 'Poppins';
  position: fixed;
  top: -9999px;
  left: -9999px;
}
</style>
