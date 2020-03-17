<template>
  <div>
    <div class="emoji-list">
      <!-- mika -->
      <!-- <p>
        <span>suggestionId: {{ suggestionId }}</span>
      </p> -->
          <!-- <p>
            <span> Storesta {{ getStoreStateItems() }} </span>
          </p> -->
          <!-- <p>
            <span> userNamesToBeInEmoji {{ userNamesToBeInEmoji }} </span>
          </p> -->
          <!-- <p>
            <span> emojiMapping {{ emojiMapping }} </span>
          </p> -->
      <div v-for="(emoji, index) in emojiList" :key="index" class="single-emoji" name="huihai">
        <span class="count">{{ (emoji.count/emojiList.length) }}</span>

        <!-- Mika -->
        <div>
          <!-- <p>
            <span> fetchName(): {{ fetchName() }} </span>
          </p> -->
          <!-- <p>
            <span> filteredUsers: {{ filteredUsers }} </span>
          </p> -->
          <!-- Toimii -->
          <!-- <p>
            <span> userNames: {{ getUserNamesForReactions() }} </span>
          </p> -->

      <!-- filteredUsers: [],
      filteredUserIdsList: [], -->


          <!-- <p>
            <span> eventId: {{ eventId }} </span>
          </p> -->
          <!-- toimii -->
          <!-- <p>
            <span> Vaihtoehto 0 : {{ reactionCodesAndUserIdsArray }} </span>
          </p> -->
          <!-- yllä oleva toimii -->
          <!-- <p>
            <span> Vaihtoetho 2: reactions: {{ reactions }} </span>
          </p> -->
          <!-- <p>
            <span> kommentin luojan userId: {{ userId }} </span>
          </p> -->
          <!-- <p>
            <span> emojiList {{ emojiList }} </span>
          </p> -->
        </div>

        <span :title="'Käyttäjät: ' + getEmojiSubmittersByReaction2(emoji.code)" class="emoji">{{ emojiMapping[emoji.code]}} </span>
        <!-- <span> {{ getEmojiSubmittersByReaction(emoji.code) }}</span> //Toimiva eli tuo emojin user_id:t -->
        <!-- <span> {{ getEmojiSubmittersByReaction(emoji.code) }}</span> -->
        <!-- <span > {{ getEmojiSubmittersByReaction2(emoji.code) }}</span> TOIMII -->
        <!-- <span :title="'Käyttäjät: ' + getEmojiSubmittersByReaction2(emoji.code)"> {{ getEmojiSubmittersByReaction2(emoji.code) }}</span> -->
        <!-- <span> {{  users }} </span> -->
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

// Mika
import { mapUserGetters, mapUserActions, mapUserMutations } from "../../store/modules/user/userModule";
import { userGetters, userActions, userMutations } from "../../store/modules/user/userConsts";
import reaction from "../../api/reaction/reaction";
// import user from "../../api/user/user";
// import { userActions, userGetters, userMutations } from '../../store/modules/user/userConsts';
// import store from "../../store/index";


// Hae eventit
// Hae
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
    // filteredUsers: String
    // userNamesToBeInEmoji: []
  },
  data() {
    return {
      emojiMapping,
      emojiList: [],
      // Mika
      filteredUsers: [],
      userNames: [],
      userName: "",
      reactionCodesAndUserIdsArray: {},
      emojiNames: [],
      userNamesToBeInEmoji: []
    };
  },
  computed: {
    ...mapReactionGetters({
      reactions: reactionGetters.GET_REACTIONS
    }),
    ...mapUserGetters({ users: userGetters.GET_USERS }),
    

    // Mika
    // ...mapUserGetters({ users: userGetters.GET_USERS })
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
    //Takista alla oleva
    // await this.getFilteredUserIds();
    await this.getUserNamesForReactions();
  },
    // this.getUserNamesForCodes(this.reactions);
    // this.getEmojiSubmittersByReaction

  // },
  methods: {
    ...mapReactionActions({
      reactionsBySuggestion: reactionActions.GET_REACTIONS_BY_SUGGESTION,
      reactionsByEvent: reactionActions.GET_REACTIONS_BY_EVENT
    }),
    ...mapUserActions({ getUsers: userActions.GET_USERS }),
    ...mapUserMutations({ setUsers: userMutations.SET_USERS }),

    // Mika
    // getUserByIdFromStore(id){
    //   return store.state.isHeadersAndIdSetInState
    // },

    // getStoreStateItems(){
    //   return store.state
    // },


    getUserNamesForReactions() {
      console.log(this.users.length);
      for (let userIndex = 0; userIndex < this.users.length; userIndex++) {
        this.userNames[userIndex] = this.users[userIndex].name;
      }
      return this.userNames;
    },

    // filterResults() {
    //   this.getUsers();
    //   if (this.searchQuery.length >= 1) {
    //     this.filteredUsers = this.users.filter(user =>
    //       user.name.toLowerCase().includes(this.searchQuery.toLowerCase())
    //     );
    //     this.setUsers(this.filteredUsers);
    //   }
    // },    
    // getUserNamesByReaction(reaction) {
    //   console.log(this.filteredUsers.length);
    //   for (let userIndex = 0; userIndex < this.filteredUsers.length; userIndex++) {
    //     this.filteredUserIdsList[userIndex] = this.filteredUsers[userIndex].id;
    //   }
    //   return this.filteredUserIdsList;
    // },
    getEmojiSubmittersByReaction(emojiCode){
      if (emojiCode) {
        return this.reactionCodesAndUserIdsArray[emojiCode]; 
      }
    },


    getEmojiSubmittersByReaction2(emojiCode){
      // this.getUsers();
      if (!this.users) {
        console.log("Did not find any user from the DB");
      } else {
        console.log(this.users);
      }
      var tempUserNameResultArray = [];
      var userIdsFromEmoji = this.reactionCodesAndUserIdsArray[emojiCode]; //Emojissa olevat user_id:t
      var usersFromDB = this.userNamesToBeInEmoji; //Kaikki nimet
      console.log(userIdsFromEmoji.length);
      if (emojiCode) {
        for (let i = 0; i < usersFromDB.length; i++) {
          if (userIdsFromEmoji.includes(usersFromDB[i].id)) {
            // userNamesFromDB.includes(userIdsFromEmoji[i].user_id)
            tempUserNameResultArray.push(usersFromDB[i].name);
          } else {
            console.log("UserId in the emoji and the users listing did not match");
          }
        }
        // return this.getUserNamesForReactions
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
      console.log("1. reactions.length: " + reactions.length);

      console.log("Getting codes from the used reactions");
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





























//Testarea ends
      });




      // for (let index = 0; index < reactions.length; index++) {
      //   if (reactions[index].code === 'THUMBS_DOWN') {
      //   // if (reactions[index].code === this.emojiList['code']) {
      //     listOfUserIds.push(reactions[index].user_id)
      //   }
      // }




      // for (let i = 0; i < reactions.length; i++) {
      //   if (reactions[i].code in this.emojiMapping) {
      //     console.log("2. reactions[" + i + "].code: " + String(reactions[i].code));
      //     if (listedEmojis.includes(reactions[i].code)) {
      //       let index = arr.findIndex(emoji => emoji.code === reactions[i].code);
      //       arr[index].count += 1;
      //     } else {
      //       console.log("3. reactions[" + i + "].code ennen pushia: " + String(reactions[i].code));
      //       arr.push({
      //         code: reactions[i].code,
      //         count: 1,
      //         //Mika lisäys
      //         id: reactions[i].id,
      //         user_id: reactions[i].user_id,
      //         user_id_total: reactions[i].code !== 'THUMBS_DOWN' ? []  : this.filterDuplicates(listOfUserIds)
      //         // user_id_total: reactions[i].code !== this.emojiList['code'] ? []  : this.filterDuplicates(listOfUserIds)
      //       });
      //       listedEmojis.push(reactions[i].code);
      //       console.log("4. " + String(reactions[i].code) + " lisättiin listedEmojis-listalle");
      //     }
      //   }
      // }
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
  margin-right: 100px;
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
