<template>
  <div class="suggestion">
    <div class="arrow-button">
      <a @click="goToHome()" unselectable="on">
        <svg-icon icon-name="arrow"><icon-arrow /></svg-icon>
        Takaisin käsite-ehdotuksiin
      </a>
    </div>

    <div v-if="meetingId" class="meeting-status">
      <div class="meeting-status-container">
        <meeting-status v-if="meetingId" :meetingId="meetingId" />
      </div>
      <div class="meeting-arrow-controls">
        <div class="control">
          « Edellinen<span> käsite</span>
        </div>
        <div class="control">
          Seuraava <span>käsite</span> »
        </div>
      </div>
    </div>

    <div v-if="suggestions && suggestions.length > 0" class="suggestion-container">
      <div class="suggestion-header">
        <div class="suggestion-header-headline">
          <h1 class="suggestion-title">{{ suggestions[0].preferred_label.fi }}</h1>
          <div class="suggestion-header-details">
            <span><strong>#{{ suggestions[0].id }} </strong></span>
            <span>Lähetetty 3 päivää sitten</span>
            <span class="suggestion-type">{{ suggestions[0].suggestion_type }}</span>
            <span class="tag"
              v-if="suggestions[0].tags && suggestions[0].tags.length > 0"
              v-for="tag in suggestions[0].tags"
              :key="tag.label">{{ tag.label }}</span>
          </div>
        </div>
        <div class="suggestion-header-buttons">
          <svg-icon icon-name="more"><icon-more /></svg-icon>
        </div>
      </div>

      <suggestion-content
        v-if="suggestions && suggestions.length > 0"
        :suggestion="suggestions[0]" />

      <div v-if="suggestions && suggestions[0].reactions.length > 0" class="suggestion-reactions">
        <div v-for="reaction in suggestions[0].reactions" :key="reaction.id">
          <div class="reaction">
            <div class="emoji">{{ reaction.code }}</div>
            <div class="counter">2</div>
            <a @click="displayEmoji(reaction.code)">
              button
            </a>
          </div>
        </div>
      </div>
    </div>

    <div v-if="meetingId" class="meeting-actions">
      <meeting-actions 
        :userId="userId"
        :suggestionId="suggestionId"
        :meetingId="meetingId"/>
    </div>

    <div v-if="events && events.length > 0">
      <div v-for="event in events" :key="event.id">
        <suggestion-event
          :event="event"
          :type="event.event_type" />
      </div>
    </div>

    <div class="comment-container">
      <add-comment :userId="userId" :suggestionId="suggestionId" />
    </div>
  </div>
</template>

<script>
import SuggestionContent from './SuggestionContent';
import SuggestionEvent from './SuggestionEvent';
import MeetingStatus from '../meetings/MeetingStatus';
import MeetingActions from '../meetings/MeetingActions';
import IconArrow from '../icons/IconArrow';
import IconMore from '../icons/IconMore';
import SvgIcon from '../icons/SvgIcon';
import AddComment from './AddComment';

import {
  suggestionGetters,
  suggestionActions
} from '../../store/modules/suggestion/suggestionConsts.js';

import {
  mapSuggestionGetters,
  mapSuggestionActions
} from '../../store/modules/suggestion/suggestionModule.js';

import { eventGetters, eventActions } from '../../store/modules/event/eventConsts.js';
import { mapEventGetters, mapEventActions } from '../../store/modules/event/eventModule.js';

export default {
  components: {
    SuggestionContent,
    SuggestionEvent,
    MeetingStatus,
    MeetingActions,
    IconArrow,
    IconMore,
    SvgIcon,
    AddComment
  },
  props: {
    suggestionId: {
      type: [String, Number],
      required: true
    },
    meetingId: {
      type: [String, Number],
      required: false
    }
  },
  data: function() {
    return {
      // eslint-disable-next-line
      userId: this.$cookies.get('logged_user_id')
    }
  },
  computed: {
    ...mapSuggestionGetters({
      suggestions: suggestionGetters.GET_SUGGESTIONS
    }),
    ...mapEventGetters({
      events: eventGetters.GET_EVENTS
    })
  },
  async created() {
    await this.getSuggestions(parseInt(this.suggestionId));
    await this.getEventsBySuggestionId(parseInt(this.suggestionId));
  },
  methods: {
    ...mapSuggestionActions({
      getSuggestions: suggestionActions.GET_SUGGESTION_BY_ID
    }),
    ...mapEventActions({
      getEventsBySuggestionId: eventActions.GET_EVENTS_BY_SUGGESTION_ID
    }),
    goToHome() {
      if (!this.meetingId) {
        this.$router.push('/');
      } else {
        this.$router.push({
          name: 'meeting-suggestion-list',
          params: {
            meetingId: this.meetingId
          }
        })
      }

    }
  }
};
</script>

<style scoped>
.suggestion {
  width: 60vw;
  padding: 40px 20%;
  overflow: hidden;
}

.arrow-button {
  color: #1ea195;
  font-weight: 800;
  font-size: 16px;
  text-align: left;
  margin-left: 6px;
  -webkit-user-select: none; /* Safari */
  -moz-user-select: none; /* Firefox */
  -ms-user-select: none; /* IE10+/Edge */
  user-select: none; /* Standard */
}

.arrow-button a:hover {
  cursor: pointer;
  cursor: hand;
}

.arrow-button svg {
  margin: 0 -15px -27px 0;
  width: 37px;
  height: 37px;
}

.meeting-status {
  margin-bottom: 30px;
}

.meeting-status-container {
  padding: 20px 40px;
  border: 2px solid #f5f5f5;
  background-color: #ffffff;
}

.meeting-arrow-controls {
  position: relative;
  width: 100%;
  margin-top: 6px;
  height: 24px;
}

.meeting-arrow-controls .control {
  display: inline-block;
  cursor: pointer;
  cursor: hand;
  font-size: 15px;
  font-weight: 600;
  color: #06a798;
  position: absolute;
  left: 0;
}

.meeting-arrow-controls .control:last-of-type {
  left: initial;
  right: 0;
}

.suggestion-container {
  background-color: #ffffff;
  border: 2px solid #f5f5f5;
  text-align: left;
}

.suggestion-header {
  margin: 35px 40px 20px;
  position: relative;
}

.suggestion-header-headline {
  line-height: 45px;
  display: inline-block;
  width: 80%;
  height: 100px;
}

h1.suggestion-title {
  display: inline;
  font-weight: 900;
  vertical-align: middle;
  text-transform: lowercase;
  text-transform: capitalize;
}

.suggestion-header-buttons {
  position: absolute;
  top: 0px;
  right: 0px;
  bottom: 0px;
  display: inline-block;
  width: 20%;
  height: 100px;
  text-align: right;
}

.suggestion-type {
  font-size: 14px;
  font-weight: 600;
  background-color: #f2994a;
  color: #ffffff;
  padding: 3px 10px;
  margin-left: 10px;
  border-radius: 2px;
  text-transform: lowercase;
}

.tag {
  font-size: 14px;
  font-weight: 600;
  background-color: #ffffff;
  color: #ac63ef;
  border: 1px solid #ac63ef;
  padding: 3px 10px;
  margin-left: 10px;
  border-radius: 2px;
  text-transform: lowercase;
}

.comment-container {
  background-color: #ffffff;
  border: 2px solid #f5f5f5;
  margin-top: 10px;
}

@media (max-width: 700px) {
  .meeting-arrow-controls .control span {
    display: none;
  }

  .suggestion {
    width: 80vw;
    padding: 10px 10% 20px;
  }

  .suggestion-header-headline,
  .suggestion-header-buttons {
    width: 100%;
    height: initial;
    position: initial;
    text-align: left;
  }

  .suggestion-header-details {
    line-height: 24px;
  }
}
</style>
