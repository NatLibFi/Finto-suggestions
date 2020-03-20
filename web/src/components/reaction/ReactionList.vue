<template>
  <div>
    <div class="emoji-list">
      <div v-for="(emoji, index) in emojiList" :key="index" class="single-emoji" name="huihai">
        <!-- <p class="count">{{ userId }}</p> -->
        <span class="count">{{ (emoji.count/emojiList.length) }}</span>
        <span :title="getEmojiSubmittersByReaction(emoji.code)" class="emoji">{{ emojiMapping[emoji.code]}} </span>
      </div>
    </div>
  </div>
</template>

<script>
import { emojiMapping } from "../../utils/reactionHelpers";
import { reactionGetters, reactionActions } from "../../store/modules/reaction/reactionConsts";
import {
  mapReactionGetters,
  mapReactionActions
} from "../../store/modules/reaction/reactionModule";
import { eventActions } from "../../store/modules/event/eventConsts";
import { mapUserGetters, mapUserActions, mapUserMutations } from "../../store/modules/user/userModule";
import { userGetters, userActions, userMutations } from "../../store/modules/user/userConsts";
import reaction from "../../api/reaction/reaction";
export const userNamesInReactionSpanTag = document.getElementById("userNamesInReactionSpanTag");

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
    componentKey: Number,
  },
  data() {
    return {
      emojiMapping,
      emojiList: [],
      filteredUsers: [],
      userNames: [],
      userName: "",
      reactionCodesAndUserIdsArray: {},
      emojiNames: [],
      userNamesToBeInEmoji: [],
      ////
      userIdHelpArray: []
      /////
    };
  },
  computed: {
    ...mapReactionGetters({
      reactions: reactionGetters.GET_REACTIONS
    }),
    ...mapUserGetters({ users: userGetters.GET_USERS }),
  },
  async created() {
    if (this.eventId) {
      await this.reactionsByEvent(this.eventId);
      this.emojiList = this.listCountedEmojis(this.reactions);
    } else {
      await this.reactionsBySuggestion(this.suggestionId);
      this.emojiList = this.listCountedEmojis(this.reactions);
    }
    await this.getUsers();
    this.userNamesToBeInEmoji = this.users;
    this.filteredUsers = this.users;
    await this.getUserNamesForReactions();
  },
  methods: {
    ...mapReactionActions({
      reactionsBySuggestion: reactionActions.GET_REACTIONS_BY_SUGGESTION,
      reactionsByEvent: reactionActions.GET_REACTIONS_BY_EVENT
    }),
    ...mapUserActions({ getUsers: userActions.GET_USERS }),
    ...mapUserMutations({ setUsers: userMutations.SET_USERS }),
    getUserNamesForReactions() {
      // console.log(this.users.length);
      for (let userIndex = 0; userIndex < this.users.length; userIndex++) {
        this.userNames[userIndex] = this.users[userIndex].name;
      }
      return this.userNames;
    },

    getEmojiSubmittersByReaction(emojiCode){
      var tempUserNameResultArray = [];
      var userIdsFromEmoji = this.reactionCodesAndUserIdsArray[emojiCode]; //Emojissa olevat user_id:t
      var usersFromDB = this.userNamesToBeInEmoji; //Kaikki nimet
      if (emojiCode) {
        for (let i = 0; i < usersFromDB.length; i++) {
          if (userIdsFromEmoji.includes(usersFromDB[i].id)) {
            tempUserNameResultArray.push(usersFromDB[i].name);
          } else {
            console.log("UserId in the emoji and the users listing did not match");
          }
        }
        return tempUserNameResultArray; 
      } else {
        tempUserNameResultArray[0] = "Did not find any userNames"
        return tempUserNameResultArray;
      }
    },

    filterDuplicates(arrayToFilter) { 
      return Array.from(new Set(arrayToFilter));;
    },

    listCountedEmojis(reactions) {
      let listedEmojis = [];
      let arr = [];
      //
      let listOfUserIds = [];
      var tempArrayOfCodes = [];
      let keyValuePairsForCodesAndUsers = {};
      for (let index = 0; index < this.reactions.length; index++) {
        const elementAtTheMoment = reactions[index];
        if (!tempArrayOfCodes.includes(elementAtTheMoment.code)) {
          tempArrayOfCodes.push(elementAtTheMoment.code);
        } else {
          console.log("Element already included the used code");
        }
      }
      tempArrayOfCodes.forEach(element => {
        for (let index = 0; index < reactions.length; index++) {
          if (reactions[index].code === element) {
            listOfUserIds.push(reactions[index].user_id);
          }
        }
        keyValuePairsForCodesAndUsers[element] = listOfUserIds;
        //////////////////
        this.reactionCodesAndUserIdsArray[element] = this.filterDuplicates(keyValuePairsForCodesAndUsers[element]);
        /////////////////////
        listOfUserIds = [];
        for (let i = 0; i < reactions.length; i++) {
          if (reactions[i].code in this.emojiMapping) {
            if (listedEmojis.includes(reactions[i].code)) {
              let index = arr.findIndex(emoji => emoji.code === reactions[i].code);
              arr[index].count += 1;
            } else {
              ////
              // console.log("listCountedEmojis(reactions): / user_id: " + reactions[i].user_id + " ja code: " + reactions[i].code);
              ////
              arr.push({
                code: reactions[i].code,
                count: 1,
                id: reactions[i].id,
                user_id: reactions[i].user_id,
                user_id_total: this.filterDuplicates(keyValuePairsForCodesAndUsers[element])
              });
              listedEmojis.push(reactions[i].code);
            }
          }
        }
      });
      return arr;
    }

    // BU
    // listCountedEmojis(reactions) {
    //   let listedEmojis = [];
    //   let arr = [];
    //   for (let i = 0; i < reactions.length; i++) {
    //     if (reactions[i].code in this.emojiMapping) {
    //       if (listedEmojis.includes(reactions[i].code)) {
    //         let index = arr.findIndex(emoji => emoji.code === reactions[i].code);
    //         arr[index].count += 1;
    //       } else {
    //         arr.push({
    //           code: reactions[i].code,
    //           count: 1
    //         });
    //         listedEmojis.push(reactions[i].code);
    //       }
    //     }
    //   }
    //   return arr;
    // }
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
  /* margin-right: 12px; */
  margin-right: 20px;
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
