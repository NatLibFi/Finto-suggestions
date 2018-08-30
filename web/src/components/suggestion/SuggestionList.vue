<template>
  <ul class="suggestionList">
  <suggestion-element
    class="suggestionElement"
    v-for="item in this.items"
    v-bind:key="item.orderNumber"
    :orderNumber=item.orderNumber
    :title=item.title
    :created=item.created
    :tags=item.tags />
  </ul>
</template>

<script>
// import {
//   suggestionActions,
//   suggestionGetters,
//   mapSuggestionActions,
//   mapSuggestionGetters } from '../../store/modules/suggestion'
import SuggestionElement from './SuggestionElement'
import api from "../../api/index.js"

export default {
  name: "SuggestionList",
  components: {
    SuggestionElement
  },
  data() {
    return {
      items:
      [
        // {
        //   orderNumber: 123,
        //   title: "Viru-Nigula",
        //   created: "2018-08-27",
        //   tags: ["created", "change"]
        // },
        // {
        //   orderNumber: 231,
        //   title: "Viru-Peruna",
        //   created: "2018-08-26",
        //   tags: ["created", "change"]
        // },
        // {
        //   orderNumber: 321,
        //   title: "Viru-Porkkana",
        //   created: "2018-08-25",
        //   tags: ["created", "change"]
        // }
      ]
    }
  },
  created: {
    async getSuggestions() {
      this.items = await api.suggestions.getSuggestions();
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  ul {
    list-style: none;
  }

  .suggestionList {
    align-items: flex-start;
    text-align: start;
  }

  .suggestionElement {
    margin: 10px 0 10px 0;
    border-top: 2px solid #b1bfd6;
    border-bottom: 2px solid #b1bfd6;
  }
</style>
