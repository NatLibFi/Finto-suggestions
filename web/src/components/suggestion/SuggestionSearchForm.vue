<template>
  <div class="searchSuggestions">
    <h4>Hae ehdotusta</h4>
    <span>
      <form>
        <input type="text" v-model="searchQuery" value="Hae jotain" />
        <input type="button" value="Hae" @click="doSearch" />
        </form>
      </span>
    </div>
</template>

<script>
export default {
  data: () => ({
    searchQuery: ''
  }),
  methods: {
    doSearch() {
      console.log(this.searchQuery);
    }
  }
}
</script>

<style scoped>
.searchSuggestions {}
</style>
