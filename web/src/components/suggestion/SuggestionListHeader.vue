<template>
  <div class="header-container">
    <div v-if="!userPage" class="title">
      <span>Tuloksia: {{ suggestionCount }} </span>
      <span v-if="isArchivedStatus"> Arkistoitu: {{ archivedSuggestionCount }}</span>
    </div>
    <div v-if="userPage" class="title user-title">
      <span>Käyttäjälle asetut ehdotukset</span>
    </div>
    <div
      v-if="!userPage"
      @click="isDropDownOpened = !isDropDownOpened"
      :class="[
        isDropDownOpened ? 'selected' : '',
        selectedSortOptionIndex !== 0 ? 'active' : '',
        'drop-down-button'
      ]"
    >
      <span>Järjestä</span>
      <svg-icon icon-name="triangle"><icon-triangle /></svg-icon>
    </div>
    <sorting-drop-down
      :selectedIndex="selectedSortOptionIndex"
      :isOpened="isDropDownOpened"
      :dropDownOptions="dropDownOptions"
      @setSelectedSort="setSelectedSort"
      @refreshSelectedIndex="selectedSortOptionIndex = $event"
      @closeDropDown="closeDropDown"
    />
  </div>
</template>

<script>
import SortingDropDown from '../common/SortingDropDown';
import SvgIcon from '../icons/SvgIcon';
import IconTriangle from '../icons/IconTriangle';
import router from '../../router/index';
import { sortingKeys } from '../../utils/sortingHelper.js';
import { handleQueries, findSortSelectionIndex } from '../../utils/suggestionHelpers.js';
export default {
  components: {
    SortingDropDown,
    SvgIcon,
    IconTriangle
  },
  props: {
    suggestionCount: Number,
    archivedSuggestionCount: Number,
    meetingId: {
      type: [String, Number],
      default: null
    },
    userPage: Boolean,
    filters: String,
    searchWord: String,
    sort: String
  },
  data() {
    return {
      selectedSortOptionIndex: 0,
      isDropDownOpened: false,
      dropDownOptions: [
        { label: 'Uusin ensin', value: sortingKeys.NEWEST_FIRST },
        { label: 'Vanhin ensin', value: sortingKeys.OLDEST_FIRST },
        { label: 'Eniten kommentoitu', value: sortingKeys.MOST_COMMENTS },
        { label: 'Vähiten kommentoitu', value: sortingKeys.LEAST_COMMENTS },
        { label: 'Viimeksi päivitetty', value: sortingKeys.LAST_UPDATED }
      ],
      isArchivedStatus: false
    };
  },
  created() {
    this.parseRouteForSelection();
    this.isArchivedStatus = !this.filters.startsWith('status:');
  },
  watch: {
    filters() {
      this.isArchivedStatus = !this.filters.startsWith('status:');
    }
  },
  methods: {
    setSelectedSort(selectedSort) {
      console.log('Name of the current page: ' + router.history.current.name);
      if (router.history.current.name === 'suggestions') {
        router.push('/suggestions/1');
      }
      if (router.history.current.name === 'meeting-suggestion-list') {
        router.push('/meetings/' + router.history.current.params.meetingId + '/1');
      }
      handleQueries(this.filters, this.searchWord, selectedSort, this.$router);
      location.reload();
    },
    closeDropDown: function() {
      this.isDropDownOpened = false;
    },
    parseRouteForSelection() {
      let arr = Object.values(this.dropDownOptions);
      if (this.sort) {
        this.selectedSortOptionIndex = findSortSelectionIndex(this.sort, arr);
      }
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
  color: #a4a4a4;
  vertical-align: middle;
  min-width: 25%;
  cursor: pointer;
  cursor: hand;
  -webkit-user-select: none; /* Safari */
  -moz-user-select: none; /* Firefox */
  -ms-user-select: none; /* IE10+/Edge */
  user-select: none; /* Standard */
}
.user-title {
  color: #353535;
}
.open {
  padding-right: 10px;
}
.toggled {
  color: #06a798;
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
.active {
  color: #06b1a1;
}
.hidden-checkmark {
  opacity: 0;
}
.suggestion-status-clicked {
  font-weight: bold;
  text-transform: uppercase;
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
@media (max-width: 420px) {
  .title {
    position: initial;
    display: block;
    height: 40px;
    display: none;
  }
  .drop-down-button {
    display: block;
    text-align: left;
    left: 4px;
    margin-left: 20px;
  }
}
</style>
