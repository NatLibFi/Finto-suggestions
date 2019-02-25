<template>
  <li @click="goToSuggestion()" class="item">
    <div class="item-summary">
      <div class="title">
        <p class="title-row">
          <span v-if="suggestion.preferred_label.fi && suggestion.preferred_label.fi.value" class="item-name">
            {{ suggestion.preferred_label.fi.value }}
          </span>
          <span v-else class="item-name">
            {{ suggestion.preferred_label.fi }}
          </span>
          <span
            :class="[suggestionTypeToStyleClass[suggestion.suggestion_type], 'tag']">
            {{ suggestionTypeToString[suggestion.suggestion_type] }}
          </span>
            <span
              v-if="suggestion.status === suggestionStateStatus.RECEIVED"
              class="tag status-received">{{ suggestionStateStatusToString[suggestionStateStatus.RECEIVED] }}
            </span>
            <span
              v-if="suggestion.status === suggestionStateStatus.READ"
              class="tag status-received">{{ suggestionStateStatusToString[suggestionStateStatus.READ] }}
            </span>
            <span
              v-if="suggestion.status === suggestionStateStatus.ACCEPTED"
              class="tag status-accepted">{{ suggestionStateStatusToString[suggestionStateStatus.ACCEPTED] }}
            </span>
            <span
              v-if="suggestion.status === suggestionStateStatus.REJECTED"
              class="tag status-rejected">{{ suggestionStateStatusToString[suggestionStateStatus.REJECTED] }}
            </span>
            <span
              v-if="suggestion.status === suggestionStateStatus.RETAINED"
              class="tag status-retained">{{ suggestionStateStatusToString[suggestionStateStatus.RETAINED] }}
            </span>
            <span
              v-if="suggestion.status === suggestionStateStatus.ARCHIVED"
              class="tag status-retained">{{ suggestionStateStatusToString[suggestionStateStatus.ARCHIVED] }}
            </span>
          <span v-if="suggestion.tags.length > 0">
            <span class="tags tag" v-for="tag in suggestion.tags" :key="tag.label">
              {{ tag.label}}
            </span>
          </span>
        </p>
      </div>
      <div class="label">
        <p>
          <strong>#{{ suggestion.id }}</strong>
          {{ dateTimeFormatLabel(suggestion.created) }} –
          <span>
            <a @click.stop="goToMeeting(suggestion.meeting_id)">
              Kokous {{ suggestion.meeting_id }}
            </a>
          </span>
        </p>
      </div>
    </div>
    <div
      v-if="suggestion.events.filter((event) => event.event_type === eventTypes.COMMENT).length > 0"
      class="item-comments">
      <svg-icon icon-name="comments"><icon-comments /></svg-icon>
      <span>
        {{ suggestion.events.filter((event) => event.event_type === eventTypes.COMMENT).length }}
      </span>
    </div>
  </li>
</template>

<script>
import SvgIcon from '../icons/SvgIcon';
import IconComments from '../icons/IconComments';
import {
  suggestionTypeToStyleClass,
  suggestionTypeToString,
  suggestionStateStatus,
  suggestionStateStatusToString
} from '../../utils/suggestionHelpers';
import { dateTimeFormatLabel } from '../../utils/dateHelper';
import { eventTypes } from '../../utils/eventHelper';

export default {
  components: {
    SvgIcon,
    IconComments
  },
  props: {
    suggestion: {
      type: Object,
      required: true
    },
    meetingId: {
      type: [Number, String],
      default: null
    }
  },
  data: () => ({
    suggestionTypeToStyleClass,
    suggestionTypeToString,
    eventTypes,
    dateTimeFormatLabel,
    suggestionStateStatus,
    suggestionStateStatusToString
  }),
  methods: {
    goToSuggestion() {
      if (!this.meetingId) {
        this.$router.push({
          name: 'suggestion',
          params: {
            suggestionId: this.suggestion.id,
            suggestion: this.suggestion
          }
        });
      } else {
        this.$router.push({
          name: 'meeting-suggestion',
          params: {
            suggestionId: this.suggestion.id,
            suggestion: this.suggestion,
            meetingId: this.meetingId
          }
        });
      }
    },
    goToMeeting(id) {
      this.$router.push({
        name: 'meeting-suggestion-list',
        params: {
          meetingId: id
        }
      });
    }
  }
};
</script>

<style scoped>
p {
  margin: 0;
}
li.item {
  position: relative;
  width: 100%;
  height: 100%;
  margin: 0;
  cursor: pointer;
  cursor: hand;
  overflow: hidden;
  transition: background-color, 0.1s;
}
li.item:hover {
  background-color: #f3fbfa;
}
.item-summary {
  padding: 10px 30px 10px;
  width: calc(100% - 130px);
  overflow: hidden;
}
.title {
  font-weight: 600;
  margin: 5px;
}
.title-row {
  line-height: 20px;
}
.item-name {
  font-size: 16px;
  margin-right: 8px;
  vertical-align: middle;
}
.tag {
  text-transform: lowercase;
  font-size: 12px;
  font-weight: 900;
  padding: 0 6px;
  border-radius: 3px;
  margin-right: 10px;
  margin: 4px 4px 0 0;
  display: inline-block;
  color: #ffffff;
}
.tag:last-of-type {
  margin-right: 0;
}
.tags {
  background-color: #4794a2;
  border: 2px solid #4794a2;
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

.label {
  font-size: smaller;
  padding-left: 5px;
}
.item-comments {
  position: absolute;
  top: 50%;
  right: 30px;
  transform: perspective(1px) translateY(-50%);
  vertical-align: middle;
  height: 24px;
  color: #a4a4a4;
}
.item-comments span {
  font-size: 14px;
  font-weight: 600;
  vertical-align: middle;
}
.item-comments svg {
  height: 16px;
  margin-right: 8px;
  vertical-align: middle;
}

@media (max-width: 700px) {
  .item-summary {
    padding: 10px 20px 10px;
  }
  .item-name {
    display: block;
  }
}
</style>
