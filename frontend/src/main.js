import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import vuetify from "./plugins/vuetify";
import VueLodash from 'vue-lodash'
import lodash from 'lodash'
import VCurrencyField from 'v-currency-field'
import { VTextField } from 'vuetify/lib'  //Globally import VTextField
import axios from 'axios'
import VueAxios from 'vue-axios'
import LoadScript from 'vue-plugin-load-script';
import './assets/css/main.css';


Vue.config.productionTip = false;

Vue.filter("toCurrency", function(value) {
  if (typeof value !== "number") {
    return value;
  }
  var formatter = new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    minimumFractionDigits: 0
  });
  return formatter.format(value);
});

Vue.filter("toCurrency2DP", function(value) {
  if (typeof value !== "number") {
    return value;
  }
  var formatter = new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    minimumFractionDigits: 2
  });
  return formatter.format(value);
});

Vue.filter("toPercentage", function(value) {
  if (typeof value !== "number") {
    return value;
  }
  var formatter = new Intl.NumberFormat("en-US", {
    style: "percent",
    minimumFractionDigits: 2
  });
  return formatter.format(value);
});


Vue.component('v-text-field', VTextField)
Vue.use(VCurrencyField, {
	locale: 'en-US',
	decimalLength: 2,
	autoDecimalMode: false,
	min: 0,
	max: null,
	defaultValue: 0,
})

Vue.use(VueAxios, axios)

Vue.use(LoadScript);
Vue.use(VueLodash, { name: 'custom' , lodash: lodash })

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount("#app");
