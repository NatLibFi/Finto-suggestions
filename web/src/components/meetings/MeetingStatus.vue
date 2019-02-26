<template>
  <div class="status-container">
    <h2 v-if="meeting">Kokous {{ meeting.id }} – {{ meeting.name }}</h2>
    <p>
      <span v-if="meeting && meeting.meeting_date">
        {{ dateTimeFormatLabel(meeting.meeting_date, true) }}
      </span>
      <span v-if="meeting && !meeting.meeting_date">
        Ei asetettua päivämäärää
      </span>
      <span v-if="isAuthenticated && role === userRoles.ADMIN">
        <a
        @click="openMeetingDialog()"
        class="edit-meeting-button">Muokkaa kokousta
        </a>
      </span>
    </p>
    <div class="meeting-status">
      <div class="status-bar">
        <div :style="progressWidth" class="progress-bar"></div>
        <div :style="backgroundWidth" class="progress-background"></div>
      </div>
      <div class="status-summary">
        <p>{{ processed }}/{{ suggestions }} ehdotusta käsitelty ({{ progression }}%)</p>
        <p
          v-if="['meeting-suggestion-list']
            .includes($route.name) && isAuthenticated && continueSuggestionHandle"
          class="next-suggestion-link" @click="goToNextSuggestion()">
          Jatka käsittelyä
        </p>
      </div>
    </div>
    <centered-dialog
      @close="isMeetingDialogOpen = false"
      v-if="isMeetingDialogOpen && isAuthenticated && role === userRoles.ADMIN">
      <meeting-management
        @close="isMeetingDialogOpen = false"
        :isNewMeeting="false"
        :meetingId="meetingId" />
    </centered-dialog>
  </div>
</template>

<script>
import CenteredDialog from '../common/CenteredDialog';
import MeetingManagement from './MeetingManagement';
import { mapMeetingGetters, mapMeetingActions } from '../../store/modules/meeting/meetingModule.js';
import { meetingGetters, meetingActions } from '../../store/modules/meeting/meetingConst.js';

import { userRoles } from '../../utils/userHelpers.js';
// eslint-disable-next-line
import { getMeetingProgressionCounts, getMeetingProgressionWidths } from '../../utils/meetingHelper.js';
// eslint-disable-next-line
import { mapAuthenticatedUserGetters } from '../../store/modules/authenticatedUser/authenticatedUserModule.js';
// eslint-disable-next-line
import { authenticatedUserGetters } from '../../store/modules/authenticatedUser/authenticatedUserConsts.js';
import { mapSuggestionGetters } from '../../store/modules/suggestion/suggestionModule.js';
import { suggestionGetters } from '../../store/modules/suggestion/suggestionConsts.js';
import { dateTimeFormatLabel } from '../../utils/dateHelper';
import { comparerDesc } from '../../utils/sortingHelper.js';

export default {
  components: {
    CenteredDialog,
    MeetingManagement
  },
  props: {
    meetingId: {
      type: [Number, String],
      required: true
    }
  },
  data: function() {
    return {
      statusBarWidth: 0,
      progressWidth: {
        width: `${0}%`
      },
      backgroundWidth: {
        width: `${100}%`
      },
      processed: 0,
      suggestions: 0,
      progression: 0,
      continueSuggestionHandle: true,
      isMeetingDialogOpen: false,
      userRoles,
      dateTimeFormatLabel
    };
  },
  computed: {
    ...mapMeetingGetters({
      meeting: meetingGetters.GET_MEETING
    }),
    ...mapAuthenticatedUserGetters({
      isAuthenticated: authenticatedUserGetters.GET_IS_AUTHENTICATED,
      role: authenticatedUserGetters.GET_USER_ROLE
    }),
    ...mapSuggestionGetters({
      suggestion_items: suggestionGetters.GET_SUGGESTIONS
    })
  },
  async created() {
    await this.getMeeting(this.meetingId);
    this.handleMeetingProgressionCounts(getMeetingProgressionCounts(this.meeting));
    this.checkSuggestionNeededToContinueToHandle();
  },
  methods: {
    ...mapMeetingActions({
      getMeeting: meetingActions.GET_MEETING
    }),
    goToMeetingList() {
      this.$router.push({
        name: 'meeting-suggestion-list',
        params: {
          meetingId: this.meetingId,
          meeting: this.meeting
        }
      });
    },
    goToNextSuggestion() {
      const nextSuggestionId = this.getNextSuggestionIdToHandle();
      if (nextSuggestionId && nextSuggestionId > 0) {
        this.$router.push({
          name: 'meeting-suggestion',
          params: {
            meetingId: this.meetingId,
            suggestionId: nextSuggestionId
          }
        });
      }
    },
    getNextSuggestionIdToHandle() {
      let nextSuggestionId = null;
      if (this.suggestion_items && this.suggestion_items.length > 0) {
        const orderedSuggestionList = this.suggestion_items
          .filter(s => s.status === null)
          .sort(comparerDesc('created'));
        if (orderedSuggestionList && orderedSuggestionList.length > 0) {
          nextSuggestionId = orderedSuggestionList[0].id;
        }
      }
      return nextSuggestionId;
    },
    handleMeetingProgressionCounts(countData) {
      if (countData) {
        this.processed = countData.processed;
        this.suggestions = countData.suggestions;
        this.progression = countData.progression;
      }
    },
    checkSuggestionNeededToContinueToHandle() {
      const nextSuggestionId = this.getNextSuggestionIdToHandle();
      this.continueSuggestionHandle = nextSuggestionId != null ? true : false;
    },
    openMeetingDialog() {
      this.isMeetingDialogOpen = true;
    },
    closeDialog() {
      this.isMeetingDialogOpen = false;
    }
  },
  watch: {
    progression() {
      const meetingProgressionWidths = getMeetingProgressionWidths(this.progression);
      this.progressWidth = meetingProgressionWidths.progressWidth;
      this.backgroundWidth = meetingProgressionWidths.backgroundWidth;
    },
    suggestion_items() {
      this.checkSuggestionNeededToContinueToHandle();
    }
  }
};
</script>

<style scoped>
.status-container {
  position: relative;
  width: 100%;
  text-align: left;
}

.edit-meeting-button {
  cursor: pointer;
  cursor: hand;
}

.meeting-status > div {
  font-size: 14px;
  font-weight: 600;
  vertical-align: middle;
  color: #6a6a6a;
}

.meeting-status .status-bar {
  width: 100%;
  margin-bottom: 4px;
}

.meeting-status .status-bar .progress-bar,
.meeting-status .status-bar .progress-background {
  display: inline-block;
  height: 6px;
  background-color: #eeeeee;
}

.meeting-status .status-bar .progress-bar {
  background-color: #66bea9;
}

.status-summary {
  position: relative;
  height: 40px;
}

.status-summary p {
  display: inline-block;
  position: absolute;
  left: 0;
  margin: 0;
}

.status-summary p.next-suggestion-link {
  left: initial;
  right: 0;
}

.next-suggestion-link {
  color: #06a798;
  cursor: pointer;
  cursor: hand;
}

@media (max-width: 700px) {
  .status-summary {
    position: initial;
    height: initial;
    padding-bottom: 10px;
  }

  .status-summary p {
    display: block;
    position: initial;
    right: initial;
    margin-bottom: 6px;
  }
}
</style>
