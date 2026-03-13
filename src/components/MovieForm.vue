<template>
  <div>
    <!-- Success message -->
    <div v-if="successMessage" class="alert alert-success">
      {{ successMessage }}
    </div>

    <!-- Error messages -->
    <div v-if="errors.length > 0" class="alert alert-danger">
      <ul>
        <li v-for="(error, index) in errors" :key="index">
          {{ error }}
        </li>
      </ul>
    </div>

    <form
      id="movieForm"
      @submit.prevent="saveMovie"
      enctype="multipart/form-data"
    >
      <div class="form-group mb-3">
        <label for="title" class="form-label">Movie Title</label>
        <input type="text" name="title" class="form-control" id="title" />
      </div>
      <div class="form-group mb-3">
        <label for="description" class="form-label">Description</label>
        <textarea
          name="description"
          class="form-control"
          id="description"
          rows="3"
        ></textarea>
      </div>
      <div class="form-group mb-3">
        <label for="poster" class="form-label">Poster</label>
        <input
          type="file"
          name="poster"
          class="form-control"
          id="poster"
          accept="image/*"
        />
      </div>
      <button type="submit" class="btn btn-primary">Submit</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

let csrf_token = ref("");
let successMessage = ref("");
let errors = ref([]);

function getCsrfToken() {
  fetch("/api/v1/csrf-token")
    .then((response) => response.json())
    .then((data) => {
      csrf_token.value = data.csrf_token;
    })
    .catch((err) => console.error("Failed to get CSRF token", err));
}

onMounted(() => {
  getCsrfToken();
});

function saveMovie() {
  // Clear previous messages
  successMessage.value = "";
  errors.value = [];

  const form = document.getElementById("movieForm");
  const formData = new FormData(form);

  fetch("/api/v1/movies", {
    method: "POST",
    body: formData,
    headers: {
      "X-CSRFToken": csrf_token.value,
    },
  })
    .then(async (response) => {
      const data = await response.json();
      if (response.ok) {
        // Success (201)
        successMessage.value = data.message || "Movie added successfully!";
        // Reset form fields
        form.reset();
      } else {
        // Validation errors (400)
        if (data.errors && Array.isArray(data.errors)) {
          errors.value = data.errors;
        } else {
          errors.value = ["An unknown error occurred."];
        }
      }
    })
    .catch((error) => {
      console.error("Network error:", error);
      errors.value = ["Network error. Could not reach the server."];
    });
}
</script>

<style scoped>
.alert {
  margin-bottom: 1rem;
  padding: 0.75rem 1.25rem;
  border-radius: 0.25rem;
}
.alert-success {
  color: #155724;
  background-color: #d4edda;
  border: 1px solid #c3e6cb;
}
.alert-danger {
  color: #721c24;
  background-color: #f8d7da;
  border: 1px solid #f5c6cb;
}
</style>
