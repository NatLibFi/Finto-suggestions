<template>
  <li @click="goToSuggestion()" class="item">
    <div class="item-summary">
      <div class="title">
        <p class="title-row">
          <span class="item-name">{{ suggestion.preferred_label.fi }}</span>
          <span
            :class="[suggestionTypeToStyleClass[suggestion.suggestion_type], 'tag']">{{ suggestionTypeToString[suggestion.suggestion_type] }}
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
          Lähetetty {{ buildLabel() }}
        </p>
      </div>
    </div>
    <div class="item-comments" v-if="suggestion.events.filter((event) => event.event_type === eventTypes.COMMENT).length > 0">
      <svg-icon icon-name="comments"><icon-comments /></svg-icon>
      <span>{{ suggestion.events.filter((event) => event.event_type === eventTypes.COMMENT).length }}</span>
    </div>
  </li>
</template>

<script>
import SvgIcon from '../icons/SvgIcon';
import IconComments from '../icons/IconComments';
import { suggestionTypeToStyleClass, suggestionTypeToString } from '../../utils/suggestionMappings';
import { dateDiffLabel } from '../../utils/dateTimeStampHelper';
import { eventTypes } from '../../utils/eventMappings';

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
    meetingId: [String, Number]
  },
  data:() => ({
    //not the best way but seems that you cannot use imported module straight inside class binding clause
    suggestionTypeToStyleClass,
    suggestionTypeToString,
    eventTypes
  }),
  methods: {
    buildLabel() {
      return dateDiffLabel(this.suggestion.created);
    },
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
        })
      }
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
  line-height: 26px;
}
.item-name {
  font-size: 17px;
  margin-right: 8px;
  vertical-align: middle;
}
.tag {
  font-weight: 600;
  text-transform: lowercase;
  font-size: 14px;
  padding: 0 6px;
  border-radius: 3px;
  color: #ffffff;
  margin-right: 10px;
}

.tag:last-of-type {
  margin-right: 0;
}
.type-new {
  background-color: #1137ff;
  border: 2px solid #1137ff;
}
.type-modify {
  background-color: #ff8111;
  border: 2px solid #ff8111;
}
.tags {
  color: #ac63ef;
  background-color: white;
  border: 2px solid #ac63ef;
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
