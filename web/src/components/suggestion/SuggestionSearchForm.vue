<template>
  <div class="searchSuggestions">
    <h4>Hae ehdotusta</h4>
    <div class="search-wrapper">
      <label>
        <input type="text" v-model="searchQuery" />
      </label>
      <input type="button" value="Hae" @click="doSearch" />
    </div>
  </div>
</template>

<script>
import {
  suggestionGetters,
  suggestionMutations
} from '../../store/modules/suggestion/suggestionConsts.js';

import {
  mapSuggestionGetters,
  mapSuggestionMutations
} from '../../store/modules/suggestion/suggestionModule.js';

import { handleSetFilters } from '../../utils/filterValueHelper.js';
import { filterType } from '../../utils/suggestionMappings.js';

export default {
  data: () => ({
    searchQuery: ''
  }),
  computed: {
    ...mapSuggestionGetters({ filters: suggestionGetters.GET_FILTERS })
  },
  methods: {
    ...mapSuggestionMutations({ setFilters: suggestionMutations.SET_FILTERS }),
    doSearch() {
      const value = { type: filterType.SEARCH, value: this.searchQuery };
      handleSetFilters(value, this.filters, this.setFilters);
    }
  }
};
</script>

<style scoped>
div.search-wrapper {
  float: left;
  width: 100%;
  height: 4em;
  padding: .5em;
  text-align: left;
}
div.search-wrapper > label > [type="text"] {
  display: inline-block;
  height: 50%;
  width: 80%;
  vertical-align: middle;
  margin-right: 30px;
  text-align: left;
  background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='25' height='25' viewBox='0 0 35 25' fill-rule='evenodd'%3E%3Cpath d='M16.036 18.455l2.404-2.405 5.586 5.587-2.404 2.404zM8.5 2C12.1 2 15 4.9 15 8.5S12.1 15 8.5 15 2 12.1 2 8.5 4.9 2 8.5 2zm0-2C3.8 0 0 3.8 0 8.5S3.8 17 8.5 17 17 13.2 17 8.5 13.2 0 8.5 0zM15 16a1 1 0 1 1 2 0 1 1 0 1 1-2 0'%3E%3C/path%3E%3C/svg%3E") center / contain no-repeat;
  background-position: left;
  text-indent: 32px;
  font-size: 14pt;
}
div.search-wrapper > [type="button"] {
  height: 60%;
  width: 13%;
  background-color: #06A798;
  color: #FFFFFF;
  font-size: 14pt;
  border-radius: 2px;
}
</style>
