<template>
  <div class="filter-suggestions">
    <h4>Suodata hakutuloksia</h4>
    <div @click="isDropDownOpened.STATUS = !isDropDownOpened.STATUS" class="filter-item">
      <div :class="[isDropDownOpened.STATUS ? 'selected' : '', 'drop-down-button']">
        <span>Käsittelyn tila</span>
        <svg-icon icon-name="triangle"><icon-triangle /></svg-icon>
      </div>
      <filter-drop-down 
        :selectedIndex="selectedOptionIndex.STATUS"
        :isOpened="isDropDownOpened.STATUS"
        :dropDownOptions="suggestionStateStatuses"
        :selectedOptionsMapper="suggestionStateStatusMapper"
        :noOptionsMessage="'Ei valittavia käsittelyn tiloja.'"
        @applyFilter="stateChanged($event)"
        @refreshSelectedIndex="selectedOptionIndex.STATUS = $event"
        @closeDropDown="closeDropDown" />
    </div>
    <div 
      @click="isDropDownOpened.TAG = !isDropDownOpened.TAG"
      class="filter-item">
      <div :class="[isDropDownOpened.TAG ? 'selected' : '', 'drop-down-button']">
        <span>Tunniste</span>
        <svg-icon icon-name="triangle"><icon-triangle /></svg-icon>
      </div>
      <multiple-choice-drop-down 
        :selectedIndexes="selectedOptionIndex.TAGS"
        :isOpened="isDropDownOpened.TAG"
        :dropDownOptions="mapTagsToDropDown()"
        :noOptionsMessage="'Ehdotustyyppejä ei valittavissa.'"
        @applyFilter="tagChanged($event)"
        @addToSelectedIndexes="addSelectedTagIndex($event)"
        @resetTags="resetTags()"
        @closeDropDown="closeDropDown" />
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
        :selectedOptionsMapper="suggestionTypeMapper"
        :noOptionsMessage="'Käsitetyyppejä ei valittavissa.'"
        @applyFilter="typeChanged($event)"
        @refreshSelectedIndex="selectedOptionIndex.TYPE = $event"
        @closeDropDown="closeDropDown" />
    </div>
    <div v-if="mapMeetingsToDropDown().length > 0"
      @click="isDropDownOpened.MEETING = !isDropDownOpened.MEETING"
      class="filter-item">
      <div :class="[isDropDownOpened.MEETING ? 'selected' : '', 'drop-down-button']">
        <span>Kokous</span>
        <svg-icon icon-name="triangle"><icon-triangle /></svg-icon>
      </div>
      <!-- TODO: Fix functionality of meeting selection-->
      <filter-drop-down 
        :selectedIndex="selectedOptionIndex.MEETING"
        :isOpened="isDropDownOpened.MEETING"
        :dropDownOptions="mapMeetingsToDropDown()"
        :noOptionsMessage="'Kokouksia ei valittavissa.'"
        @applyFilter="meetingChanged($event)"
        @refreshSelectedIndex="selectedOptionIndex.MEETING = $event"
        @closeDropDown="closeDropDown" />
    </div>
  </div>
</template>

<script>
import FilterDropDown from '../common/FilterDropDown';
import MultipleChoiceDropDown from '../common/MultipleChoiceDropDown';
import SvgIcon from '../icons/SvgIcon';
import IconTriangle from '../icons/IconTriangle';

import {
  suggestionStateStatus,
  suggestionType,
  filterType
} from '../../utils/suggestionMappings.js';

import {
  suggestionGetters,
  suggestionMutations
} from '../../store/modules/suggestion/suggestionConsts.js';
import {
  mapSuggestionGetters,
  mapSuggestionMutations
} from '../../store/modules/suggestion/suggestionModule.js';

import { mapMeetingActions, mapMeetingGetters } from '../../store/modules/meeting/meetingModule.js';
import { meetingActions, meetingGetters } from '../../store/modules/meeting/meetingConst.js';

import { mapTagActions, mapTagGetters } from '../../store/modules/tag/tagModule.js';
import { tagActions, tagGetters } from '../../store/modules/tag/tagConst.js';

import { handleDropDownSelection } from '../../utils/filterValueHelper.js';

// import { format, parse } from 'date-fns';

export default {
  components: {
    FilterDropDown,
    MultipleChoiceDropDown,
    SvgIcon,
    IconTriangle
  },
  props: {
    isMeeting: Boolean
  },
  data: () => ({
    selectedOptionIndex: {
      STATUS: 0, // one always selected
      TAGS: [], // multiple choice
      TYPE: 0, // multiple choice
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
        label: 'Käsittelemätön',
        value: 'NONE'
      },
      {
        label: 'Hyväksytty',
        value: 'ACCEPTED'
      },
      {
        label: 'Hylätty',
        value: 'REJECTED'
      }
    ],
    suggestionStateStatusMapper: {
      ACCEPTED: suggestionStateStatus.ACCEPTED,
      REJECTED: suggestionStateStatus.REJECTED,
      NONE: null
    },
    suggestionTypes: [
      {
        label: 'Kaikki ehdotustyypit',
        value: 'NONE'
      },
      {
        label: 'Käsite-ehdotus',
        value: 'NEW'
      },
      {
        label: 'Käsitemuutos',
        value: 'MODIFY'
      }
    ],
    suggestionTypeMapper: {
      NONE: null,
      NEW: suggestionType.NEW,
      MODIFY: suggestionType.MODIFY
    }
  }),
  computed: {
    ...mapMeetingGetters({ meetings: meetingGetters.GET_MEETINGS }),
    ...mapTagGetters({ tags: tagGetters.GET_TAGS }),
    ...mapSuggestionGetters({ filters: suggestionGetters.GET_FILTERS })
  },
  created() {
    this.getMeetings();
    this.getTags();
  },
  methods: {
    ...mapMeetingActions({ getMeetings: meetingActions.GET_MEETINGS }),
    ...mapTagActions({ getTags: tagActions.GET_TAGS }),
    ...mapSuggestionMutations({ setFilters: suggestionMutations.SET_FILTERS }),
    stateChanged(selected) {
      handleDropDownSelection(
        selected,
        filterType.STATUS,
        this.suggestionStateStatuses,
        this.filters,
        this.setFilters
      );
    },
    typeChanged(selected) {
      handleDropDownSelection(
        selected,
        filterType.TYPE,
        this.suggestionTypes,
        this.filters,
        this.setFilters
      );
    },
    mapMeetingsToDropDown() {
      let meetings = [];
      this.meetings.forEach(meeting => {
        //TODO: format date better with date-fns
        meetings.push({
          label: `${meeting.meeting_date.split('T')[0]}`,
          value: meeting.id
        });
      });
      return meetings;
    },
    meetingChanged(selected) {
      handleDropDownSelection(
        selected,
        filterType.MEETING,
        this.mapMeetingsToDropDown(),
        this.filters,
        this.setFilters
      );
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
    tagChanged(selected) {
      handleDropDownSelection(
        selected,
        filterType.TAG,
        this.mapTagsToDropDown(),
        this.filters,
        this.setFilters
      );
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
      this.selectedOptionIndex.TAGS = [];
    },
    closeDropDown() {
      this.isDropDownOpened.STATUS = false;
      this.isDropDownOpened.TAG = false;
      this.isDropDownOpened.TYPE = false;
      this.isDropDownOpened.MEETING = false;
    }
  }
};
</script>

<style scoped>
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
  transform: perspective(1px) translateY(-50%);
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
  transform: perspective(1px) translateY(-50%);
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
