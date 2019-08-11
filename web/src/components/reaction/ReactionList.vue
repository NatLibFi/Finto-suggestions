<template>
  <div>
    <div class="emoji-list">
      <div v-for="(emoji, index) in emojiList" :key="index" class="single-emoji">
        <span class="count">{{ emoji.count }}</span>
        <span class="emoji">
          {{ emojiMapping[emoji.code] }}
        </span>
      </div>
    </div>
  </div>
</template>

<script>
import { emojiMapping } from '../../utils/reactionHelpers';
import { reactionGetters, reactionActions } from '../../store/modules/reaction/reactionConsts';
import {
  mapReactionGetters,
  mapReactionActions
} from '../../store/modules/reaction/reactionModule';

export default {
  props: {
    suggestionId: {
      type: [String, Number],
      required: false
    },
    eventId: {
      type: [String, Number],
      required: false
    },
    userId: {
      type: [String, Number],
      required: false
    },
    componentKey: Number
  },
  data() {
    return {
      emojiMapping,
      emojiList: []
    };
  },
  computed: {
    ...mapReactionGetters({
      reactions: reactionGetters.GET_REACTIONS
    })
  },
  async created() {
    if (this.eventId) {
      await this.reactionsByEvent(this.eventId);
      this.emojiList = this.listCountedEmojis(this.reactions);
    } else {
      await this.reactionsBySuggestion(this.suggestionId);
      this.emojiList = this.listCountedEmojis(this.reactions);
    }
  },
  methods: {
    ...mapReactionActions({
      reactionsBySuggestion: reactionActions.GET_REACTIONS_BY_SUGGESTION,
      reactionsByEvent: reactionActions.GET_REACTIONS_BY_EVENT
    }),
    listCountedEmojis(reactions) {
      let listedEmojis = [];
      let arr = [];
      for (let i = 0; i < reactions.length; i++) {
        if (reactions[i].code in this.emojiMapping) {
          if (listedEmojis.includes(reactions[i].code)) {
            let index = arr.findIndex(emoji => emoji.code === reactions[i].code);
            arr[index].count += 1;
          } else {
            arr.push({
              code: reactions[i].code,
              count: 1
            });
            listedEmojis.push(reactions[i].code);
          }
        }
      }
      return arr;
    }
  }
};
</script>

<style scoped>
.emoji-list {
  font-size: 16px;
  min-height: 45px;
  position: relative;
}

.single-emoji {
  display: inline-block;
  width: 50px;
  height: 40px;
  margin-right: 12px;
  position: relative;
}

.count {
  position: absolute;
  top: 50%;
  left: 0;
  transform: translateY(-50%);
}

.emoji {
  font-size: 24px;
  position: absolute;
  top: 50%;
  left: 20px;
  transform: translateY(-50%);
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
