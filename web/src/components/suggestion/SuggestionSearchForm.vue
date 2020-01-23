<template>
  <div class="search-suggestions">
    <h5>Hae ehdotusta {{ searchWord }}</h5>
    <div class="search-wrapper">
      <div class="input-wrapper">
        <input
          :value="searchWord"
          ref="input"
          @input="updateSearchWord"
          @keyup.enter.prevent="updateSearchWord"
        />
        <transition name="fade">
          <div v-if="searchWord && searchWord.length > 0" @click="clearSearch" class="clear-button">
            <svg-icon icon-name="cross"><icon-cross /></svg-icon>
          </div>
        </transition>
      </div>
    </div>
  </div>
</template>

<script>
import SvgIcon from '../icons/SvgIcon';
import IconCross from '../icons/IconCross';

import { handleQueries } from '../../utils/suggestionHelpers.js';

export default {
  components: {
    SvgIcon,
    IconCross
  },
  props: {
    filters: String,
    searchWord: String,
    sort: String
  },
  methods: {
    updateSearchWord() {
      setTimeout(() => {
        handleQueries(this.filters, this.$refs.input.value, this.sort, this.$router);
      }, 800);
    },
    clearSearch() {
      handleQueries(this.filters, '', this.sort, this.$router);
    }
  },
  mounted() {
    document.addEventListener('keydown', e => {
      if (e.keyCode == 13) {
        this.updateSearchWord(this.$refs.input.value);
      }
    });
  },
  watch: {
    $route() {
      this.filters = this.$route.query.filters ? this.$route.query.filters : '';
      this.sort = this.$route.query.sort ? this.$route.query.sort : '';
    }
  }
};
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
  height: 40px;
  width: 100%;
  text-align: left;
}

.input-wrapper input {
  position: absolute;
  width: 100%;
  height: 40px;
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
  top: 8px;
  color: #cccccc;
}

.input-wrapper .clear-button:hover {
  color: #bbbbbb;
}

.input-wrapper .clear-button svg {
  width: 20px;
}

@media (max-width: 900px) {
  .search-wrapper input {
    display: block;
    position: relative;
    width: 100%;
  }

  .input-wrapper {
    width: 100%;
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
