
<template>
    <v-app style="background: #ffffff">
      <link rel="preconnect" href="https://fonts.gstatic.com">
      <link href="https://fonts.googleapis.com/css?family=Poppins:100,300,400,500,700,900" rel="stylesheet">
      <template v-if="accessTokenIsValid && proceed">
        <Navbar/>
          <v-container style="width: 1012px; height: 100%" class="pa-0">
              <router-view
                :key="$route.fullPath"
                />
          </v-container>

        </template>
        <template v-else-if="proceed || isLoginView">
          <router-view
            :key="$route.fullPath"
            />
        </template>
    </v-app>
</template>

<script type="text/javascript">
import Navbar from "@/components/Navbar.vue"
import { mapGetters } from "vuex";
import {
  USER_FETCH,
  REFRESH_ACCESS_TOKEN,
  USER_LOGOUT,
} from "@/store/actions.type";
import Chart from 'chart.js';
// import * as Adblock from "@/assets/js/prebid-ads.js";

Chart.defaults.global.defaultFontFamily = "Poppins";

  export default {
    name: "App",
    data() {
      return {
        proceed: false,
        allowedRoutes: [
          "login",
          "verify",
          "resetPassword",
          "rego",
          "verifyReset",
        ]
      }
    },
    components: {
      Navbar
    },
    head: {
      script: [
        { type: 'text/javascript', src: require("@/assets/js/prebid-ads.js"), async: true, body: true}, // Insert in body
      ]
    },
    computed: {
      ...mapGetters(["activeUser", "refreshToken", "accessTokenIsValid", "refreshTokenIsValid"]),
      isLoginView() {
        return this.$route.name === 'login'
      }
    },
    // watch: {
    //   activeUser () {
    //     this.setUserInfo();
    //   },
    // },
    methods: {
      setUserInfo() {
        if (this.accessTokenIsValid && this.refreshTokenIsValid) {
          if (this._.isEmpty(this.activeUser)) {
            this.$store.dispatch(USER_FETCH).then(() => {
              this.proceed = true;
            })
          } else {
            this.proceed = true;
          }
        } else {
          if (this.refreshTokenIsValid) {
            this.$store.dispatch(REFRESH_ACCESS_TOKEN).then(() => {
              this.$store.dispatch(USER_FETCH).then(() => {
                this.proceed = true;
              })
            })
          } else if (this.refreshToken) {
            this.$store.dispatch(USER_LOGOUT)
            this.proceed = true;
          } else if (this.allowedRoutes.includes(this.$route.name)){
            this.proceed = true;
          } else {
            this.$router.push({ name: 'login' });
            this.proceed = true;
          }
        }
      },
      checkAdBlocker() {
        // this.$loadScript(require("@/assets/js/prebid-ads.js")).then(() => {
          if (window.canRunAds === undefined){
          // adblocker detected, show fallback
            console.log("adblocker detected");
          } else {
            console.log("adblocker disabled");
          }
        // })
      }
    },
    mounted() {
      this.setUserInfo();
      this.checkAdBlocker();
    }
  }
</script>
