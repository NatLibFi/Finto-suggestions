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
          {{ emoji }} abc
        </span>
      </div>
    </div>
  </div>
</template>

<script>
import SvgIcon from '../icons/SvgIcon';
import IconEmoji from '../icons/IconEmoji';
import { directive as onClickaway } from 'vue-clickaway';

import { reactionGetters, reactionActions } from '../../store/modules/reaction/reactionConsts';
import {
  mapReactionGetters,
  mapReactionActions
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
    reactionId: Number
  },
  data() {
    return {
      showEmojiSelector: false,
      emojiMapping,
      temporaryReactionsArray: []
    };
  },
  computed: {},
  ...mapReactionGetters({
    reactions: reactionGetters.GET_REACTIONS
  }),
  methods: {
    ...mapReactionActions({
      addReaction: reactionActions.ADD_REACTION,
      deleteReaction: reactionActions.DELETE_REACTION,
      getReactionsBySuggestion: reactionActions.GET_REACTIONS_BY_SUGGESTION,
      getReactionsByEvent: reactionActions.GET_REACTIONS_BY_EVENT
    }),
    toggleEmojiSelector() {
      this.showEmojiSelector = !this.showEmojiSelector;
    },

    async deleteReactionById(reactionIdPerAction){
      await this.deleteReaction({suggestionId: reactionIdPerAction});
    },


    async addEmoji(emoji) {
//////////////////////////////////////
      if (!this.eventId) {


        // Poisto toimii näillä -----
        // // let tempId = 276;
        // this.reactionId = 277;
        // console.log("this.reactionId" + this.reactionId);
        // // console.log("tempId" + tempId);

        // // this.temporaryReactionsArray = this.getReactionsBySuggestion(this.suggestionId);
        // // this.temporaryReactionsArray = this.getReactionsBySuggestion(this.suggestionId);
        // // for (let index = 0; index < this.getReactionsBySuggestion(this.suggestionId).length; index++) {
        // //   const element = this.getReactionsBySuggestion(this.suggestionId)[index];
        // //   console.log("****************" + element);
        // // }
        // await this.deleteReaction({reactionId: this.reactionId});
        // ------
        
// Älä poista seuraavaa
        await this.addReaction({
          data: {
            code: emoji,
            suggestion_id: this.suggestionId,
            user_id: parseInt(this.userId, 10)
          },
          suggestionId: this.suggestionId
        });


        this.getReactionsBySuggestion(this.suggestionId);
        // this.temporaryReactionsArray = [];


/////////////////////////////////////////
      } else if (this.eventId) {

        // this.temporaryReactionsArray = this.getReactionsBySuggestion(this.suggestionId);
        // this.temporaryReactionsArray = this.getReactionsBySuggestion(this.eventId);
        // for (let index = 0; index < this.getReactionsBySuggestion(this.eventId).length; index++) {
        //   const element = this.getReactionsBySuggestion(this.eventId)[index];
        //   console.log("****************" + element);
        // }


        await this.addReaction({
          data: {
            code: emoji,
            event_id: this.eventId,
            user_id: parseInt(this.userId, 10)
          },
          suggestionId: this.suggestionId
        });
        this.getReactionsByEvent(this.eventId);
        this.temporaryReactionsArray = [];
      }
      this.toggleEmojiSelector();
      this.updateReactionList();
    },
    updateReactionList() {
      this.$emit('updateReactionList');
    }
  }
};



    // async addEmoji(emoji) {
    //   var temporaryReactionsArray = [];




    //   if (!this.eventId) {
    //     await this.addReaction({
    //       data: {
    //         code: emoji,
    //         suggestion_id: this.suggestionId,
    //         user_id: parseInt(this.userId, 10)
    //       },
    //       suggestionId: this.suggestionId
    //     });
    //     this.getReactionsBySuggestion(this.suggestionId);
    //   } else if (this.eventId) {






    //     await this.addReaction({
    //       data: {
    //         code: emoji,
    //         event_id: this.eventId,
    //         user_id: parseInt(this.userId, 10)
    //       },
    //       suggestionId: this.suggestionId
    //     });
    //     this.getReactionsByEvent(this.eventId);
    //   }
    //   this.toggleEmojiSelector();
    //   this.updateReactionList();
    // },












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
