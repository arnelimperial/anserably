<template>
  <div id="app">
    <NavbarComponent />
    <router-view />
  </div>
</template>

<script>
import { APIService } from "@/common/api.service.js";
import NavbarComponent from "./components/common-components/Navbar.vue";
import axios from "axios";
export default {
  name: "App",
  components: {
    NavbarComponent
  },
  methods: {
    //  async setUserInfo() {
    //   const data = await APIService('/api/users/');
    //   const requestUser = data['username'];
    //   window.localStorage.setItem('username', requestUser);
    
    // },
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
  
}
</script>

<style>
 
 
</style>
