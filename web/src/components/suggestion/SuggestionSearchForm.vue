<template>
  <div class="search-suggestions">
    <h5>Hae ehdotusta</h5>
    <div class="search-wrapper">
      <div class="input-wrapper">
        <input v-model="searchQuery" ref="input" @keyup.enter="doSearch" type="text" />
        <transition name="fade">
          <div v-if="searchQuery.length > 0" @click="clearSearch" class="clear-button">
            <svg-icon icon-name="cross"><icon-cross /></svg-icon>
          </div>
        </transition>
      </div>
      <div @click="doSearch" class="search-button">
        <span>Hae</span>
      </div>
    </div>
  </div>
</template>

<script>
import SvgIcon from '../icons/SvgIcon';
import IconCross from '../icons/IconCross';

import {
  suggestionGetters,
  suggestionActions
} from '../../store/modules/suggestion/suggestionConsts.js';

import {
  mapSuggestionGetters,
  mapSuggestionActions
} from '../../store/modules/suggestion/suggestionModule.js';

import { handleSetFilters } from '../../utils/filterValueHelper.js';
import { filterType } from '../../utils/suggestionHelpers.js';

export default {
  components: {
    SvgIcon,
    IconCross
  },
  data: () => ({
    searchQuery: ''
  }),
  computed: {
    ...mapSuggestionGetters({
      filters: suggestionGetters.GET_FILTERS
    })
  },
  async created() {
    await this.getSelectedFilters();
    if (this.filters.length > 0) {
      const searchFilter = this.filters.find(f => f.type === filterType.SEARCH);
      this.searchQuery = searchFilter ? searchFilter.value : '';
    }
  },
  methods: {
    ...mapSuggestionActions({
      setFilters: suggestionActions.SET_SELECTED_FILTERS,
      getSelectedFilters: suggestionActions.GET_SELECTED_FILTERS
    }),
    doSearch() {
      const value = { type: filterType.SEARCH, value: this.searchQuery };
      handleSetFilters(value, this.filters, this.setFilters);
    },
    clearSearch() {
      this.searchQuery = '';
      this.doSearch();
    }
  },
  mounted: function() {
    document.addEventListener('keydown', e => {
      if (e.keyCode == 13) {
        this.doSearch();
      }
    });
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

.input-wrapper {
  position: relative;
  display: inline-block;
  height: 38px;
  width: calc(100% - 150px);
  text-align: left;
}

.input-wrapper input {
  position: absolute;
  width: 100%;
  height: 38px;
  padding-left: 8px;
  text-align: left;
  border: 2px solid #eeeeee;
  font-size: 14px;
  font-weight: 500;
  box-sizing: border-box;
}

.input-wrapper .clear-button {
  position: absolute;
  right: 12px;
  top: 7px;
  color: #cccccc;
}

.input-wrapper .clear-button:hover {
  color: #bbbbbb;
}

.input-wrapper .clear-button svg {
  width: 20px;
}

.search-button {
  position: absolute;
  right: 0;
  display: inline-block;
  height: 38px;
  width: 140px;
  color: #ffffff;
  font-weight: 600;
  font-size: 16px;
  background-color: #06A798;
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

@media (max-width: 900px) {
  .search-wrapper input, .search-button {
    display: block;
    position: relative;
    width: 100%;
  }

.input-wrapper {
  width: 100%;
}

  .search-button {
    left: 0;
    margin-top: 10px;
    margin-bottom: 0;
  }
}

.fade-enter-active {
  transition: opacity 0.1s;
}
.fade-leave-active {
  transition: opacity 0.2s;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>
