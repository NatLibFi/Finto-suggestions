<template>
<div class="paginate-container">
  <paginate
    v-if="pageCount"
    v-model="page"
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
      this.$emit('paginationPageChanged', pageNumber);
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
  transform: translate(-50%, -50%);
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
</style>
