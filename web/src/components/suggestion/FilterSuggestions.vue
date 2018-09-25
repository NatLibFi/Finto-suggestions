<template>
  <div class="filterSuggestions">
    <h4>Suodata hakutuloksia</h4>
    <span>
      <common-drop-down
        :header="'Käsittelyn tila'"
        :options="suggestionStateStatuses"
        :changeCallBack="stateChanged"
      />
      <common-drop-down
        :header="'Ehdotustyyppi'"
        :options="mapTagsToDropDown()"
        :changeCallBack="tagChanged"
      />
      <common-drop-down
        :header="'Tyyppi'"
        :options="suggestionTypes"
        :changeCallBack="typeChanged"
      />
      <common-drop-down
        :header="'Kokous'"
        :options="mapMeetingsToDropDown()"
        :changeCallBack="meetingChanged"
      />
    </span>
  </div>
</template>

<script>
import CommonDropDown from '../common/CommonDropDown';
import { suggestionStateStatus, suggestionType, filterType } from '../../utils/suggestionMappings.js';

import { suggestionGetters, suggestionMutations } from '../../store/modules/suggestion/suggestionConsts.js';
import { mapSuggestionGetters, mapSuggestioMutations } from '../../store/modules/suggestion/suggestionModule.js';

import { mapMeetingActions, mapMeetingGetters } from '../../store/modules/meeting/meetingModule.js';
import { meetingActions, meetingGetters } from '../../store/modules/meeting/meetingConst.js';

import { mapTagActions, mapTagGetters } from '../../store/modules/tag/tagModule.js';
import { tagActions, tagGetters } from '../../store/modules/tag/tagConst.js';

import { findValueFromDropDownOptions } from '../../utils/dropDownHelper.js'

export default {
  components: {
    CommonDropDown
  },
  data: () => ({
    suggestionStateStatuses: [
      {
        label: suggestionStateStatus.ACCEPTED,
        value: suggestionStateStatus.ACCEPTED
      },
      {
        label: suggestionStateStatus.REJECTED,
        value: suggestionStateStatus.REJECTED
      }],
    suggestionTypes: [
      {
        label: suggestionType.NEW,
        value: suggestionType.NEW
      },
      {
        label: suggestionType.MODIFY,
        value: suggestionType.MODIFY
      }],
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
    ...mapSuggestioMutations({ setFilters: suggestionMutations.SET_FILTERS }),
    stateChanged(value) {
      console.log(value);
    },
    typeChanged(value) {
      console.log(value);
    },
    mapMeetingsToDropDown() {
      let meetings = [];
      this.meetings.forEach(meeting => {
        meetings.push({label: `${meeting.name} ${meeting.meeting_date}`, value: meeting.id});
      });
      return meetings;
    },
    meetingChanged(selected) {
      this.handleSetFilters(selected, filterType.MEETING, this.mapMeetingsToDropDown());
    },
    mapTagsToDropDown() {
      let tags = [];
      this.tags.forEach(tag => {
        tags.push({label: tag.label, value: tag.label });
      });
      return tags;
    },
    tagChanged(selected) {
      this.handleSetFilters(selected, filterType.TAG, this.mapTagsToDropDown());
    },
    handleSetFilters(selectedFilter, filterType, dropDownOptions) {
      if(selectedFilter && selectedFilter.target.value !== '') {
        const selectedValue = findValueFromDropDownOptions(selectedFilter.target.value, dropDownOptions);
        let filters = this.filters;
        filters.push({ type: filterType, value: selectedValue });
        this.setFilters(filters);
      } else {
        const filters = this.filters.filter(f => f.type !== filterType);
        this.setFilters(filters);
      }
    }
  }
};

</script>

<style scoped>
</style>
