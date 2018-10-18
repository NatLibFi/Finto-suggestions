<template>
  <div class="header-container">
    <div class="counts">
      <span class="open">{{ openSuggestionCount }} käsittelemätöntä</span>
      <span class="resolved">{{ resolvedSuggestionCount }} käsiteltyä</span>
    </div>
    <div
      @click="isDropDownOpened = !isDropDownOpened"
      :class="[isDropDownOpened ? 'selected' : '', 'drop-down-list']">
      <span>Järjestä</span>
      <svg-icon icon-name="triangle"><icon-triangle /></svg-icon>
    </div>
    <!-- TODO: Create SortingComponent from this div -->
    <div
      v-if="isDropDownOpened"
      class="drop-down-options"
      v-on-clickaway="closeDropDown">
      <div v-for="(option, i) in dropDownOptions" :key="option.id">
        <div
          @click="sortValueSelected(option, i)"
          :class="[i == selectedSortOptionIndex ? 'selected' : '', 'option']">
          <svg-icon
            :class="[i == selectedSortOptionIndex ? '' : 'hidden-checkmark']"
            icon-name="check"><icon-check />
          </svg-icon>
          <span>{{ option.label }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { suggestionSortingKeys } from '../../utils/suggestionMappings.js';
import { findValueFromDropDownOptions } from '../../utils/dropDownHelper.js';

import SvgIcon from '../icons/SvgIcon';
import IconTriangle from '../icons/IconTriangle';
import IconCheck from '../icons/IconCheck';
import { directive as onClickaway } from 'vue-clickaway';

export default {
  components: {
    SvgIcon,
    IconTriangle,
    IconCheck
  },
  directives: {
    onClickaway: onClickaway
  },
  props: {
    openSuggestionCount: Number,
    resolvedSuggestionCount: Number
  },
  data: () => ({
    // TODO: change the index to 0 after changing list order to NEWEST_FIRST
    selectedSortOptionIndex: 1,
    isDropDownOpened: false,
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
    sortValueSelected(option, index) {
      this.handleSortDropDownSelectedIndicator(index);

      if (option && option.value !== '') {
        // do sorting by sorting key
        const selectedValue = findValueFromDropDownOptions(option.value, this.dropDownOptions);
        this.sortSuggestionList(this.selectedOptionsMapper[selectedValue]);
      } else {
        this.sortSuggestionList(null);
      }
    },
    sortSuggestionList(selectedSorting) {
      this.$emit('sortSuggestionListBy', selectedSorting);
    },
    handleSortDropDownSelectedIndicator(index) {
      // update dropdownlist selected value indicator as selected
      this.selectedSortOptionIndex = index;
    },
    closeDropDown: function() {
      this.isDropDownOpened = false;
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.header-container {
  position: relative;
  width: 60vw;
  margin: 20px 20vw 0;
  font-weight: normal;
  text-align: left;
  background-color: #ffffff;
  border: 2px solid #f5f5f5;
}
.counts {
  display: inline-block;
  overflow: hidden;
  text-align: left;
  padding: 12px 20px 10px;
  font-size: 14px;
  font-weight: 600;
  vertical-align: middle;
}
.open {
  min-width: 25%;
  color: #06a798;
  padding-right: 10px;
}
.resolved {
  min-width: 25%;
  color: #a4a4a4;
}
.drop-down-list {
  position: absolute;
  top: 54%;
  right: 19px;
  transform: perspective(1px) translateY(-50%);
  overflow: hidden;
  text-align: right;
  font-size: 13px;
  font-weight: 600;
  color: #828282;
  cursor: pointer;
  cursor: hand;
}

.drop-down-list svg {
  display: inline-block;
  height: 16px;
  vertical-align: middle;
  margin: 0 0 -4px 2px;
}

.drop-down-options {
  position: absolute;
  top: 42px;
  right: 0;
  background-color: #ffffff;
  width: 200px;
  z-index: 2;
  border: 1px solid #e1e1e1;
  border-radius: 2px;
  -webkit-box-shadow: 6px 8px 17px -6px rgba(80, 80, 80, 0.35);
  -moz-box-shadow: 6px 8px 17px -6px rgba(80, 80, 80, 0.35);
  box-shadow: 6px 8px 17px -6px rgba(80, 80, 80, 0.35);
}

.option {
  padding: 8px 6px 7px;
  border-bottom: 1px solid #f5f5f5;
  font-size: 14px;
  font-weight: 500;
  color: #555555;
  vertical-align: middle;
}

.option:hover {
  background-color: #f3fbfa;
  color: #111111;
  cursor: pointer;
  cursor: hand;
}

.option svg {
  height: 10px;
  margin-right: 5px;
  vertical-align: middle;
}

.selected {
  font-weight: 600;
  color: #111111;
}

.hidden-checkmark {
  opacity: 0;
}

@media (max-width: 700px) {
  .header-container {
    width: 80vw;
    margin: 20px 10vw 0;
  }

  .counts {
    font-size: 12px;
  }

  .drop-down-list {
    right: 8px;
  }

  .option {
    padding: 12px 6px 11px;
  }
}
</style>
