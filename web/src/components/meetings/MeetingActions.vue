<template>
  <div v-if="isAuthenticated" class="actions-container">
    <add-comment v-if="events && events.length > 1" :userId="userId" :suggestionId="suggestionId" />
    <div class="action-buttons">
      <span class="button move-to-next-meeting">
        Siirrä seuraavaan<span class="hidden-in-mobile"> kokoukseen</span>
      </span>
      <span class="button dismiss" @click="retainSuggestion()">
        Jätä ehdotukseksi
      </span>
      <span class="button approve" @click="approveSuggestion()">
        Hyväksy ehdotus
      </span>
    </div>
  </div>
</template>

<script>
import AddComment from '../suggestion/AddComment';

import {
  mapAuthenticatedUserGetters,
  mapAuthenticatedUserActions
} from '../../store/modules/authenticatedUser/authenticatedUserModule.js';
import {
  authenticatedUserGetters,
  authenticatedUserActions
} from '../../store/modules/authenticatedUser/authenticatedUserConsts.js';
import { mapSuggestionActions } from '../../store/modules/suggestion/suggestionModule';
import { suggestionActions } from '../../store/modules/suggestion/suggestionConsts';
import { suggestionStateStatus } from '../../utils/suggestionHelpers';
import { newActionEvent } from '../../utils/tagHelpers';
import { mapEventActions } from '../../store/modules/event/eventModule';
import { eventActions } from '../../store/modules/event/eventConsts';
import { mapMeetingMutations } from '../../store/modules/meeting/meetingModule';
import { meetingMutations } from '../../store/modules/meeting/meetingConsts';

export default {
  components: {
    AddComment
  },
  props: {
    userId: [String, Number],
    suggestionId: {
      type: [String, Number],
      required: true
    },
    meetingId: {
      type: [String, Number],
      required: false
    },
    events: {
      type: [Array, Object],
      required: false
    }
  },
  computed: {
    ...mapAuthenticatedUserGetters({
      isAuthenticated: authenticatedUserGetters.GET_IS_AUTHENTICATED
    })
  },
  created() {
    this.validateAuthentication();
  },
  methods: {
    ...mapSuggestionActions({
      setSuggestionStatus: suggestionActions.SET_SUGGESTION_STATUS
    }),
    ...mapAuthenticatedUserActions({
      validateAuthentication: authenticatedUserActions.VALIDATE_AUTHENTICATION
    }),
    ...mapEventActions({
      addEvent: eventActions.ADD_NEW_EVENT
    }),
    ...mapMeetingMutations({
      setMeetingStatus: meetingMutations.SET_UPDATE_MEETING_SUGGESTIONS_PROGRESS_STATUS
    }),
    async createEvent(status) {
      const event = newActionEvent('käsitteli ehdotuksen.', status, this.userId, this.suggestionId);
      await this.addEvent(event);
    },
    async dismissSuggestion() {
      await this.setSuggestionStatus({
        suggestionId: this.suggestionId,
        status: suggestionStateStatus.REJECTED
      });
      await this.createEvent(suggestionStateStatus.REJECTED);
      this.updateMeetingSuggestionStatus();
      this.$emit('moveToNextSuggestion');
    },
    async approveSuggestion() {
      await this.setSuggestionStatus({
        suggestionId: this.suggestionId,
        status: suggestionStateStatus.ACCEPTED
      });
      await this.createEvent(suggestionStateStatus.ACCEPTED);
      this.updateMeetingSuggestionStatus();
      this.$emit('moveToNextSuggestion');
    },
    async retainSuggestion() {
      await this.setSuggestionStatus({
        suggestionId: this.suggestionId,
        status: suggestionStateStatus.RETAINED
      });
      await this.createEvent(suggestionStateStatus.RETAINED);
      this.updateMeetingSuggestionStatus();
      this.$emit('moveToNextSuggestion');
    },
    updateMeetingSuggestionStatus() {
      this.setMeetingStatus(true);
    }
  }
};
</script>

<style scoped>
.actions-container {
  background-color: #ffffff;
  border-top: none;
}

.action-buttons {
  padding: 20px 40px 25px;
  border: 2px solid #f5f5f5;
  border-top: none;
  display: flex;
  justify-content: space-between;
}

.action-buttons .button {
  display: inline-block;
  padding: 6px 12px;
  margin: 0;
  font-weight: 600;
  font-size: 13px;
  border-radius: 2px;
  cursor: pointer;
  cursor: hand;
}

.action-buttons .move-to-next-meeting {
  color: #06a798;
  border: 3px solid #44bdb2;
  margin-right: 12px;
  transition: color, 0.1s;
  transition: border, 0.1s;
}

.action-buttons .move-to-next-meeting:hover {
  color: #44bdb2;
  border: 3px solid #5bcdc3;
}

.action-buttons .dismiss {
  color: #ffffff;
  background-color: #394554;
  border: 3px solid #394554;
  transition: background-color, 0.1s;
  transition: border, 0.1s;
  margin: 0 12px;
  margin-left: auto;
}

.action-buttons .dismiss:hover {
  background-color: #525d6c;
  border: 3px solid #525d6c;
}

.action-buttons .approve {
  color: #ffffff;
  background-color: #237bba;
  border: 3px solid #237bba;
  transition: background-color, 0.1s;
  transition: border, 0.1s;
}

.action-buttons .approve:hover {
  background-color: #3c90cd;
  border: 3px solid #3c90cd;
}

@media (max-width: 700px) {
  .action-buttons {
    padding: 20px 20px 25px;
    display: inline-block;
  }
  .hidden-in-mobile {
    display: none;
  }

  .action-buttons .button {
    text-align: center;
    width: calc(100% - 40px);
    margin-bottom: 8px;
  }

  .action-buttons .dismiss,
  .action-buttons .move-to-next-meeting {
    margin-left: 0;
    margin-right: 0;
  }

  .button:last-of-type {
    margin-bottom: 0;
  }
}
</style>
