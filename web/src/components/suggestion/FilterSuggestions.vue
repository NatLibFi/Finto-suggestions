<template>
  <div class="filterSuggestions">
    <h4>Suodata hakutuloksia</h4>
    <ul>
      <li>
        <common-drop-down
          :header="'Käsittelyn tila'"
          :options="suggestionStateStatuses"
          :changeCallBack="stateChanged"
        />
      </li>
      <li>
        <common-drop-down
          :header="'Ehdotustyyppi'"
          :options="mapTagsToDropDown()"
          :changeCallBack="tagChanged"
        />
      </li>
      <li>
        <common-drop-down
          :header="'Tyyppi'"
          :options="suggestionTypes"
          :changeCallBack="typeChanged"
        />
      </li>
      <li>
        <common-drop-down
          :header="'Kokous'"
          :options="mapMeetingsToDropDown()"
          :changeCallBack="meetingChanged"
        />
      </li>
    </ul>
  </div>
</template>

<script>
import CommonDropDown from '../common/CommonDropDown';
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
      }
    ],
    suggestionTypes: [
      {
        label: suggestionType.NEW,
        value: suggestionType.NEW
      },
      {
        label: suggestionType.MODIFY,
        value: suggestionType.MODIFY
      }
    ]
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

      if (this.meetings && this.meetings.length > 0) {
        this.meetings.forEach(meeting => {
          //TODO: format date better with date-fns
          meetings.push({
            label: `${meeting.name} ${meeting.meeting_date.split('T')[0]}`,
            value: meeting.id
          });
        });
      }

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

      if (this.tags && this.tags.lenght > 0) {
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
    }
  }
};
</script>

<style scoped>
div.filterSuggestions ul {
  width: 100%;
  padding: 10px;
  text-align: left;
}

div.filterSuggestions ul > li {
  display: inline-block;
  margin: 5px;
  padding: 10px;
  vertical-align: top;
  width: 150px;
}
</style>
