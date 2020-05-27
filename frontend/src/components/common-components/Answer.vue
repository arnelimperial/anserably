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
    <hr />
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "AnswerComponent",
  props: {
    answer: {
      type: Object,
      required: true
    },
    requestUser: {
      type: String,
      required: true
    }
  },

  computed: {
    isAnswerAuthor() {
      // return true if the logged in user is also the author of the answer instance
      let answer_obj = this.answer;
      let auth_author_of_answer = Object.values(answer_obj).includes(localStorage.getItem('author'));
      return auth_author_of_answer
      
    }

  },
  methods: {
    triggerDeleteAnswer() {
      this.$emit("delete-answer", this.answer);
    }
  }
};
</script>

<style>
</style>