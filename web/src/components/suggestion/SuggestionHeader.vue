<template>
  <div class="header-container">
    <div v-if="!userPage" class="title">
      <span class="open">{{ openSuggestionCount }} käsittelemätöntä</span>
      <span class="resolved">{{ resolvedSuggestionCount }} käsiteltyä</span>
    </div>
    <div v-if="userPage" class="title">
      <span>Käyttäjälle asetut ehdotukset</span>
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

import {
  mapSuggestionGetters,
  mapSuggestionActions
} from '../../store/modules/suggestion/suggestionModule.js';
import {
  suggestionGetters,
  suggestionActions
} from '../../store/modules/suggestion/suggestionConsts.js';

export default {
  components: {
    SortingDropDown,
    SvgIcon,
    IconTriangle
  },
  props: {
    openSuggestionCount: Number,
    resolvedSuggestionCount: Number,
    meetingSort: Boolean,
    userPage: Boolean
  },
  data: () => ({
    selectedSortOptionIndex: 0,
    isDropDownOpened: false,
    dropDownOptions: [
      { label: 'Uusin ensin', value: sortingKeys.NEWEST_FIRST },
      { label: 'Vanhin ensin', value: sortingKeys.OLDEST_FIRST },
      { label: 'Eniten kommentoitu', value: sortingKeys.MOST_COMMENTS },
      { label: 'Vähiten kommentoitu', value: sortingKeys.LEAST_COMMENTS },
      { label: 'Viimeksi päivitetty', value: sortingKeys.LAST_UPDATED },
      { label: 'Eniten reaktiota', value: sortingKeys.MOST_REACTIONS }
    ]
  }),
  computed: {
    ...mapSuggestionGetters({
      suggestionSelectedSort: suggestionGetters.GET_SUGGESTIONS_SELECTED_SORT,
      meetingSuggestionSelectedSort: suggestionGetters.GET_MEETING_SUGGESTIONS_SELECTED_SORT
    })
  },
  created() {
    if (this.meetingSort) {
      this.getMeetingSuggestionSelectedSort();
    } else {
      this.getSuggestionSelectedSort();
    }
    this.handleSortinDropDownIndex();
  },
  methods: {
    ...mapSuggestionActions({
      setSuggestionSelectedSort: suggestionActions.SET_SUGGESTIONS_SELECTED_SORT,
      setMeetingSuggestionSelectedSort: suggestionActions.SET_MEETING_SUGGESTIONS_SELECTED_SORT,
      getSuggestionSelectedSort: suggestionActions.GET_SUGGESTIONS_SELECTED_SORT,
      getMeetingSuggestionSelectedSort: suggestionActions.GET_MEETING_SUGGESTIONS_SELECTED_SORT
    }),
    setSelectedSort(selectedSort) {
      if (this.meetingSort) {
        this.setMeetingSuggestionSelectedSort(selectedSort);
        this.getMeetingSuggestionSelectedSort();
      } else {
        this.setSuggestionSelectedSort(selectedSort);
        this.getSuggestionSelectedSort();
      }
    },
    closeDropDown: function() {
      this.isDropDownOpened = false;
    },
    handleSortinDropDownIndex() {
      if (this.meetingSort) {
        this.selectedSortOptionIndex = getSelectedSortOptionIndex(
          this.dropDownOptions,
          this.meetingSuggestionSelectedSort,
          0
        );
      } else {
        this.selectedSortOptionIndex = getSelectedSortOptionIndex(
          this.dropDownOptions,
          this.suggestionSelectedSort,
          0
        );
      }
    }
  },
  watch: {
    suggestionSelectedSort() {
      this.handleSortinDropDownIndex();
    },
    meetingSuggestionSelectedSort() {
      this.handleSortinDropDownIndex();
    }
  }
};
</script>

<style scoped>
.header-container {
  position: relative;
  width: 60vw;
  margin: 20px 20vw 0;
  font-weight: normal;
  text-align: left;
  background-color: #ffffff;
  border: 2px solid #f5f5f5;
  height: 36px;
}
.title {
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

  .title {
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
