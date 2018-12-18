<template>
  <div class="header-container">
    <div class="counts">
      <span class="open">{{ futureMeetingCount }} tulevaa</span>
      <span class="resolved">{{ pastMeetingCount }} mennyttä</span>
    </div>
    <div
      @click="isDropDownOpened = !isDropDownOpened"
      :class="[isDropDownOpened ? 'selected' : '', 'drop-down-button']">
      <span>Järjestä</span>
      <svg-icon icon-name="triangle"><icon-triangle /></svg-icon>
    </div>
    <sorting-drop-down
      :selectedIndex="selectedSortOptionIndex"
      :isOpened="isDropDownOpened"
      :dropDownOptions="dropDownOptions"
      @sortSuggestionListBy="sortSuggestionList"
      @refreshSelectedIndex="selectedSortOptionIndex = $event"
      @closeDropDown="closeDropDown"/>
  </div>
</template>

<script>
import { sortingKeys } from '../../utils/sortingHelper.js';

import SortingDropDown from '../common/SortingDropDown';
import SvgIcon from '../icons/SvgIcon';
import IconTriangle from '../icons/IconTriangle';

export default {
  components: {
    SortingDropDown,
    SvgIcon,
    IconTriangle
  },
  props: {
    futureMeetingCount: Number,
    pastMeetingCount: Number
  },
  data: () => ({
    // TODO: change the index to 0 after changing list order to NEWEST_FIRST
    selectedSortOptionIndex: 1,
    isDropDownOpened: false,
    dropDownOptions: [
      { label: 'Uusin ensin', value: suggestionSortingKeys.NEWEST_FIRST },
      { label: 'Vanhin ensin', value: suggestionSortingKeys.OLDEST_FIRST }
    ]
  }),
  methods: {
    sortSuggestionList(selectedSorting) {
      this.$emit('sortListBy', selectedSorting);
    },
    closeDropDown() {
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
.drop-down-button {
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

.drop-down-button svg {
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
