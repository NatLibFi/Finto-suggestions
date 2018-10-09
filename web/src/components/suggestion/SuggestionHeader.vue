<template>
  <div>
    <section>
      <div class="headerContainer">
        <div class="counts">
          <span class="open">{{ openSuggestionCount }} käsittelemätöntä</span>
          <span class="resolved">{{ resolvedSuggestionCount }} käsiteltyä</span>
        </div>
         <div class="dropDownList">
           <common-drop-down
            :header="'Järjestele'"
            :options="dropDownOptions"
            :changeCallBack="sortValueSelected"
           />
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import { suggestionSortingKeys } from '../../utils/suggestionMappings.js';
import commonDropDown from '../common/CommonDropDown';
import { findValueFromDropDownOptions } from '../../utils/dropDownHelper.js'

export default {
  components: {
    commonDropDown
  },
  props: {
    openSuggestionCount: Number,
    resolvedSuggestionCount: Number
  },
  data: () => ({
    selectedSortOptionIndex: 0,
    dropDownOptions: [
      { label: 'Uusin ensin', value: 'NEWEST_FIRST' },
      { label: 'Vanhin ensin', value: 'OLDEST_FIRST' },
      { label: 'Eniten kommentoitu', value: 'MOST_COMMENTS' },
      { label: 'Vähiten kommentoitu', value: 'LEAST_COMMENTS' },
      { label: 'Viimeksi päivitetty', value: 'LAST_UPDATED' },
      { label: 'Eniten reaktiota', value: 'MOST_REACTIONS' }
    ],
    selectedOptionsMapper: {
      NEWEST_FIRST: suggestionSortingKeys.NEWEST_FIRST,
      OLDEST_FIRST: suggestionSortingKeys.OLDEST_FIRST,
      MOST_COMMENTS: suggestionSortingKeys.MOST_COMMENTS,
      LEAST_COMMENTS: suggestionSortingKeys.LEAST_COMMENTS,
      LAST_UPDATED: suggestionSortingKeys.LAST_UPDATED,
      MOST_REACTIONS: suggestionSortingKeys.MOST_REACTIONS
    }
  }),
  methods: {
    sortValueSelected(selected) {
      this.handleSortDropDownSelectedIndicator(selected);

      if (selected && selected.target.value !== '') {
        // do sorting by sorting key
        const selectedValue = findValueFromDropDownOptions(selected.target.value, this.dropDownOptions);
        this.sortSuggestionList(this.selectedOptionsMapper[selectedValue]);
      } else {
        this.sortSuggestionList(null);
      }
    },
    sortSuggestionList(selectedSorting) {
      this.$emit('sortSuggestionListBy', selectedSorting);
    },
    handleSortDropDownSelectedIndicator(selected) {
      // update dropdownlist selected value indicator as selected
      // TODO: this is dirty way doing this, need to refactore more vuejs way doing this
      if (this.selectedSortOptionIndex > 0) {
        const selectedOption = selected.target[this.selectedSortOptionIndex];
        selectedOption.innerText = selectedOption.value.slice(0, selectedOption.value.length);
      }

      const selectedIndex = selected.target.selectedIndex;

      if (selectedIndex > 1) {
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
  font-weight: normal;
}
.counts {
  display: inline-block;
  width: 80%;
  overflow: hidden;
  text-align: left;
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
.dropDownList {
  float: right;
  width: 20%;
  overflow: hidden;
  text-align: right;
}
</style>
