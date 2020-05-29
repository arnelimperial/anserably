<template>
  <div class="single-answer">
    <p class="text-muted">
      <strong>{{ answer.author }}</strong>
      &#8901; {{ answer.created }}
    </p>
    <p>{{ answer.body }}</p>
    <div v-if="isAnswerAuthor">
      <router-link 
        :to="{ name: 'answer-editor', params: { id: answer.id }}"
        class="btn btn-sm btn-outline-secondary mr-1"
      >Edit</router-link>
      <button class="btn btn-sm btn-outline-danger" @click="triggerDeleteAnswer">Delete</button>
    </div>
    <div v-else>
      <button 
        class="btn btn-sm"
        @click="toggleLike"
        :class="{
          'btn-info': userLikedAnswer,
          'btn-outline-secondary': !userLikedAnswer,
        }"
      
      >
      <strong><i class="fas fa-thumbs-up"></i>[{{ likesCounter }}]</strong>
      </button>
      <span class="text-muted ml-3">{{ msg }}</span>

    </div>
    <hr />
  </div>
</template>

<script>
import axios from "axios";
import { APIService } from "@/common/api.service.js";
export default {
  name: "AnswerComponent",
  props: {
    answer: {
      type: Object,
      required: true
    },
    // requestUser: {
    //   type: String,
    //   required: true
    // }
  },
  data() {
    return {
      userLikedAnswer: this.answer.user_has_voted,
      likesCounter: this.answer.likes_count,
      msg: ''
    }

  },

  computed: {
    isAnswerAuthor() {
      // return true if the logged in user is also the author of the answer instance
      let answer_obj = this.answer;
      let auth_author_of_answer = Object.values(answer_obj).includes(localStorage.getItem('author'));
      return auth_author_of_answer;
      
    }

  },
  methods: {
    triggerDeleteAnswer() {
      this.$emit("delete-answer", this.answer);
    },
    toggleLike(){
      this.userLikedAnswer === false 
        ? this.likeAnswer()
        : this.unLikeAnswer()
    },
    likeAnswer(){
      this.userLikedAnswer = true;
      this.likesCounter += 1;
      let endpoint = `/api/answers/${ this.answer.id}/like/`;
      this.msg = 'You like it!'
      APIService(endpoint, 'POST');


    },
    unLikeAnswer(){
      this.userLikedAnswer = false;
      this.likesCounter -= 1;
      let endpoint = `/api/answers/${ this.answer.id}/like/`;
      this.msg = 'You dislike it!'
      APIService(endpoint, 'DELETE');

    }
  }
};
</script>

<style>
</style>