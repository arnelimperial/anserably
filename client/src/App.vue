<template>
  <div>
    <div id="nav" class="text-center pt-5">
      <router-link :to="{ name: 'home' }">Question List</router-link> |
      <router-link :to="{ name: 'ask' }">Ask Question</router-link> |
      <a href="#">Help</a>
    </div>
    <router-view />
  </div>
</template>

<script>
import { APIService } from "@/common/api.service.js";
//import NavbarComponent from "./components/common-components/Navbar.vue";
import axios from "axios";
export default {
  name: "Apps",

  methods: {
     async setUserInfo() {
      const data = await APIService('/api/users/');
      const requestUser = data['username'];
      window.localStorage.setItem('username', requestUser);
    
    },
    async setUserInfo(){
      const config = {
        method: 'get',
        url: 'http://127.0.0.1:8000/api/users/'
    }
    let res = await axios(config)
    let info = res.data.results;
    //let requestUser = info[0].email;
    let fname = info[0].first_name;
    let lname = info[0].last_name;
    let requestUser = fname + ' ' + lname
    //console.log('Current user:', email)
    localStorage.setItem('author', requestUser);
    localStorage.getItem('author')
    //console.info("User: ", localStorage.getItem('author'));
    },

  },
  created() {
    //this.setUserInfo()
    this.setUserInfo()

    
  }
  
};
</script>

<style>
  /* #app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;

  } */

  #nav a {
    font-weight: bold;
    font-size: 2vw;
    
  }

  #nav a.router-link-exact-active {
    color: #42b983;
  }
</style>
