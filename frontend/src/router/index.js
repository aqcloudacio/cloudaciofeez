import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";
import Scenario from "../views/Scenario.vue";
import Platform from "../views/Platform.vue";
import Output from "../views/Output.vue";
import Profile from "../views/Profile.vue";
import Templates from "../views/Templates.vue";
import Login from "../views/Login.vue";
import Rego from "../views/Rego.vue";
import Verify from "../views/Verify.vue";
import ResetPassword from "../views/ResetPassword.vue";
import VerifyReset from "../views/VerifyReset.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "",
    name: "home",
    component: Home
  },
  {
    path: "/login",
    name: "login",
    component: Login
  },
  {
    path: "/rego",
    name: "rego",
    component: Rego
  },
  {
    path: "/verify/:user/:token",
    name: "verify",
    component: Verify
  },
  {
    path: "/resetpassword",
    name: "resetPassword",
    component: ResetPassword
  },
  {
    path: "/verifyreset/:user/:token",
    name: "verifyReset",
    component: VerifyReset
  },
  {
    path: "/scenario/:id",
    name: "scenario",
    component: Scenario,
    props: true
  },
  {
    path: "/reports/:scenarioId",
    name: "reports",
    component: Output,
    props: true
  },
  {
    path: "/scenario/:scenarioId/:id",
    name: "platform",
    component: Platform,
    props(route) {
      // we keep the params.id Type from changing when entered from url
      let props = { ...route.params };
      props.id = parseInt(props.id);
      return props;
    }
  },
  {
    path: "/profile",
    name: "profile",
    component: Profile,
    props: true
  },
  {
    path: "/templates",
    name: "templates",
    component: Templates,
    props: true
  },
];

const router = new VueRouter({
  mode: "history",
  routes
});

export default router;
