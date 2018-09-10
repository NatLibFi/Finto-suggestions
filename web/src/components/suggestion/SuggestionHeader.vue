<template>
  <section class="SuggestionListHeader">
    <span class="open">{{ openSuggestionCount }} käsittelemätöntä</span>
    <span class="resolved">{{ resolvedSuggestionCount }} käsiteltyä</span>
    <span class="filteringOptions">
      <select v-model="selectedSortOption" @change="sortValueSelected">
        <option disabled value="">Järjestele</option>
        <option v-if="selectedSortOption != ''" value=""></option>
        <option v-for="selection in dropDownOptions" :key="selection.label">{{ selection.label }}</option>
      </select>
    <i class="arrow down"></i>
    </span>
  </section>
</template>

<script>
import sortConst from "../../utils/suggestionSortConst.js";

export default {
  props: {
    openSuggestionCount: Number,
    resolvedSuggestionCount: Number
  },
  data: () => ({
    selectedSortOption: "",
    dropDownOptions: [
      { label: "Uusin ensin", value: "NEWEST_FIRST" },
      { label: "Vanhin ensin", value: "OLDEST_FIRST" },
      { label: "Eniten kommentoitu", value: "MOST_COMMENTS" },
      { label: "Vähiten kommentoitu", value: "LEAST_COMMENTS" },
      { label: "Viimeksi päivitetty", value: "LAST_UPDATED" },
      { label: "Eniten reaktiota", value: "MOST_REACTIONS" }
    ],
    selectedOptionsMapper: {
      NEWEST_FIRST: sortConst.NEWEST_FIRST,
      OLDEST_FIRST: sortConst.OLDEST_FIRST,
      MOST_COMMENTS: sortConst.MOST_COMMENTS,
      LEAST_COMMENTS: sortConst.LEAST_COMMENTS,
      LAST_UPDATED: sortConst.LAST_UPDATED,
      MOST_REACTIONS: sortConst.MOST_REACTIONS
    }
  }),
  created() {
    this.$emit("fetchOpenSuggestionCount");
    this.$emit("fetchResolvedSuggestionCount");
  },
  methods: {
    sortValueSelected() {
      const selectedValue = this.dropDownOptions.find(e => e.label == this.selectedSortOption);
      this.sortSuggestionList(this.selectedOptionsMapper[selectedValue.value]);
    },
    sortSuggestionList(selectedFiltering) {
      this.$emit("sortSuggestionListBy", selectedFiltering);
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.SuggestionListHeader {
  font-weight: normal;
  border-top: 2px solid #b1bfd6;
  margin: 10px 0 0 10px;
}
.SuggestionListHeader span {
  margin: 10px;
  justify-content: space-between;
  flex-wrap: wrap;
}
.open {
  min-width: 25%;
  color: green;
}
.resolved {
  min-width: 25%;
  color: grey;
}
.filteringOptions {
  flex-grow: 1;
  width: 50%;
}

.filteringOptions select {
  border: 0 !important; /*Removes border*/
  -webkit-appearance: none; /*Removes default chrome and safari style*/
  -moz-appearance: none; /*Removes default style Firefox*/
}

.filteringOptions select:focus {
  outline: none;
}

.filteringOptions option:hover {
  box-shadow: 0 0 10px 100px #1882a8 inset;
}

/* CAUTION: IE hackery ahead */
.filteringOptions select::-ms-expand {
  display: none; /* remove default arrow on ie10 and ie11 */
}

/* target Internet Explorer 9 to undo the custom arrow */
@media screen and (min-width: 0\0) {
  .filteringOptions select {
    background: none\9;
    padding: 5px\9;
  }
}

i {
  border: solid black;
  border-width: 0 3px 3px 0;
  display: inline-block;
  padding: 3px;
}
.down {
  transform: rotate(45deg);
  -webkit-transform: rotate(45deg);
}
</style>
