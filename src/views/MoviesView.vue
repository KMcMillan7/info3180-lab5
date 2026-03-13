<template>
  <div class="container mt-4">
    <h1>Movies</h1>
    <div v-if="movies.length === 0" class="no-movies">
      <p>
        No movies added yet.
        <router-link to="/movies/create">Add one!</router-link>
      </p>
    </div>
    <div class="row">
      <div class="movie-card" v-for="movie in movies" :key="movie.id">
        <img :src="movie.poster" class="movie-poster" alt="Movie title" />
        <div class="movie-info">
          <h5 class="movie-title">{{ movie.title }}</h5>
          <p class="movie-description">{{ movie.description }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

let movies = ref([]);

function fetchMovies() {
  fetch("/api/v1/movies")
    .then((response) => response.json())
    .then((data) => {
      movies.value = data.movies;
    })
    .catch((error) => {
      console.error("Error fetching movies:", error);
    });
}

onMounted(() => {
  fetchMovies();
});
</script>
<style scoped>
.page-title {
  font-size: 2rem;
  margin-bottom: 1.5rem;
}

.no-movies {
  text-align: center;
  color: #6c757d;
  margin-top: 3rem;
}

.movies-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
}

.movie-card {
  display: flex;
  gap: 1rem;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 1rem;
  background: #fff;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
  transition: box-shadow 0.2s;
}

.movie-card:hover {
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.12);
}

.movie-poster {
  width: 100px;
  height: 140px;
  object-fit: cover;
  border-radius: 4px;
  flex-shrink: 0;
}

.movie-info {
  flex: 1;
}

.movie-title {
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0 0 0.5rem 0;
}

.movie-description {
  font-size: 0.9rem;
  color: #495057;
  line-height: 1.5;
  margin: 0;
}
</style>
