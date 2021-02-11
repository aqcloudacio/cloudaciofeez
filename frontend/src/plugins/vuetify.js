import Vue from "vue";
import Vuetify from "vuetify/lib";

Vue.use(Vuetify);

const opts = {
  theme: {
    themes: {
      light: {
        primary: '#47b27a',
        primaryhalf: '#ecf7f1',
        secondary: '#38383b',
        accent: '#e35c38',
        PRgrey: '#dbdbdb',
        grey1: "#e4e7f0",
        grey2: "f1f3f7",
        grey3: "fdfbfb",
        // error: '#FF5252',
        // info: '#2196F3',
        // success: '#4CAF50',
        // warning: '#FFC107'
      },
    },
  },
}

export default new Vuetify(opts);
