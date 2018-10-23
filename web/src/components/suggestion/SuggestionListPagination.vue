<template>
<div class="paginate">
  <paginate
    v-model="page"
    :page-count="pageCount"
    :click-handler="changePageHandler"
    :prev-text="'<<'"
    :next-text="'>>'"
    :container-class="'paginate'"
    :page-link-class="'paginateLink'"
    :page-class="'paginateItem'"
    :next-class="'paginateItem'"
    :prev-class="'paginateItem'"
    >
  </paginate>
</div>
</template>

<script>
import Paginate from 'vuejs-paginate';

export default {
  components: {
    Paginate
  },
  props: {
    pageCount: Number
  },
  data: () => ({
    page: 1
  }),
  methods: {
    changePageHandler(pageNumber) {
      this.$emit('paginationPageChanged', pageNumber)
    }
  }
};
</script>

<style>
.paginate ul {
  padding: 0;
  margin: 0;
}

.paginate li {
  display: inline-block;
  padding: 10px 10px;
}

.active {
  font-weight: bold;
  border: none;
}

.paginateLink:focus {
  outline: none;
}

.paginateItem {
  border: 1px solid lightgray;
  height: 15px;
}


</style>
