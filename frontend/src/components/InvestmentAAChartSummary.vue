<template lang="html">
  <v-container class="pa-3">
      <AABarChart
        v-if="chartData != null"
        :chartData="chartData"
        :options="chartOptions"
        :height="220"
        ref="AABarChart"
        :key="AAKey"
      >
    </AABarChart>
  </v-container>
</template>

<script>
import AABarChart from "@/components/AABarChart.vue";
import MergeAAAllocations from "@/components/mixins/MergeAAAllocations.js"

export default {
  name: "InvestmentAAChartSummary",
  mixins: [MergeAAAllocations],
  props: {
    RPAANames: {
      type: Array,
      required: false
    },
    aaSummary: {
      type: Array,
      required: false
    },
  },
  data() {
    return {
      AAKey:0,
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
              maxRotation: 0,
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
          display: false,
        },
      }
    };
  },
  components: {
    AABarChart
  },
  computed: {
    AAArray() {
      if (!this._.isEmpty(this.aaSummary)) {
        return this.$mergeAAAllocations(this.RPAANames, this.aaSummary, "aa_total_perc")
      } else {
        return []
      }
    },
    chartData(){
      return {
        labels: this.RPAANames,
        datasets: [
          {
            data: this.AAArray,
            backgroundColor: 'rgba(222, 72, 108)',
            borderColor: 'rgba(222, 72, 108)',
            borderWidth: 1,
            label: "Asset Allocation"
          },
        ]
      }
    },
  },
  watch: {
    aaSummary () {
      this.forceRerender();
    },
  },
  methods: {
    forceRerender(){
      this.AAKey += 1;
    },
  },
  mounted() {
  }
};
</script>
<style scoped>
  .v-select__selection {
    font-size: 12px !important;
  }
</style>
