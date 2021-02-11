export default {
  methods: {
    $mergeAAAllocations (AANames, AASummary, prop) {
      let result = []
      for (const AAName of AANames) {
        // finds all items in the aa set that match the custom rp aa name
        const filterArr = AASummary.filter(
          x => x.custom_name === AAName)
        // creates an array with the found items
        const percentageArr = filterArr.map(a => a[prop]);
        if (!this._.isEmpty(percentageArr)) {
          // If the found item array has value, sums the items
          const percentageTotal = percentageArr.reduce((acc, curVal) =>
            Number(acc) + Number(curVal))
          result.push(percentageTotal);
        } else {
          // If no data is found, adds 0 to the array to maintain data order.
          result.push(0);
        }
      }
      return result;
    }
  }
}
