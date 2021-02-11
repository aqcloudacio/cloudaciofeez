export const rule4Digits = {
  computed: {
    $rule4Digits() {
      return [v => {
        if (v) {
          v = v.toString()
          return (parseFloat(v.replace(/,/g, '')) < 10000 && parseFloat(v.replace(/,/g, '')) >= 0
            || 'Must be less than $10,000')
        } else {
          return true
        }
      }]
    }
  }
}

export const rule6Digits = {
  computed: {
    $rule6Digits() {
      return  [v => {
        if (v) {
          v = v.toString()
          return (parseFloat(v.replace(/,/g, '')) < 100000 && parseFloat(v.replace(/,/g, '')) >= 0
            || 'Must be less than $100,000')
        } else {
          return true
        }
      }]
    }
  }
}

export const rule7Digits = {
  computed: {
    $rule7Digits() {
      return  [v => {
        if (v) {
          v = v.toString()
          return (parseFloat(v.replace(/,/g, '')) < 1000000 && parseFloat(v.replace(/,/g, '')) >= 0
            || 'Must be less than $1,000,000')
        } else {
          return true
        }
      }]
    }
  }
}

export const ruleEmail = {
  computed: {
    $ruleEmail() {
      return [
        v => !!v || 'Email is required',
        v => /.+@.+\..+/.test(v) || 'Email must be valid',
        v => v ? !(v.includes("+")) : false || 'Email can not contain "+"'
      ]
    }
  }
}

export const rule8Digits = {
  computed: {
    $rule8Digits() {
      return  [v => {
        if (v) {
          v = v.toString()
          return (parseFloat(v.replace(/,/g, '')) < 10000000 && parseFloat(v.replace(/,/g, '')) >= 0
            || 'Must be less than $10,000,000')
        } else {
          return true
        }
      }]
    }
  }
}
export const rulePercentage = {
  computed: {
    $rulePercentage() {
      return [v => (v < 10) && (v >= 0) || 'Must be between 0% and 10%']
    }
  }
}

export const rulePercTo100 = {
  computed: {
    $rulePercTo100() {
      return [v => (v <= 100) && (v >= 0) || 'Must be between 0% and 100%']
    }
  }
}

export const ruleGTZero = {
  computed: {
    $ruleGTZero() {
      return  [v => {
        if (v) {
          v = v.toString()
          return (parseFloat(v.replace(/,/g, '')) > 0  || 'Must be greater than zero')
        } else {
          return true
        }
      }]
    }
  }
}

export const ruleMobile = {
  computed: {
    $ruleMobile() {
      return [
        v => !!v || 'This field is required',
        v => (v ? v.length > 10 : false) ? true : 'Phone number must be 10 digits',
      ]
    }
  }
}

export const rulePassword = {
  computed: {
    $rulePassword() {
      return [
        v => !!v || 'Password is required',
        v => (v ? v.length > 7 : false) ? true : 'Password must be at least 8 characters',
        v => /[A-Za-z]/i.test(v) || 'Password must contain a letter',
      ]
    }
  }
}

export const ruleRequired = {
  computed: {
    $ruleRequired() {
      return [v => !!v || 'This field is required']
    }
  }
}
