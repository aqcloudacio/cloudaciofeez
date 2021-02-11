<template lang="html">
  <v-container class="pa-0">
    <v-card-title class="pb-0 pt-0">
      Health Check
    </v-card-title>
    <v-card-text>
      Balances: {{balancesAligned}}<br>
    </v-card-text>
  </v-container>
</template>

<script>

export default {
  name: "Healthcheck",
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
      error: null
    };
  },
  computed: {
    balancesAligned() {
      let currentTotal = this.currentPlatforms.reduce(function(prev, cur) {
        return prev + cur.platform_total;
      }, 0);
      let recommendedTotal = this.recommendedPlatforms.reduce(function(prev, cur) {
        return prev + cur.platform_total;
      }, 0);
      let alternativeTotal = this.alternativePlatforms.reduce(function(prev, cur) {
        return prev + cur.platform_total;
      }, 0);
      let aligned = (alternativeTotal === currentTotal && alternativeTotal === recommendedTotal && alternativeTotal !== null)
      if (aligned ) {
        return "Aligned"
      } else {
        return "Not aligned"
      }
    }
  },
  methods: {
  }
};
</script>
