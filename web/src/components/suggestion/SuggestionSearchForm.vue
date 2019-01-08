<template>
  <div class="search-suggestions">
    <h5>Hae ehdotusta</h5>
    <div class="search-wrapper">
      <input type="text" v-model="searchQuery" />
      <div @click="doSearch" class="search-button">
        <span>Hae</span>
      </div>
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
/* eslint-disable */
</script>

<style scoped>
.search-suggestions {
  height: 100%;
  padding-bottom: 20px;
}

h5 {
  text-align: left;
  margin-bottom: 6px;
}

.search-wrapper {
  position: relative;
  height: 100%;
  width: 100%;
  text-align: left;
}

.search-wrapper input {
  display: inline-block;
  width: 58%;
  height: 36px;
  margin-right: 30px;
  padding-left: 8px;
  text-align: left;
  border: 2px solid #eeeeee;
  font-size: 14px;
  font-weight: 500;
}

.search-button {
  display: inline-block;
  height: 42px;
  width: 140px;
  color: #ffffff;
  font-weight: 600;
  font-size: 16px;
  background-color: #06A798;
  position: relative;
  margin-bottom: -14px;
  text-align: center;
  cursor: pointer;
  cursor: hand;
  -webkit-user-select: none; /* Safari */
  -moz-user-select: none; /* Firefox */
  -ms-user-select: none; /* IE10+/Edge */
  user-select: none; /* Standard */
  transition: background-color 0.1s;
}

.search-button:hover {
  background-color: #0EB6A6;
}

.search-button span {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: perspective(1px) translate(-50%, -50%);
}

@media (max-width: 700px) {
  .search-wrapper input, .search-button {
    display: block;
    position: relative;
    width: 100%;
  }

  .search-button {
    left: 0;
    margin-top: 10px;
    margin-bottom: 0;
  }
}
</style>
