<template>
  <div class="container">
    <!-- <img src="../assets/logo.png"> -->
    <suggestionList />
  </div>
</template>

<script>
// @ is an alias to /src
import suggestionList from "../components/suggestion/SuggestionList";

export default {
  name: "index",
  components: {
    suggestionList
  }
};
</script>

<style>
.container {
  display: flex;
  flex-flow: row wrap;
  flex-direction: column;
  justify-content: space-around;
}
</style>
