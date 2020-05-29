<template>
  <div class="single-question">
    <div class="container" v-if="question">
      <h2>{{ question.content }}</h2>
      <div v-if="showEditQuestion">
        <!-- <router-link
          :to="{ name: 'update-question', params: { slug: question.slug }}"
          class="btn btn-sm btn-outline-secondary mr-1"
        >Edit</router-link>-->
        <button
          onclick="document.getElementById('id01').style.display='block'"
          class="btn btn-sm btn-outline-secondary mr-1"
        >Update Question</button>

        <div id="id01" class="w3-modal mt-5 bg-dark">
          <div class="w3-modal-content w3-animate-opacity w3-card-4">
            <header class="container bg-light py-2">
              <span
                onclick="document.getElementById('id01').style.display='none'"
                class="w3-button w3-display-topright"
              >&times;</span>
              <h6>
                Update:
                <span class="w3-text-red">{{ question.content }}</span>
              </h6>
            </header>
            <div class="container my-3">
              <form @submit.prevent="submitUpdatedQuestion">
                <textarea
                  v-model="questionBody"
                  class="form-control mb-4"
                  rows="3"
                  placeholder="Update here..."
                ></textarea>
                <button type="submit" class="btn btn-success mb-3">Submit update</button>
              </form>
            </div>
          </div>
        </div>
        <button class="btn btn-sm btn-outline-danger my-2" @click="deleteQuestion">Delete Question</button>
      </div>

      <p class="mb-0">
        Posted by:
        <span class="w3-text-red">{{ question.author }}</span>
      </p>
      <p class="text-secondary">{{ question.created }}</p>
      <hr />
      <div v-if="userHasAnswered">
        <p class="answer-added">You've written an answer!</p>
      </div>
      <div v-else-if="showForm">
        <form class="card" @submit.prevent="onSubmit">
          <div class="card-header px-3">Answer thje question</div>
          <div class="card-block">
            <textarea
              v-model="newAnswerBody"
              class="form-control"
              placeholder="Share your knowledge"
              rows="5"
            ></textarea>
          </div>
          <div class="card-footer px-3">
            <button class="btn btn-sm btn-success">Submit your answer</button>
          </div>
        </form>
        <p v-if="error" class="text-danger mt-2">{{ error }}</p>
      </div>
      <div v-else>
        <button class="btn bt-sm btn-success" @click="showForm = true">Answer the question</button>
      </div>
      <hr />
    </div>
    <div v-else>
      <h2 class="w3-text-red">404 - Not Found</h2>

    </div>

    <div class="container" v-if="question">
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
import QuestionActions from "@/components/common-components/QuestionActions.vue";
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
    QuestionActions,
    PreventUnload
  },
  data() {
    return {
      question: {},
      answers: [],
      newAnswerBody: [],
      error: null,
      userHasAnswered: false,
      showForm: false,
      next: null,
      loadingAnswers: false,
      hasChanges: true,
      requestUser: null,
      showEditQuestion: false,
      questionSlug: null,
      questionBody: null
    };
  },

  methods: {
    setRequestUser() {
      // the username has been set to localStorage by the App.vue component
      this.requestUser = localStorage.getItem("author");
    },
    setPageTitle(title) {
      document.title = title;
    },
    getQuestionData() {
      let endpoint = `/api/questions/${this.slug}/`;
      APIService(endpoint).then(data => {
        if(data) {
          this.question = data;
          this.userHasAnswered = data.user_has_answered;
          this.setPageTitle(data.content);

        }else {
          this.question = null;
          this.setPageTitle("404 Error");
        }
        
      });
    },
    getQuestionAnswers() {
      let endpoint = `/api/questions/${this.slug}/answers/`;
      if (this.next) {
        endpoint = this.next;
      }
      this.loadingAnswers = true;
      APIService(endpoint).then(data => {
        this.answers.push(...data.results);
        this.loadingAnswers = false;
        if (data.next) {
          this.next = data.next;
        } else {
          this.next = null;
        }
      });
    },

    async deleteAnswer(answer) {
      let endpoint = `/api/answers/${answer.id}/`;
      try {
        await APIService(endpoint, "DELETE");
        this.$delete(this.answers, this.answers.indexOf(answer));
        this.userHasAnswered = false;
      } catch (err) {
        console.log(err);
      }
    },
    async isQuestionAuthor() {
      let resp = await axios.get("http://127.0.0.1:8000/api/questions/");
      let q_obj = resp.data.results;
      let current_user = localStorage.getItem("author");
      let result = q_obj.filter(obj => {
        return obj.author === current_user;
      });
      if (this.question.author === current_user) {
        this.showEditQuestion = true;
      }
    },
    async deleteQuestion() {
      let endpoint = `/api/questions/${this.slug}`;
      try {
        await APIService(endpoint, "DELETE");
        this.$router.push("/core");
      } catch (err) {
        console.log(err);
      }
    },

    onSubmit() {
      if (this.newAnswerBody) {
        let endpoint = `/api/questions/${this.slug}/answer/`;
        APIService(endpoint, "POST", { body: this.newAnswerBody }).then(
          data => {
            this.answers.unshift(data);
            this.showForm = false;
            this.userHasAnswered = true;
            if (this.error) {
              this.error = null;
            }
          }
        );
        this.newAnswerBody = null;
      } else {
        this.error = "You cannot send an empty answer!";
      }
    },
    submitUpdatedQuestion() {
      if (this.questionBody) {
        let endpoint = `/api/questions/${this.slug}/`;
        APIService(endpoint, "PUT", { content: this.questionBody }).then(() => {
          this.$router.push({
            name: "home",
            params: { slug: this.questionSlug }
          });
        });
      } else {
        this.error = "Required field!";
      }
    },
    async beforeRouteEnter(to, from, next) {
      // get the answer's data from the REST API and set two data properties for the component
      let endpoint = `/api/questions/${to.params.slug}/`;
      let data = await APIService(endpoint);
      return next(vm => (vm.questionBody = data.content));
    }
  },
  created() {
    this.getQuestionData();
    this.getQuestionAnswers();
    this.setRequestUser();
    this.isQuestionAuthor();
    //this.deleteQuestion()
  }
};
</script>
 

<style scoped>
.single-question {
  margin: 100px 30px;
}

.answer-added {
  font-weight: bold;
  color: green;
}
.error {
  font-weight: bold;
  color: red;
}
</style>