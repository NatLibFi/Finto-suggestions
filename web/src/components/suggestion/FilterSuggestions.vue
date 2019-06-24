<template>
  <div class="filter-suggestions">
    <h5>
      Suodata hakutuloksia
      <a v-if="filters && filters.length > 0" @click="resetFilters()" class="clear-button">
        Tyhjennä valinnat
      </a>
    </h5>
    <div @click="isDropDownOpened.STATUS = !isDropDownOpened.STATUS" class="filter-item">
      <div :class="[isDropDownOpened.STATUS ? 'selected' : '', 'drop-down-button']">
        <span>Käsittelyn tila</span>
        <svg-icon icon-name="triangle"><icon-triangle /></svg-icon>
      </div>
      <filter-drop-down
        :selectedIndex="selectedOptionIndex.STATUS"
        :isOpened="isDropDownOpened.STATUS"
        :dropDownOptions="suggestionStateStatuses"
        :noOptionsMessage="'Ei valittavia käsittelyn tiloja.'"
        @applyFilter="stateChanged($event)"
        @refreshSelectedIndex="selectedOptionIndex.STATUS = $event"
        @closeDropDown="closeDropDown"
      />
    </div>
    <div @click="isDropDownOpened.TYPE = !isDropDownOpened.TYPE" class="filter-item">
      <div :class="[isDropDownOpened.TYPE ? 'selected' : '', 'drop-down-button']">
        <span>Ehdotustyyppi</span>
        <svg-icon icon-name="triangle"><icon-triangle /></svg-icon>
      </div>
      <filter-drop-down
        :selectedIndex="selectedOptionIndex.TYPE"
        :isOpened="isDropDownOpened.TYPE"
        :dropDownOptions="suggestionTypes"
        :noOptionsMessage="'Käsitetyyppejä ei valittavissa.'"
        @applyFilter="typeChanged($event)"
        @refreshSelectedIndex="selectedOptionIndex.TYPE = $event"
        @closeDropDown="closeDropDown"
      />
    </div>
    <div @click="isDropDownOpened.TAG = !isDropDownOpened.TAG" class="filter-item">
      <div :class="[isDropDownOpened.TAG ? 'selected' : '', 'drop-down-button']">
        <span>Tunniste</span>
        <svg-icon icon-name="triangle"><icon-triangle /></svg-icon>
      </div>
      <multiple-choice-drop-down
        :selectedIndexes="selectedOptionIndex.TAGS"
        :isOpened="isDropDownOpened.TAG"
        :dropDownOptions="mapTagsToDropDown()"
        :noOptionsMessage="'Tunnisteita ei valittavissa.'"
        @applyFilter="tagChanged($event)"
        @addToSelectedIndexes="addSelectedTagIndex($event)"
        @resetTags="resetTags()"
        @closeDropDown="closeDropDown"
      />
    </div>
    <div
      v-if="!meetingId && mapMeetingsToDropDown().length > 0"
      @click="isDropDownOpened.MEETING = !isDropDownOpened.MEETING"
      class="filter-item"
    >
      <div :class="[isDropDownOpened.MEETING ? 'selected' : '', 'drop-down-button']">
        <span>Kokous</span>
        <svg-icon icon-name="triangle"><icon-triangle /></svg-icon>
      </div>
      <filter-drop-down
        :selectedIndex="selectedOptionIndex.MEETING"
        :isOpened="isDropDownOpened.MEETING"
        :dropDownOptions="mapMeetingsToDropDown()"
        :noOptionsMessage="'Ei kokouspäiviä määriteltynä.'"
        @applyFilter="meetingChanged($event)"
        @refreshSelectedIndex="selectedOptionIndex.MEETING = $event"
        @closeDropDown="closeDropDown"
      />
    </div>
  </div>
</template>

<script>
import FilterDropDown from '../common/FilterDropDown';
import MultipleChoiceDropDown from '../common/MultipleChoiceDropDown';
import SvgIcon from '../icons/SvgIcon';
import IconTriangle from '../icons/IconTriangle';

import { filterType, handleQueries, handleMeetingQueries } from '../../utils/suggestionHelpers.js';

import { mapMeetingActions, mapMeetingGetters } from '../../store/modules/meeting/meetingModule.js';
import { meetingActions, meetingGetters } from '../../store/modules/meeting/meetingConsts.js';

import { mapTagActions, mapTagGetters } from '../../store/modules/tag/tagModule.js';
import { tagActions, tagGetters } from '../../store/modules/tag/tagConst.js';

import {
  suggestionType,
  suggestionTypeToString,
  suggestionStateStatus,
  suggestionStateStatusToString
} from '../../utils/suggestionHelpers.js';

export default {
  components: {
    FilterDropDown,
    MultipleChoiceDropDown,
    SvgIcon,
    IconTriangle
  },
  props: {
    meetingId: [String, Number],
    filters: String,
    searchWord: String,
    sort: String
  },
  data: () => ({
    filterStrings: {
      status: '',
      tags: '',
      type: '',
      meeting: ''
    },
    selectedOptionIndex: {
      STATUS: 0, // one always selected
      TAGS: [], // multiple choice
      TYPE: 0, // one always selected
      MEETING: null // no default
    },
    isDropDownOpened: {
      STATUS: false,
      TAG: false,
      TYPE: false,
      MEETING: false
    },
    suggestionStateStatuses: [
      {
        label: 'Kaikki ehdotukset',
        value: null
      },
      {
        label: suggestionStateStatusToString.RECEIVED,
        value: suggestionStateStatus.RECEIVED
      },
      {
        label: suggestionStateStatusToString.READ,
        value: suggestionStateStatus.READ
      },
      {
        label: suggestionStateStatusToString.ACCEPTED,
        value: suggestionStateStatus.ACCEPTED
      },
      {
        label: suggestionStateStatusToString.REJECTED,
        value: suggestionStateStatus.REJECTED
      },
      {
        label: suggestionStateStatusToString.RETAINED,
        value: suggestionStateStatus.RETAINED
      },
      {
        label: suggestionStateStatusToString.ARCHIVED,
        value: suggestionStateStatus.ARCHIVED
      }
    ],
    suggestionTypes: [
      {
        label: 'Kaikki ehdotustyypit',
        value: null
      },
      {
        label: suggestionTypeToString.NEW,
        value: suggestionType.NEW
      },
      {
        label: suggestionTypeToString.MODIFY,
        value: suggestionType.MODIFY
      }
    ]
  }),
  computed: {
    ...mapMeetingGetters({
      meetings: meetingGetters.GET_MEETINGS
    }),
    ...mapTagGetters({
      tags: tagGetters.GET_TAGS
    })
  },
  async created() {
    this.filterStrings = {
      status: '',
      tags: '',
      type: '',
      meeting: ''
    };
    await this.getMeetings();
    await this.getTags();
  },
  methods: {
    ...mapMeetingActions({
      getMeetings: meetingActions.GET_MEETINGS
    }),
    ...mapTagActions({
      getTags: tagActions.GET_TAGS
    }),
    stateChanged(selected) {
      let stateString = this.createFilterString(filterType.STATUS, selected);
      let filters = this.combineStateStrings(filterType.STATUS, stateString);
      if (this.meetingId) {
        handleMeetingQueries(this.meetingId, filters, this.searchWord, this.sort, this.$router);
      } else {
        handleQueries(filters, this.searchWord, this.sort, this.$router);
      }
    },
    meetingChanged(selected) {
      if (this.meetingId) {
        handleMeetingQueries(this.meetingId, this.filters, this.searchWord, this.sort, this.$router);
      } else {
        let stateString = 'meeting_id:' + selected.toString().toLowerCase();
        let filters = this.combineStateStrings(filterType.MEETING, stateString);
        handleQueries(filters, this.searchWord, this.sort, this.$router);
      }
    },
    tagChanged(selected) {
      let filters = this.combineStateStrings(filterType.TAGS, selected);
      if (this.meetingId) {
        handleMeetingQueries(this.meetingId, filters, this.searchWord, this.sort, this.$router);
      } else {
        handleQueries(filters, this.searchWord, this.sort, this.$router);
      }
    },
    typeChanged(selected) {
      let stateString = this.createFilterString(filterType.TYPE, selected);
      let filters = this.combineStateStrings(filterType.TYPE, stateString);
      if (this.meetingId) {
        handleMeetingQueries(this.meetingId, filters, this.searchWord, this.sort, this.$router);
      } else {
        handleQueries(filters, this.searchWord, this.sort, this.$router);
      }
    },
    mapMeetingsToDropDown() {
      let meetings = [];

      if (this.meetings && this.meetings.length > 0) {
        this.meetings.forEach(meeting => {
          if (meeting.meeting_date) {
            meetings.push({
              label: meeting.name,
              value: meeting.id
            });
          }
        });
      }
      return meetings;
    },
    mapTagsToDropDown() {
      let tags = [];
      if (this.tags && this.tags.length > 0) {
        this.tags.forEach(tag => {
          tags.push({ label: tag.label, value: tag.label });
        });
      }
      return tags;
    },
    addSelectedTagIndex(tagIndex) {
      if (this.selectedOptionIndex.TAGS.indexOf(tagIndex) == -1) {
        this.selectedOptionIndex.TAGS.push(tagIndex);
      } else {
        let i = this.selectedOptionIndex.TAGS.indexOf(tagIndex);
        this.selectedOptionIndex.TAGS.splice(i, 1);
      }
    },
    resetTags() {
      this.tagChanged('');
      this.selectedOptionIndex.TAGS = [];
    },
    resetFilters() {
      this.selectedOptionIndex = {
        STATUS: 0,
        TAGS: [],
        TYPE: 0,
        MEETING: null
      };
      this.filterStrings = {
        status: '',
        tags: '',
        type: '',
        meeting: ''
      };
      handleQueries('', this.searchWord, this.sort, this.$router);
      this.hasTouchedFilters = false;
    },
    closeDropDown() {
      this.isDropDownOpened.STATUS = false;
      this.isDropDownOpened.TAG = false;
      this.isDropDownOpened.TYPE = false;
      this.isDropDownOpened.MEETING = false;
    },
    createFilterString(filterType, selected) {
      if (selected) {
        return filterType + ':' + selected.toLowerCase();
      }
      return '';
    },
    combineStateStrings(filter, string) {
      if (this.filters.includes(filter) && string && string.length > 0) {
        let str = this.updateStateString(filter, string);
        if (str.length > 0) {
          return str;
        }
        if (!filterType.TAGS) {
          return string;
        } else {
          return '';
        }
      } else {
        return this.updateStateString(filter, string);
      }
    },
    updateFilterStrings(filter, string) {
      if (filter === filterType.STATUS) {
        this.filterStrings.status = string;
      } else if (filter === filterType.TAGS) {
        this.updateTags();
      } else if (filter === filterType.TYPE) {
        this.filterStrings.type = string;
      } else if (filter === filterType.MEETING) {
        this.filterStrings.meeting = string;
      }
    },
    updateStateString(filter, string) {
      this.updateFilterStrings(filter, string);

      let arr = Object.values(this.filterStrings);
      let str = '';

      for (let i in arr) {
        if (str.length === 0) {
          str = str.concat(arr[i]);
        } else if (str.length > 0 && arr[i].length > 0) {
          str = str.concat('|' + arr[i]);
        }
      }

      return str;
    },
    updateTags() {
      let str = '';

      let indexes = Object.values(this.selectedOptionIndex.TAGS);

      for (let i in this.selectedOptionIndex.TAGS) {
        if (str.length === 0) {
          str = str.concat(this.tags[indexes[i]].label.toLowerCase());
        } else {
          str = str.concat('-', this.tags[indexes[i]].label.toLowerCase());
        }
      }
      if (str.length > 0) {
        this.filterStrings.tags = 'tags:' + str;
      } else {
        this.filterStrings.tags = '';
      }
    },
    findTagIndexByTagName(tag) {
      const tags = this.mapTagsToDropDown();
      if (tags.length > 0) {
        const selectedTag = tags.find(t => t.value === tag);
        return tags.indexOf(selectedTag);
      }
      return -1;
    }
  }
};
</script>

<style scoped>
h5 {
  margin: 0 auto 2px;
}

.clear-button {
  font-size: 12px;
  cursor: pointer;
  cursor: hand;
  -webkit-user-select: none; /* Safari */
  -moz-user-select: none; /* Firefox */
  -ms-user-select: none; /* IE10+/Edge */
  user-select: none; /* Standard */
}

.filter-suggestions {
  width: 100%;
  padding-right: 10px;
  text-align: left;
}

.filter-item {
  position: relative;
  height: 35px;
  width: 135px;
  display: inline-block;
  border: 2px solid #eeeeee;
  margin: 6px 10px 6px 0;
  cursor: pointer;
  cursor: hand;
  transition: border-color 0.1s;
}

.filter-item:hover {
  border-color: #a7e7e1;
}

.drop-down-button {
  position: absolute;
  top: 53.5%;
  left: 14px;
  transform: perspective(1px) translateY(calc(-56% - 0.5px));
  overflow: hidden;
  font-size: 13px;
  font-weight: 600;
  color: #606060;
  cursor: pointer;
  cursor: hand;
  width: 100%;
  -webkit-user-select: none; /* Safari */
  -moz-user-select: none; /* Firefox */
  -ms-user-select: none; /* IE10+/Edge */
  user-select: none; /* Standard */
}

.drop-down-button svg {
  position: absolute;
  top: 66%;
  right: 16px;
  transform: perspective(1px) translateY(calc(-50% - 0.5px));
  display: inline-block;
  height: 16px;
  margin: 0 0 -4px 2px;
}

.selected {
  font-weight: 600;
  color: #111111;
}

@media (max-width: 700px) {
  .filter-item {
    margin: 3px 10px 3px 0;
    height: 40px;
    width: 150px;
  }
}
</style>
