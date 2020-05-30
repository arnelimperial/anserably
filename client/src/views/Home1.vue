<template>
  <div class="home text-primary">
    <div class="container mt-2">
      <div v-for="question in questions" :key="question.id">
        <p class="mb-0">Posted by:
          <span class="text-info">{{ question.author }}</span>
        </p>
        <p>
          
            {{ question.content }}
          
        </p>
        <p class="w3-text-indigo">Posted Date: {{ question.created }}</p>
        <hr>
      </div>
    </div>
         
  </div>
</template>
     
<script>
import axios from "axios";
  export default {
    name: "Home",

    data() {
      return {
        questions: [],
        errors: []
      };
    },
    mounted() {
        axios.get("http://127.0.0.1:8000/api/questions/")
        .then(response => (this.questions = response.data.results))
        .catch(err => {

        })
      }
    
  };
</script>