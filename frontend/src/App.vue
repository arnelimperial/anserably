<template>
  <div id="app">
    <NavbarComponent />
    <router-view />
  </div>
</template>

<script>
import { APIService } from "@/common/api.service.js";
import NavbarComponent from "./components/common-components/Navbar.vue";
export default {
  name: "App",
  components: {
    NavbarComponent
  },
  methods: {
     async setUserInfo() {
       const data = await APIService('/api/users/');
       const requestUser = data.results['email'];
        window.localStorage.setItem('email', requestUser);
    
      }
  },
  created() {
    this.setUserInfo()
  }
  
};
</script>

<style>
 
 
</style>
