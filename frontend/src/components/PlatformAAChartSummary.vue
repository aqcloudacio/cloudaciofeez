<template lang="html">
  <v-card v-if="chartData != null" class="rounded-card no-box-shadow-thin-border">
    <v-container height="150px">
      <AABarChart
        :chartData="chartData"
        :options="chartOptions"
        :height="200"
        ref="AABarChart"
      >
    </AABarChart>
    </v-container>

  </v-card>
</template>

<script>
import AABarChart from "@/components/AABarChart.vue";
import { mapGetters } from "vuex";

import MergeRPAllocations from "@/components/mixins/MergeRPAllocations.js"
import MergeAAAllocations from "@/components/mixins/MergeAAAllocations.js"

export default {
  name: "PlatformAAChartSummary",
  mixins: [MergeRPAllocations, MergeAAAllocations],
  props: {
  },
  data() {
    return {
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
              maxRotation: 0 ,
              callback: function (value) {
                let matches = value.match(/\b(\w)/g);
                let acronym = matches.join('');
                return acronym
              }
            }
          }],
        },
        tooltips: {
          callbacks: {
            label: function(tooltipItem, data) {
              let label = data.datasets[tooltipItem.datasetIndex].label || '';
              if (label.length > 0) {
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
        // title: {
        //   display: true,
        //   text: "Asset Allocation",
        // },
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
  components: {
    AABarChart
  },
  computed: {
    ...mapGetters(["activeScenario", "activePlatform", "activePlatformAA"]),
    AANames() {
      let custom_names = this.activePlatformAA.map(a => a.custom_name);
      let aanames = [...new Set(custom_names)];
      return aanames
    },
    RPArray() {
      // finds any duplicate RP_AA_Names and merges their values
      if (!this._.isEmpty(this.activeScenario.risk_profile)) {
        return this.$mergeRPAllocations(this.AANames, this.activeScenario.risk_profile.allocations)

      } else {
        return []
      }
    },
    AAArray() {
      return this.$mergeAAAllocations(this.AANames, this.activePlatformAA,'aa_total_perc_platform')
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
            data: this.AAArray,
            backgroundColor: 'rgba(222, 72, 108)',
            borderColor: 'rgba(222, 72, 108)',
            borderWidth: 1,
            label: this.activePlatform.str_name.toUpperCase()
          }
        ]
      }
    },
  },
  methods: {
  },
  mounted() {
  }
};
</script>
