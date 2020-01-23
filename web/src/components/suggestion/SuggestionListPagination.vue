<template>
  <div :class="[pageCountLoading ? 'loading' : '', 'paginate-container']">
    <transition name="fade">
      <paginate
        v-if="pageCount"
        v-model="pageNumber"
        :page-count="pageCount"
        :click-handler="changePageHandler"
        :prev-text="'«'"
        :next-text="'»'"
        :container-class="'paginate'"
        :page-class="'paginate-item'"
        :next-class="'paginate-item next'"
        :prev-class="'paginate-item prev'"
      >
      </paginate>
    </transition>
  </div>
</template>

<script>
import Paginate from 'vuejs-paginate';

import { handleQueries } from '../../utils/suggestionHelpers.js';

export default {
  components: {
    Paginate
  },
  props: {
    meetingId: {
      type: [Number, String],
      default: null
    },
    pageCount: Number,
    page: [String, Number],
    pageCountLoading: Boolean,
    isUserPage: Boolean,
    userId: [Number, String]
  },
  created() {
    this.pageNumber = parseInt(this.page, 10);
  },
  data() {
    return {
      pageNumber: 1,
      filters: this.$route.query.filters ? this.$route.query.filters : '',
      searchWord: this.$route.query.search ? this.$route.query.search : '',
      sort: this.$route.query.sort ? this.$route.query.sort : ''
    };
  },
  methods: {
    changePageHandler(pageNumber) {
      if (this.isUserPage) {
        this.$router.push({
          name: 'user',
          params: {
            page: pageNumber,
            userId: this.userId
          }
        });
      } else if (this.meetingId) {
        this.$router.push({
          name: 'meeting-suggestion-list',
          params: {
            meetingId: this.meetingId,
            page: pageNumber
          }
        });
      } else {
        this.$router.push({
          name: 'suggestions',
          params: {
            page: pageNumber,
            meetingId: null
          }
        });
      }
      handleQueries(this.filters, this.searchWord, this.sort, this.$router);
    }
  },
  watch: {
    $route() {
      this.filters = this.$route.query.filters ? this.$route.query.filters : '';
      this.searchWord = this.$route.query.search ? this.$route.query.search : '';
      this.sort = this.$route.query.sort ? this.$route.query.sort : '';
    }
  }
};
</script>

<style>
div.paginate-container {
  position: relative;
  height: 70px;
  width: 60vw;
  margin: 0 20vw 50px;
  background-color: #ffffff;
  border: 2px solid #f5f5f5;
  border-top: none;
  overflow: none;
}

ul.paginate {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, calc(-50% - 0.5px));
  padding: 0;
  margin: 0;
  width: 100%;
}

ul.paginate .paginate-item {
  display: inline-block;
  max-height: 26px;
  padding: 0;
  margin: 0;
}

.paginate-item a {
  display: inline-block;
  width: 26px;
  height: 26px;
  margin: 0 1px;
  border: 2px solid #eeeeee;
  border-radius: 1px;
  line-height: 28px;
  font-size: 14px;
  font-weight: 800;
  vertical-align: middle;
  -webkit-user-select: none; /* Safari */
  -moz-user-select: none; /* Firefox */
  -ms-user-select: none; /* IE10+/Edge */
  user-select: none; /* Standard */
  outline: none;
}

.paginate-item.prev a,
.paginate-item.next a {
  color: #06b1a1;
  line-height: 26px;
}

.paginate-item a:hover {
  border-color: #a7e7e1;
}

.paginate-item.active a {
  border-color: #06b1a1;
  background-color: #06b1a1;
  color: #ffffff;
}

.paginate-item.disabled a,
.paginate-item.disabled a:hover,
.paginate-item.disabled a:active,
.paginate-item.disabled a:focus {
  color: #eeeeee;
  border-color: #eeeeee;
  cursor: initial;
}

@media (max-width: 700px) {
  div.paginate-container {
    width: 80vw;
    margin: 0 10vw 50px;
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}

.loading {
  animation: loading 1.5s infinite;
}

@keyframes loading {
  0% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
  100% {
    opacity: 1;
  }
}
</style>
