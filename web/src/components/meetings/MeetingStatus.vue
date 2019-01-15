<template>
  <div class="status-container">
    <!-- TODO: get meeting from store and show meeting.name only-->
    <h2 v-if="meeting">Kokous {{ meeting.id }} – {{ meeting.name }}</h2>
    <div class="meeting-status">
      <div class="status-bar">
        <div :style="progressWidth" class="progress-bar"></div>
        <div :style="backgroundWidth" class="progress-background"></div>
      </div>
      <div class="status-summary">
        <p>{{ processed }}/{{ suggestions }} ehdotusta käsitelty ({{ progression }}%)</p>
        <p
          v-if="['meeting-suggestion-list'].includes($route.name) && isAuthenticated && continueSuggestionHandle"
          class="next-suggestion-link" @click="goToNextSuggestion()">
          Jatka käsittelyä
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import { mapMeetingGetters, mapMeetingActions } from '../../store/modules/meeting/meetingModule.js';
import { meetingGetters, meetingActions } from '../../store/modules/meeting/meetingConst.js';

import { getMeetingProgressionCounts, getMeetingProgressionWidths } from '../../utils/meetingHelper.js';
import { mapAuthenticatedUserGetters } from '../../store/modules/authenticatedUser/authenticatedUserModule.js';
import { authenticatedUserGetters } from '../../store/modules/authenticatedUser/authenticatedUserConsts.js';
import { mapSuggestionGetters } from '../../store/modules/suggestion/suggestionModule.js';
import { suggestionGetters } from '../../store/modules/suggestion/suggestionConsts.js';
import { comparerDesc } from '../../utils/sortingHelper.js';

export default {
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
      continueSuggestionHandle: true
    }
  },
  computed: {
    ...mapMeetingGetters({
      meeting: meetingGetters.GET_MEETING
    }),
    ...mapAuthenticatedUserGetters({
      isAuthenticated: authenticatedUserGetters.GET_AUTHENTICATION
    }),
    ...mapSuggestionGetters({
      suggestion_items: suggestionGetters.GET_SUGGESTIONS
    })
  },
  async created() {
    await this.getMeeting(this.meetingId);
    this.handleMeetingProgressionCounts(
      getMeetingProgressionCounts(
        this.meeting
    ));
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
      if(nextSuggestionId && nextSuggestionId > 0) {
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
        const orderedSuggestionList = this.suggestion_items.filter(s => s.status === null).sort(comparerDesc('created'));
        if(orderedSuggestionList && orderedSuggestionList.length > 0) {
          nextSuggestionId = orderedSuggestionList[0].id
        }
      }
      console.log(nextSuggestionId);
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
.meeting-status .status-bar .progress-background
{
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
