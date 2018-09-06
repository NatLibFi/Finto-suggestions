<template>
  <div class="container">
    <!-- <img src="../assets/logo.png"> -->
    <SuggestionList />
  </div>
</template>

<script>
// @ is an alias to /src
import SuggestionList from "../components/suggestion/SuggestionList";

export default {
  name: "index",
  components: {
    SuggestionList
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
