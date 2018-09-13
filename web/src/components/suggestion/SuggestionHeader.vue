<template>
  <div>
    <section class="SuggestionListHeader">
      <div class="headerContainer">
        <div class="counts">
          <span class="open">{{ openSuggestionCount }} käsittelemätöntä</span>
          <span class="resolved">{{ resolvedSuggestionCount }} käsiteltyä</span>
        </div>
        <div class="dropDownList">
          <span class="sortingOptions">
            <select v-model="selectedSortOption" @change="sortValueSelected" :required="true">
              <option disabled value="">Järjestele</option>
              <option value=""></option>
              <option v-for="selection in dropDownOptions" :key="selection.label" :value="selection.label">{{ selection.label }}</option>
            </select>
            <i class="arrow down"></i>
          </span>
        </div>
      </div>
    </section>
  </div>
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
    selectedSortOptionIndex: 0,
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
    sortValueSelected(selected) {
      this.handleSortDropDownSelectedIndicator(selected);

      if(selected && selected.target.value !== '') {
        // do sorting by sorting key
        const selectedValue = this.dropDownOptions.find(e => e.label == selected.target.value);
        this.sortSuggestionList(this.selectedOptionsMapper[selectedValue.value]);
      }
      else {
        this.sortSuggestionList(this.selectedSortOption);
      }
    },
    sortSuggestionList(selectedFiltering) {
      this.$emit("sortSuggestionListBy", selectedFiltering);
    },
    handleSortDropDownSelectedIndicator(selected) {
      // update dropdownlist selected value indicator as selected
      // TODO: this is dirty way doing this, need to refactore more vuejs way doing this
      if(this.selectedSortOptionIndex > 0) {
        const selectedOption = selected.target[this.selectedSortOptionIndex];
        selectedOption.innerText = selectedOption.value.slice(0, selectedOption.value.length)
      }

      const selectedIndex = selected.target.selectedIndex;

      if(selectedIndex > 1){
        selected.target[selectedIndex].innerText = `> ${selected.target.value}`;
        this.selectedSortOptionIndex = selectedIndex;
      }
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.headerContainer {
  width: 90%;
  margin-left: 40px;
  padding: 10px;
  height: 30%;
  border-top: 2px solid #b1bfd6;
  font-weight: normal;
}
.counts {
  display: inline-block;
  width: 80%;
  overflow: hidden;
  text-align: left;
}
.dropDownList{
  float: right;
  width: 20%;
  overflow: hidden;
  text-align: right;
}
.open {
  min-width: 25%;
  color: green;
  font-weight: bold;
  padding-right: 10px;
}
.resolved {
  min-width: 25%;
  color: grey;
  font-weight: bold;
}
.sortingOptions {
  flex-grow: 1;
  width: 70%;
  right: 0;
  position: relative;
}

.sortingOptions select {
  border: 0 !important; /*Removes border*/
  -webkit-appearance: none; /*Removes default chrome and safari style*/
  -moz-appearance: none; /*Removes default style Firefox*/
  font-size: 12pt;
  width: 40%;
}

.sortingOptions select:focus {
  outline: none;
  border: 2px solid red;
}

.sortingOptions option:hover {
  box-shadow: 0 0 10px 100px #1882a8 inset;
}

/* CAUTION: IE hackery ahead */
.sortingOptions select::-ms-expand {
  display: none; /* remove default arrow on ie10 and ie11 */
}

/* target Internet Explorer 9 to undo the custom arrow */
@media screen and (min-width: 0\0) {
  .sortingOptions select {
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
.right {
  transform: rotate(-45deg);
  -webkit-transform: rotate(-45deg);
}
</style>
