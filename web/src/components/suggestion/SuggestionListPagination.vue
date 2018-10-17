<template>
<div class="paginate">
  <paginate
    :page-count="20"
    :click-handler="functionName"
    :prev-text="'Prev'"
    :next-text="'Next'"
    :container-class="'paginate'">
  </paginate>
</div>
</template>

<script>
import Paginate from 'vuejs-paginate';

export default {
  components: {
    Paginate
  },
  methods: {
    testfunc(asd) {
      console.log("test func");
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

</style>
