<template>
  <div class="select-emoji-box">
    <button @click="toggleEmojiSelector">
      <svg-icon icon-name="emoji"><icon-emoji /></svg-icon>
    </button>
    <div v-if="showEmojiSelector" v-on-clickaway="toggleEmojiSelector" class="emoji-selector">
      <div class="emoji-list">
        <span
          v-for="(emoji, index) in emojiMapping"
          @click="addEmoji(index)"
          :key="emoji.id"
          class="single-emoji"
        >
          {{ emoji }}
        </span>
      </div>
    </div>
  </div>
</template>

<script>
import SvgIcon from '../icons/SvgIcon';
import IconEmoji from '../icons/IconEmoji';
import { directive as onClickaway } from 'vue-clickaway';

import { reactionGetters, reactionActions, reactionMutations } from '../../store/modules/reaction/reactionConsts';
import {
  mapReactionGetters,
  mapReactionActions,
  mapReactionMutations
} from '../../store/modules/reaction/reactionModule';

import { emojiMapping } from '../../utils/reactionHelpers';
// eslint-disable-next-line no-unused-vars
import reaction from '../../api/reaction/reaction';

export default {
  components: {
    SvgIcon,
    IconEmoji
  },
  directives: {
    onClickaway: onClickaway
  },
  props: {
    suggestionId: {
      type: [Number, String],
      required: false
    },
    eventId: {
      type: [Number, String],
      required: false
    },
    userId: {
      type: [Number, String],
      required: true
    },
    reactionId: Number,
  },
  data() {
    return {
      showEmojiSelector: false,
      emojiMapping,
      temporaryReactionsArray: []
    };
  },
  computed: {
  ...mapReactionGetters({
      reactions: reactionGetters.GET_REACTIONS
    })
  },
  methods: {
    ...mapReactionActions({
      addReaction: reactionActions.ADD_REACTION,
      deleteReaction: reactionActions.DELETE_REACTION,
      getReactionsBySuggestion: reactionActions.GET_REACTIONS_BY_SUGGESTION,
      getReactionsByEvent: reactionActions.GET_REACTIONS_BY_EVENT
    }),
    ...mapReactionMutations({setReaction: reactionMutations.SET_REACTION}),
    toggleEmojiSelector() {
      this.showEmojiSelector = !this.showEmojiSelector;
    },

    async deleteReactionById(reactionIdPerAction){
      await this.deleteReaction({suggestionId: reactionIdPerAction});
    },

    async addEmoji(emoji) {
      var countOfKeys = ((this.reactions) ? Object.keys(this.reactions).length : countOfKeys = 0); 
      let userIdCount = 0;
      let isSuggestion = false;
      if (!this.eventId) {
        console.log("Eventillä on id, vaikka tarkistus edellyttää, ettei ole: " + this.eventId);
        isSuggestion = true;
      }
      if (countOfKeys > 0) {
        Array.prototype.forEach.call(this.reactions, element => {
          console.log("user_id:t elementissä1 :" + element.user_id);
          console.log("userID komponentissä1 :" + this.userId);
          if (element.user_id == this.userId && element.code == emoji) {
            userIdCount += 1;
          } else {
            userIdCount = 0;
          }
        });
      } // typeof car.color === 'undefined'
      if (typeof this.eventId === 'undefined' && userIdCount == 0) { // was earlier isSuggestion
        await this.addReaction({
          data: {
            code: emoji,
            suggestion_id: this.suggestionId,
            user_id: parseInt(this.userId, 10)
          },
          suggestionId: this.suggestionId
        });
        this.getReactionsBySuggestion(this.suggestionId);        
      } else {
        console.log("User already has added the emoji");  
      }

      if (this.eventId && userIdCount == 0) { // was earlier isSuggestion == false
        console.log("päästiinkö tänne asti? ");
        await this.addReaction({
          data: {
            code: emoji,
            event_id: this.eventId,
            user_id: parseInt(this.userId, 10)
          },
          suggestionId: this.suggestionId
        });
        this.getReactionsByEvent(this.eventId);       
      } else {
        console.log("User already has added the emoji");  
      }
      this.toggleEmojiSelector();
      this.updateReactionList();
    },
    updateReactionList() {
      this.$emit('updateReactionList');
    }
  }
};


</script>

<style scoped>
.select-emoji-box {
  position: relative;
  display: inline-block;
}

.select-emoji-box:focus,
.select-emoji-box button:focus {
  outline: none;
}

.select-emoji-box button {
  background-color: rgba(0, 0, 0, 0);
  border-width: 0;
}

.emoji-selector {
  z-index: 1;
  position: absolute;
  right: 0;
  border: 1px solid #f0f0f0;
  min-height: 72px;
  min-width: 180px;
  margin: 0 0 0 0;
  padding: 5px;
  background-color: #ffffff;
}

.emoji-selector-header {
  border-bottom: 1px solid #f5f5f5;
}

.emoji-selector-header > h4 {
  color: #444444;
  font-size: 9pt;
  text-align: center;
  margin: 5px 0 5px 0;
}

.emoji-list {
  text-align: center;
}

.single-emoji {
  font-size: 24px;
  padding: 2px 6px 2px 10px;
  display: inline-block;
  user-select: none;
}

.single-emoji:hover {
  background-color: #f4f4f4;
  cursor: pointer;
  cursor: hand;
}

@media (max-width: 560px) {
  .emoji-selector {
    right: initial;
  }
}
</style>
