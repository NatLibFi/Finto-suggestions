<template>
  <div class="filterSuggestions">
    <h4>Suodata hakutuloksia</h4>
    <span>
      <common-drop-down :header="'Käsittelyn tila'" :options="suggestionStateStatuses" />
      <common-drop-down :header="'Ehdotustyyppi'" />
      <common-drop-down :header="'Tyyppi'" :options="suggestionTypes" />
      <common-drop-down :header="'Kokous'" />
    </span>
  </div>
</template>

<script>
import CommonDropDown from '../common/CommonDropDown';
import { suggestionStateStatus, suggestionType } from '../../utils/suggestionMappings.js';

import { mapMeetingActions, mapMeetingGetters } from '../../store/modules/meeting/meetingModule.js';
import { meetingActions, meetingGetters } from '../../store/modules/meeting/meetingConst.js';

import { mapTagActions, mapTagGetters } from '../../store/modules/tag/tagModule.js';
import { tagActions, tagGetters } from '../../store/modules/tag/tagConst.js';

export default {
  components: {
    CommonDropDown
  },
  data: () => ({
    suggestionStateStatuses = [suggestionStateStatus.ACCEPTED, suggestionStateStatus.REJECTED],
    suggestionTypes = [suggestionType.NEW, suggestionType.MODIFY],
    ...mapMeetingGetters({ meetings: meetingGetters.GET_MEETINGS }),
    ...mapTagGetters({ tags: tagGetters.GET_TAGS })
  }),
  created() {
    this.getMeetings();
    this.getTags();
  },
  methods: {
    ...mapMeetingActions({ getMeetings: meetingActions.GET_MEETINGS }),
    ...mapTagActions({ getTags: tagActions.GET_TAGS })
  }
};

</script>

<style scoped>
</style>
