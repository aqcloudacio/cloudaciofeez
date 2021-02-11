import VCurrencyField from './VCurrencyField.vue';
import options from './options';

const version = '__VERSION__'

export {
  VCurrencyField,
  options,
  version,
};

function install(Vue, globalOptions) {
  if (globalOptions) {
    Object.keys(globalOptions).map((key) => {
      options[key] = globalOptions[key];
    });
  }

  Vue.component('v-currency-field', VCurrencyField);
}

export default install;

// Install by default if included from script tag
if (typeof window !== 'undefined' && window.Vue) {
  window.Vue.use(install);
}
