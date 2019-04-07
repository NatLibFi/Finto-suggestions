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
      @setSelectedSort="setSelectedSort"
      @refreshSelectedIndex="selectedSortOptionIndex = $event"
      @closeDropDown="closeDropDown"/>
  </div>
</template>

<script>
import { sortingKeys, getSelectedSortOptionIndex } from '../../utils/sortingHelper.js';

import SortingDropDown from '../common/SortingDropDown';
import SvgIcon from '../icons/SvgIcon';
import IconTriangle from '../icons/IconTriangle';

import { mapMeetingGetters, mapMeetingActions } from '../../store/modules/meeting/meetingModule.js';
import { meetingGetters, meetingActions } from '../../store/modules/meeting/meetingConsts.js';

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
    selectedSortOptionIndex: 1,
    isDropDownOpened: false,
    dropDownOptions: [
      { label: 'Ensin luotu ensin', value: sortingKeys.OLDEST_FIRST },
      { label: 'Viimeiseksi luotu ensin', value: sortingKeys.NEWEST_FIRST }
    ]
  }),
  computed: {
    ...mapMeetingGetters({
      selectedSort: meetingGetters.GET_MEETINGS_SELECTED_SORT
    })
  },
  created() {
    this.getSelectedSortKey();
    this.handleSortinDropDownIndex();
  },
  methods: {
    ...mapMeetingActions({
      setSelectedSortKey: meetingActions.SET_MEETINGS_SELECTED_SORT,
      getSelectedSortKey: meetingActions.GET_MEETINGS_SELECTED_SORT
    }),
    setSelectedSort(selectedSort) {
      this.setSelectedSortKey(selectedSort);
    },
    closeDropDown() {
      this.isDropDownOpened = false;
    },
    handleSortinDropDownIndex() {
      if (this.selectedSort) {
        this.selectedSortOptionIndex = getSelectedSortOptionIndex(
          this.dropDownOptions,
          this.selectedSort
        );
      }
    }
  },
  watch: {
    selectedSort() {
      this.handleSortinDropDownIndex();
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
  font-size: 13px;
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
  transform: perspective(1px) translateY(calc(-50% - 0.5px));
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
