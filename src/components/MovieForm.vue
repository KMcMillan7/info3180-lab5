<template>
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
</template>

<script setup>
import { ref, onMounted } from "vue";

let csrf_token = ref("");

// Fetch CSRF token when component mounts
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
  let movieform = document.getElementById("movieForm");
  let form_Data = new FormData(movieform);

  fetch("/api/v1/movies", {
    method: "POST",
    body: form_Data,
    headers: {
      "X-CSRFToken": csrf_token.value,
    },
  })
    .then((response) => response.json())
    .then((data) => {
      // For now just log; later we'll show messages
      console.log("Success:", data);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}
</script>
