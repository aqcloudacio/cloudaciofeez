<template lang="html">
  <v-container >
  <v-form @submit.prevent="onSubmit">
    <v-card class="pa-2">
      <v-row>
        <v-col>
          <v-select
            dense solo hide-details
            :items="platformFees"
            :return-object="true"
            item-text="description"
            v-model="platformFee"
            label="Select Fee"
          />
        </v-col>

      </v-row>
      <template
       v-if="platformFee != null">
        <PlatformFeeSummary
          :key="platformFee.id"
          v-if="!_.isEmpty(platformFee)"
          :platform="platform"
          :platformFee="platformFee"
          :template="template"
          :investmentClassList="investmentClassList"
          v-on="$listeners"
        />
      </template>
    </v-card>
  </v-form>
</v-container>
</template>

<script>
import PlatformFeeSummary from "@/components/PlatformFeeSummary.vue";

export default {
  name: "PlatformFeeSelector",

  props: {
    platformFees: {
      type: Array,
      required: true,
    },
    platform: {
      type: Number,
      required: false,
    },
    template: {
      type: Boolean,
      required: false,
    },
    investmentClassList: {
      type: Array,
      required: false,
    },
  },
  data() {
    return {
      platformFee: null,
    };
  },
  watch: {
    platformFees() {
      this.platformFee = null;
    }
  },
  components: {
    PlatformFeeSummary
  },
  methods: {
    onSubmit() {
      //pass
    }
  }
};
</script>
