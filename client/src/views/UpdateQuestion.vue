<template>
  <div class="container pt-5">
    <h1 class="mb-3">Edit Your Question</h1>
    <form @submit.prevent="onSubmit">
      <textarea 
        v-model="questionBody" 
        class="form-control" 
        rows="3"
        ></textarea>
      <br />
      <button type="submit" class="btn btn-success">Update</button>
    </form>
    <p v-if="error" class="muted mt-2">{{ error }}</p>
  </div>
</template>

<script>
import { APIService } from "@/common/api.service.js";
export default {
  name: "UpdateQuestion",
  props: {
    slug: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      questionSlug: null,
      questionBody: null,
      error: null
    };
  },
  methods: {
    onSubmit() {
      if (this.questionBody) {
        let endpoint = `/api/questions/${this.slug}/`;
        APIService(endpoint, "PUT", { content: this.questionBody }).then(() => {
          this.$router.push({
            name: "question",
            params: { slug: this.questionSlug }
          });
        });
      } else {
        this.error = "Required field!";
      }
    }
  },
  async beforeRouteEnter(to, from, next) {
    // get the answer's data from the REST API and set two data properties for the component
    let endpoint = `/api/questions/${to.params.slug}/`;
    let data = await APIService(endpoint);
    return next(
      vm => (
        (vm.questionBody = data.content)
      )
    );
  }
};
</script>