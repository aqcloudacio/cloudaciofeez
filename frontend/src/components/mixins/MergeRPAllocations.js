export default {
  methods: {
    $mergeRPAllocations (AANames, rpAllocations) {
      let result = []
      for (const AAName of AANames) {
        // finds all items in the risk profile that match the custom rp aa name
        const filterArr = rpAllocations.filter(
          x => x.name.custom_name === AAName)
        // creates an array with the found items
        const percentageArr = filterArr.map(a => a.percentage);
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
