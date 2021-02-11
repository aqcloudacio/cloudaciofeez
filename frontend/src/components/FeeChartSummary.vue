<template lang="html">
  <v-card v-if="chartData != null" class="rounded-card no-box-shadow-thin-border">
    <v-container  height="200px" >
      <FeeBarChart
        :chartData="chartData"
        :options="chartOptions"
        :height="200"
      >
      </FeeBarChart>
    </v-container>
  </v-card>
</template>

<script>
import FeeBarChart from "@/components/FeeBarChart.vue";

export default {
  name: "FeeChartSummary",
  props: {
    currentPlatforms: {
      type: Array,
      required: false
    },
    recommendedPlatforms: {
      type: Array,
      required: false
    },
    alternativePlatforms: {
      type: Array,
      required: false
    },
  },
  data() {
    return {
      error: null,
      chartOptions: {
        cornerRadius: 200,
        scaleShowVerticalLines: false,
        responsive:true,
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
                    return value.toLocaleString('en-US', {style:'currency', currency:'USD',minimumFractionDigits: 0})
                  }
                }
            }],
            xAxes: [{
              gridLines: {
                display: false,
              },
              ticks: {
                fontColor: 'rgba(77,77,80)',
                maxRotation: 0 // angle in degrees
              }
            }],
        },
        legend:{
          display:false
        },
        title: {
          display: true,
          text: "Total Fees",
        },
        tooltips: {
          callbacks: {
            title: function() {
              return null
            },
            label: function(tooltipItem) {
              let value = tooltipItem.yLabel;
              return value.toLocaleString('en-US', {style:'currency', currency:'USD',minimumFractionDigits: 2});
            }
          }
        }
      }
    };
  },
  components: {
    FeeBarChart
  },
  computed: {
    feeArray() {
      let currentFees = this.currentPlatforms.reduce(function(prev, cur) {
        return prev + cur.platform_total_fees;
      }, 0);
      let recommendedFees = this.recommendedPlatforms.reduce(function(prev, cur) {
        return prev + cur.platform_total_fees;
      }, 0);
      let alternativeFees = this.alternativePlatforms.reduce(function(prev, cur) {
        return prev + cur.platform_total_fees;
      }, 0);
      return [currentFees, recommendedFees, alternativeFees];
    },
    chartData(){
      return {
        labels: ["CUR", "REC", "ALT"],
        datasets: [{
          pointStyle: 'rectRounded',
          data: this.feeArray,
          backgroundColor: [
            'rgba(222, 72, 108)',
            'rgba(68,136,220)',
            'rgba(238,205,75)',
          ],
          borderColor: [
            'rgba(222, 72, 108)',
            'rgba(68,136,220)',
            'rgba(238,205,75)',
          ],
          borderWidth: 1,
          borderRadius:true,
        }]
      }
    },
  },
  methods: {
  },
  mounted() {
    // this.buildChartData();
  }
};
</script>
