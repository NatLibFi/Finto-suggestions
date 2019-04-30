<template>
  <div class="suggestion">
    <div class="arrow-button">
      <a @click="goBack()" unselectable="on">
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
          <div v-if="!noPreviousSuggestions" @click="goToPreviousSuggestion()">
            « Edellinen<span> käsite</span>
          </div>
        </div>
        <div class="control">
          <div v-if="!noNextSuggestions" @click="goToNextSuggestion()">
            Seuraava <span>käsite</span> »
          </div>
        </div>
      </div>
    </div>

    <div v-if="suggestion" class="suggestion-container">
      <div class="suggestion-header">
        <div class="suggestion-header-headline">
          <h1
            v-if="suggestion.preferred_label.fi && suggestion.preferred_label.fi.value"
            class="suggestion-title"
          >
            {{ suggestion.preferred_label.fi.value }}
          </h1>
          <h1
            v-if="suggestion.preferred_label.fi && !suggestion.preferred_label.fi.value"
            class="suggestion-title"
          >
            {{ suggestion.preferred_label.fi }}
          </h1>
          <transition name="fade">
            <div class="suggestion-header-details">
              <span>
                <strong>#{{ suggestion.id }} </strong>
              </span>
              <span>{{ dateTimeFormatLabel(suggestion.created) }}</span>
              <assign-meeting
                @closeDropdown="dropdownOpen = false"
                @goToMeeting="goToMeeting($event)"
                :suggestion="suggestion"
                :meetingId="suggestion.meeting_id"
                :isAuthenticated="isAuthenticated"
                :isAdmin="role === userRoles.ADMIN"
                class="assign-meeting"
              />
            </div>
          </transition>
          <div class="tags">
            <span v-if="suggestion.suggestion_type === suggestionType.NEW" class="tag type-new">
              {{ suggestionTypeToString[suggestion.suggestion_type] }}
            </span>
            <span
              v-if="suggestion.suggestion_type === suggestionType.MODIFY"
              class="tag type-modify"
            >
              {{ suggestionTypeToString[suggestion.suggestion_type] }}
            </span>
            <span
              v-if="suggestion.status === suggestionStateStatus.RECEIVED"
              class="tag status-received"
            >
              {{ suggestionStateStatusToString[suggestionStateStatus.RECEIVED] }}
            </span>
            <span
              v-if="suggestion.status === suggestionStateStatus.READ"
              class="tag status-received"
            >
              {{ suggestionStateStatusToString[suggestionStateStatus.READ] }}
            </span>
            <span
              v-if="suggestion.status === suggestionStateStatus.ACCEPTED"
              class="tag status-accepted"
            >
              {{ suggestionStateStatusToString[suggestionStateStatus.ACCEPTED] }}
            </span>
            <span
              v-if="suggestion.status === suggestionStateStatus.REJECTED"
              class="tag status-rejected"
            >
              {{ suggestionStateStatusToString[suggestionStateStatus.REJECTED] }}
            </span>
            <span
              v-if="suggestion.status === suggestionStateStatus.RETAINED"
              class="tag status-retained"
            >
              {{ suggestionStateStatusToString[suggestionStateStatus.RETAINED] }}
            </span>
            <span
              v-if="suggestion.status === suggestionStateStatus.ARCHIVED"
              class="tag status-retained"
            >
              {{ suggestionStateStatusToString[suggestionStateStatus.ARCHIVED] }}
            </span>
            <span v-if="suggestion.tags && suggestion.tags.length > 0">
              <span v-for="tag in suggestion.tags" :key="tag.label" class="tag">
                {{ tag.label }}
              </span>
            </span>
          </div>
        </div>
        <div class="suggestion-header-buttons" v-if="isAuthenticated && role === userRoles.ADMIN">
          <tag-selector :suggestion="suggestion" :userId="userId" />
          <menu-button :options="menuOptions" name="suggestion-menu" class="menu" ref="menu" />
        </div>
      </div>

      <suggestion-content
        :suggestion="suggestion"
        :user-name="userName"
        :isAuthenticated="isAuthenticated"
        :isAdmin="role === userRoles.ADMIN"
      />
    </div>

    <div v-if="meetingId" class="meeting-actions">
      <meeting-actions
        :userId="userId"
        :suggestionId="suggestionId"
        :meetingId="meetingId"
        :events="events"
        @moveToNextSuggestion="goToNextSuggestion"
      />
    </div>

    <div v-if="events && events.length > 0">
      <div v-for="event in events" :key="event.id">
        <suggestion-event
          :event="event"
          :type="event.event_type"
          :suggestionId="suggestionId"
          :isAuthenticated="isAuthenticated"
        />
      </div>
    </div>

    <div>
      <add-comment :suggestionId="suggestionId" />
    </div>
  </div>
</template>

<script>
import SuggestionContent from './SuggestionContent';
import SuggestionEvent from './SuggestionEvent';
import MeetingStatus from '../meetings/MeetingStatus';
import MeetingActions from '../meetings/MeetingActions';
import IconArrow from '../icons/IconArrow';
import SvgIcon from '../icons/SvgIcon';
import MenuButton from '../common/MenuButton';
import AddComment from './AddComment';
import AssignMeeting from './AssignMeeting';

import {
  suggestionType,
  suggestionTypeToString,
  suggestionStateStatus,
  suggestionStateStatusToString
} from '../../utils/suggestionHelpers';

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

import { userActions, userGetters } from '../../store/modules/user/userConsts';
import { mapUserActions, mapUserGetters } from '../../store/modules/user/userModule';

import { newActionEvent } from '../../utils/tagHelpers';
import { dateTimeFormatLabel } from '../../utils/dateHelper.js';

// eslint-disable-next-line
import { mapAuthenticatedUserGetters, mapAuthenticatedUserActions } from '../../store/modules/authenticatedUser/authenticatedUserModule.js';
// eslint-disable-next-line
import { authenticatedUserGetters, authenticatedUserActions } from '../../store/modules/authenticatedUser/authenticatedUserConsts.js';

import { userRoles } from '../../utils/userHelpers';

import TagSelector from '../tag/TagSelector';

export default {
  components: {
    SuggestionContent,
    SuggestionEvent,
    MeetingStatus,
    MeetingActions,
    IconArrow,
    SvgIcon,
    MenuButton,
    AddComment,
    AssignMeeting,
    TagSelector
  },
  props: {
    suggestionId: {
      type: [String, Number],
      required: true
    },
    meetingId: {
      type: [String, Number],
      default: null
    }
  },
  data() {
    return {
      suggestionTypeToString,
      dateTimeFormatLabel,
      userName: '',
      suggestionType,
      requestedSuggestionId: null,
      dropdownOpen: false,
      noNextSuggestions: false,
      noPreviousSuggestions: false,
      movingAction: {
        NEXT: 'next',
        PREVIOUS: 'previous'
      },
      menuOptions: [
        {
          title: 'Merkitse vastaanotettuksi',
          method: this.markAsReadSuggestion
        },
        {
          title: 'Hylkää ehdotus',
          method: this.rejectSuggestion
        },
        {
          title: 'Arkistoi ehdotus',
          method: this.archiveSuggestion
        }
      ],
      userRoles,
      suggestionStateStatus,
      suggestionStateStatusToString,
      meetingComponentKey: 0
    };
  },
  computed: {
    ...mapSuggestionGetters({
      suggestion: suggestionGetters.GET_SUGGESTION,
      suggestions: suggestionGetters.GET_SUGGESTIONS
    }),
    ...mapEventGetters({
      events: eventGetters.GET_EVENTS
    }),
    ...mapUserGetters({
      user: userGetters.GET_USER
    }),
    ...mapAuthenticatedUserGetters({
      isAuthenticated: authenticatedUserGetters.GET_IS_AUTHENTICATED,
      userId: authenticatedUserGetters.GET_USER_ID,
      role: authenticatedUserGetters.GET_USER_ROLE
    })
  },
  async created() {
    await this.getSuggestionById(parseInt(this.suggestionId));
    await this.getEventsBySuggestionId(parseInt(this.suggestionId));
    await this.getUserName();

    if (this.meetingId) {
      await this.getSuggestionsByMeetingId(this.meetingId);
    }
    this.checkVisibilityOfGoingNextOrPrevious();
  },
  methods: {
    ...mapSuggestionActions({
      getSuggestionById: suggestionActions.GET_SUGGESTION_BY_ID,
      getSuggestionsByMeetingId: suggestionActions.GET_SUGGESTIONS_BY_MEETING_ID,
      setSuggestionStatus: suggestionActions.SET_SUGGESTION_STATUS
    }),
    ...mapEventActions({
      getEventsBySuggestionId: eventActions.GET_EVENTS_BY_SUGGESTION_ID,
      addEvent: eventActions.ADD_NEW_EVENT
    }),
    ...mapUserActions({
      getUser: userActions.GET_USER
    }),
    goBack() {
      if (this.meetingId) {
        this.$router.push(`/meetings/${this.meetingId}`);
      } else {
        this.$router.go(-1);
      }
    },
    goToMeeting(id) {
      this.$router.push({
        name: 'meeting-suggestion-list',
        params: {
          meetingId: id
        }
      });
    },
    async getUserName() {
      if (this.suggestion.user_id) {
        await this.getUser(this.suggestion.user_id);
        this.userName = this.user.name;
      } else {
        this.userName = '';
      }
    },
    goToPreviousSuggestion() {
      this.getNextUsableSuggestionId(this.movingAction.PREVIOUS);
      if (this.requestedSuggestionId) {
        this.$router.push({
          name: 'meeting-suggestion',
          params: {
            suggestionId: this.requestedSuggestionId,
            suggestion: this.suggestion,
            meetingId: this.meetingId
          }
        });
        this.getEventsBySuggestionId(parseInt(this.requestedSuggestionId));
      }
    },
    goToNextSuggestion() {
      if (this.noNextSuggestions) {
        this.$router.push('/meetings/' + this.meetingId);
      } else {
        this.getNextUsableSuggestionId(this.movingAction.NEXT);
        if (this.requestedSuggestionId) {
          this.$router.push({
            name: 'meeting-suggestion',
            params: {
              suggestionId: this.requestedSuggestionId,
              suggestion: this.suggestion,
              meetingId: this.meetingId
            }
          });
          this.getEventsBySuggestionId(parseInt(this.requestedSuggestionId));
        }
      }
    },
    getNextUsableSuggestionId(action) {
      if (this.suggestions && this.suggestions.length > 0) {
        for (let i = 0; this.suggestions.length > i; i++) {
          if (this.suggestions[i].id === parseInt(this.suggestionId)) {
            if (action === this.movingAction.PREVIOUS) {
              if (this.suggestions.length > 1 && i > 0) {
                this.requestedSuggestionId = this.suggestions[i - 1].id;
                break;
              }
            }
            if (action === this.movingAction.NEXT) {
              if (this.suggestions.length - 1 > i) {
                this.requestedSuggestionId = this.suggestions[i + 1].id;
                break;
              }
            }
          }
        }
      }
    },
    checkVisibilityOfGoingNextOrPrevious() {
      if (this.suggestionId && this.suggestions && this.suggestions.length > 0) {
        const element = this.suggestions.find(
          suggestion => suggestion.id === parseInt(this.suggestionId)
        );
        const index = this.suggestions.indexOf(element);

        if (index === 0) {
          this.noPreviousSuggestions = true;
        } else {
          this.noPreviousSuggestions = false;
        }

        if (this.suggestions.length - 1 === index) {
          this.noNextSuggestions = true;
        } else {
          this.noNextSuggestions = false;
        }
      }
    },
    handleOpenTagSelector() {
      this.openTagSelector ? (this.openTagSelector = false) : (this.openTagSelector = true);
    },
    closeMenuDropdown() {
      this.$refs.menu.closeDropdown();
    },
    async createEvent(status) {
      const event = newActionEvent('käsitteli ehdotuksen.', status, this.userId, this.suggestionId);
      await this.addEvent(event);
    },
    async markAsReadSuggestion() {
      await this.setSuggestionStatus({
        suggestionId: this.suggestionId,
        status: suggestionStateStatus.READ
      });
      await this.createEvent(suggestionStateStatus.READ);
      this.closeMenuDropdown();
    },
    async rejectSuggestion() {
      await this.setSuggestionStatus({
        suggestionId: this.suggestionId,
        status: suggestionStateStatus.REJECTED
      });
      await this.createEvent(suggestionStateStatus.REJECTED);
      this.closeMenuDropdown();
    },
    async archiveSuggestion() {
      await this.setSuggestionStatus({
        suggestionId: this.suggestionId,
        status: suggestionStateStatus.ARCHIVED
      });
      await this.createEvent(suggestionStateStatus.ARCHIVED);
      this.closeMenuDropdown();
    }
  },
  watch: {
    async suggestion() {
      await this.getUserName();
    },
    async suggestionId() {
      await this.getSuggestionById(this.suggestionId);
      this.checkVisibilityOfGoingNextOrPrevious();
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
  font-size: 14px;
  text-align: left;
  margin-left: 6px;
  margin-bottom: 2px;
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
  margin: 0 -15px -28px 0;
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
  font-size: 24px;
  vertical-align: middle;
  text-transform: lowercase;
}

.suggestion-header-buttons {
  position: absolute;
  top: 0px;
  right: 0px;
  bottom: 0px;
  display: inline-block;
  width: 30%;
  height: 100px;
  text-align: right;
}

.icon-button {
  margin-left: 20px;
}

.menu {
  margin-left: 20px;
}

.suggestion-header-details {
  line-height: 24px;
  font-size: 13px;
}

.suggestion-header-details span a:hover {
  cursor: pointer;
  cursor: hand;
}

.tags {
  line-height: 20px;
  font-size: 12px;
  font-weight: 900;
  text-transform: lowercase;
  color: #ffffff;
}

.tag {
  background-color: #4794a2;
  border: 2px solid #4794a2;
  padding: 1px 6px 0;
  margin: 4px 4px 0 0;
  border-radius: 2px;
  display: inline-block;
}

.type-new {
  background-color: #1137ff;
  border: 2px solid #1137ff;
}

.type-modify {
  background-color: #ff8111;
  border: 2px solid #ff8111;
}

.status-received {
  background-color: #1137ff;
  border: 2px solid #1137ff;
}

.status-read {
  background-color: #f5f5f5;
  border: 2px solid #f5f5f5;
}

.status-accepted {
  background-color: #58ba81;
  border: 2px solid #58ba81;
}

.status-rejected {
  background-color: #cc4a4a;
  border: 2px solid #cc4a4a;
}

.status-retained {
  background-color: #f2994a;
  border: 2px solid #f2994a;
}

.status-archived {
  background-color: #ad9d8f;
  border: 2px solid #ad9d8f;
}

.comment-container {
  background-color: #ffffff;
  border: 2px solid #f5f5f5;
  margin-top: 10px;
}

.assign-meeting {
  display: inline-block;
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

  .suggestion-header-buttons {
    margin-top: 20px;
  }

  .icon-button {
    margin-left: 0;
    margin-right: 20px;
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>
