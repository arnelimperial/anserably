import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";
import Question from "../views/Question.vue";
import Ask from "../views/Ask.vue";


Vue.use(VueRouter);

const routes = [
  {
    path: "/core",
    name: "home",
    component: Home
  },

  {
    path: "/question/:slug", 
    name: "question",
    component: Question,
    props: true
  },
  {
    path: "/ask/:slug?",
    name: "ask",
    component: Ask,
    props: true
  }
  

];

const router = new VueRouter({
  mode: "history",
  //base: process.env.BASE_URL,
  routes
});

export default router;
