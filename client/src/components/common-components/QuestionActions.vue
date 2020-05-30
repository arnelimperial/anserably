<template>
  <div class="question-actions">
   
    <!-- <router-link
      :to="{ name: 'answer-editor', params: { id: answer.id }}"
      class="btn btn-sm btn-outline-secondary mr-1"
    >Edit</router-link> -->
    <button class="btn btn-sm btn-outline-danger" @click="deleteQuestion">Delete your question</button>
  </div>
</template>

<script>
import { APIService } from "@/common/api.service.js";
import axios from "axios";
export default {
  name: "QuestionActions",
  props: {
    slug: {
      type: String,
      required: true

    }
    
  },
  // computed:{
  //   async isQuestionAuthor() {
  //     let resp = await axios.get('http://127.0.0.1:8000/api/questions/');
  //     let q_obj = resp.data.results;
  //     let current_user = localStorage.getItem('author');
  //     //let auth_author_of_question = Object.values(q_obj).indexOf('Arnel Imperial') > -1;
  //     //let auth_author = q_obj.some(el => el);
  //     //console.log(auth_author);
  //     //return auth_author;
  //     let result = q_obj.filter(obj => {
  //       return obj.author === current_user;
  //     })
  //     return (result[0].author === current_user);
  //   }


  // },
  
  methods: {
    async deleteQuestion() {
      let endpoint = `/api/questions/${this.slug}`;
      try{
        await APIService(endpoint, 'DELETE');
        this.$router.push('/core');

      }catch(err){
        console.log(err);
      }
    },
    
  },
 
};
</script>

<style>
</style>