<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top" id="mainNav">
      <div class="container">
      <!-- Bind Server and Client -->
        <a v-bind:href="about_link" class="navbar-brand js-scroll-trigger">Anserably</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarResponsive">
          <ul class="navbar-nav ml-auto">
            <li class="nav-item">
              <router-link :to="{ name: 'home' }" class="nav-link js-scroll-trigger">Question List</router-link>
            </li>
            <li class="nav-item">
              <router-link :to="{ name: 'ask' }" class="nav-link js-scroll-trigger">Ask Question</router-link>
            </li>
            <li class="nav-item" v-for="user in users" :key="user.pk">
              <div class="w3-dropdown-hover">
                <button class="w3-btn btn-primary">{{ user.email}}</button>
                <div class="w3-dropdown-content w3-bar-block w3-border">
                  <span class="w3-bar-item btn">Hi! {{ user.first_name }} {{ user.last_name }}</span>
                  <a v-bind:href="`/users/${user.username}/`" class="w3-bar-item btn">My Profile</a>
                  <a href="/accounts/logout/" class="w3-bar-item btn">Logout</a>
                </div>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </div>

</template>

<script>
import axios from "axios";
export default {
    name: 'NavbarComponent',
    data() {
      return {
        about_link: "http://127.0.0.1:8000/",
        users: []
      }
      
    },
    mounted() {
    axios.get("http://127.0.0.1:8000/api/users/")
      .then(response => (this.users = response.data.results))
      .catch(err => {
        
      })
    }
}
</script>

<style scoped>
  
</style>




