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
import { suggestionActions } from '../../store/modules/suggestion/suggestionConsts.js';
import { mapSuggestionActions } from '../../store/modules/suggestion/suggestionModule.js';

export default {
  data: () => ({
    searchQuery: null
  }),
  methods: {
    ...mapSuggestionActions({
      setSearchQuery: suggestionActions.SET_SEARCH_QUERY
    }),
    doSearch() {
      this.setSearchQuery(this.searchQuery);
    }
  }
};
</script>

<style scoped>
</style>
