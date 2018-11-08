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
</style>
