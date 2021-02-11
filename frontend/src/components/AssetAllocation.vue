<template lang="html">
  <div>
    <v-card v-for="(value, key) in aaObj" :key="key">
      <v-card-text>
        {{key}}: {{(value / groupingTotal) | toPercentage}}
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
export default {
  name: "AssetAllocation",
  props: {
    aaData: {
      type: Array,
      required: true
    },
    groupingTotal: {
      type: Number,
      required: true
    }
  },
  computed: {
    aaObj: function (){
      var aaObject = {};
      for (let i = 0; i < this.aaData.length; i++) {
        let found = false;
          for (let x = 0; x < this.aaData[i].rp_aa_name.length; x++) {
            let aaName = this.aaData[i].rp_aa_name[x];
            if (aaName in aaObject) {
              aaObject[aaName] += this.aaData[i].rp_aa_dollar;
              found = true;
              break;
            }

            if (!found) {
              let key = this.aaData[i].rp_aa_name[x];
              let value = this.aaData[i].rp_aa_dollar;
              aaObject[key]= value;
              found = false;
            }
        }
      }
      return (aaObject)
    }
  },
};
</script>
