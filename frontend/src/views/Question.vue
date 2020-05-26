<template>
  <div class="single-question">
    <div class="container">
      <h2>{{ question.content }}</h2>
      <p class="mb-0">Posted by: 
        <span class="w3-text-red">{{ question.author }}</span>
      </p>
      <p class="text-secondary">{{ question.created }}</p>
      <hr>
      <div v-if="userHasAnswered">
        <p class="answer-added">You've written an answer!</p>
      </div>
      <div v-else-if="showForm">
        <form class="card" @submit.prevent="onSubmit">
          <div class="card-header px-3">Answer thje question</div>
          <div class="card-block">
            <textarea v-model="newAnswerBody" class="form-control" placeholder="Share your knowledge" rows="5"></textarea>
          </div>
          <div class="card-footer px-3">
            <button class="btn btn-sm btn-success">Submit your answer</button>

          </div>
        </form>
        <p v-if="error" class="text-danger mt-2">{{ error }}</p>
      </div>
      <div v-else>
        <button class="btn bt-sm btn-success" @click="showForm = true">
          Answer the question
        </button>
      </div>
      <hr>
    </div>
   
    <div class="container">
      <AnswerComponent
        v-for="answer in answers"
        :answer="answer"
        :key="answer.id"
        :requestUser="requestUser"
        @delete-answer="deleteAnswer"
      />
      <div class="my-4">
        <p v-show="loadingAnswers">...load...</p>
          <button 
            v-show="next"
            @click="getQuestionAnswers"
            class="btn btn-sm btn-outline-success"
            >Load more...</button>
      </div>
      
    </div>
    
    
    <PreventUnload :when="hasChanges"/>
   
   
  </div>
 
  
</template>

<script>
import { APIService } from "../common/api.service.js";
import PreventUnload from 'vue-prevent-unload';
import AnswerComponent from "@/components/common-components/Answer.vue";
import axios from "axios";
export default {

  name: "Question",
  props: {
    slug: {
      type: String,
      required: true
    }
  },
  components: {
    AnswerComponent,
    PreventUnload
  },
  data() {
    return {
      question: {},
      answers: [],
      newAnswerBody: [],
      error: null,
      userHasAnswered: false,
      showForm:false,
      next: null,
      loadingAnswers: false,
      hasChanges: true,
      requestUser: null
    }
  },

  methods: {
     setRequestUser() {
      // the username has been set to localStorage by the App.vue component
      this.requestUser = window.localStorage.getItem("email");
    },
    setPageTitle(title) {
      document.title = title;

    },
    getQuestionData() {
      let endpoint = `/api/questions/${this.slug}/`;
      APIService(endpoint)
        .then(data => {
          this.question = data;
          this.userHasAnswered = data.user_has_answered;
          this.setPageTitle(data.content)
        })
    },
    getQuestionAnswers() {
      let endpoint = `/api/questions/${this.slug}/answers/`;
      if (this.next) {
        endpoint = this.next;
      }
      this.loadingAnswers = true;
      APIService(endpoint)
        .then(data => {
          this.answers.push(...data.results);
          this.loadingAnswers = false;
          if (data.next) {
            this.next = data.next;
          } else {
            this.next = null;
          }
        })
    },
    onSubmit() {
      if(this.newAnswerBody) {
        let endpoint = `/api/questions/${this.slug}/answer/`;
        APIService(endpoint, "POST", { body: this.newAnswerBody })
        .then(data => {
          this.answers.unshift(data)
          this.showForm = false;
          this.userHasAnswered = true;
          if(this.error) {
            this.error = null;
          }
        })
        this.newAnswerBody = null;
      }else {
        this.error = "You cannot send an empty answer!"
      }
    },
    async deleteAnswer(answer) {
      let endpoint = `/api/answers/${answer.id}/`;
      try {
        await APIService(endpoint, "DELETE");
        this.$delete(this.answers, this.answers.indexOf(answer));
        this.userHasAnswered = false;
      }catch(err){
        console.log(err)
      }
    }
    
  },
  created() {
    this.getQuestionData()
    this.getQuestionAnswers()
    this.setRequestUser()

  }
 
}
</script>
 

<style scoped>
  .single-question {
    margin: 100px 30px;
  }

  .answer-added{
    font-weight: bold;
    color: green;
  }
  .error {
    font-weight: bold;
    color: red;
  }

</style>