<template>
  <div class="meetings">
    Olet nyt saapunut tapaamiseen liittyvälle käsite-ehdotussivulle
    <a @click="setPageOk()" unselectable="on">
      Swap the value:
    </a>
    {{ isPageOk }}
  <div>
    <a @click="goToMeetingsPage()" unselectable="on">Palaa takaisin tapaamilistaukseen</a>
  </div>
  <div>
    <p>Storagesta:</p>
      <!-- <input v-model="jsonTestString.firstName" type="text" />
      <input v-model="jsonTestString.lastName" type="text" />
      <input v-model="jsonTestString.howDoesItFeel" type="text" /> -->
      <input v-model="shouldBeSeenOnTemplate" type="text" />
  </div>
     <!-- -> Model -->
     {{ jsonTestString }}
     <div>>> Tapaaminen: {{ meeting.name }}</div>
     <div>>> Luontipäivä: {{ meeting.created }}</div>
     <div>>> Tapaamispäivä: {{ meeting.meeting_date }}</div>
     <div>>> Tapaamisen id: #{{ meeting.id }}</div>
     <div>>> Tapaamiseen liitetyt käsite-ehdotukset:
      <li v-for="item in meeting.suggestions" :key="item.id">
        {{ item }}
      </li>
    </div>
    <!-- {{ getStoreStateItem() }} -->
    <!--  -->
  </div>
</template>

<script>
import axios from 'axios';
import SvgIcon from '../icons/SvgIcon';
import IconArrow from '../icons/IconArrow';

import { userRoles } from '../../utils/userHelpers.js';
// eslint-disable-next-line
import { authenticatedUserGetters } from '../../store/modules/authenticatedUser/authenticatedUserConsts.js';
// eslint-disable-next-line
import { mapAuthenticatedUserGetters } from '../../store/modules/authenticatedUser/authenticatedUserModule.js';
/// -> Model 
import { mapMeetingGetters, mapMeetingActions } from '../../store/modules/meeting/meetingModule.js';
import { meetingGetters, meetingActions } from '../../store/modules/meeting/meetingConsts.js';
import { mapGetters } from 'vuex';

///
import store from "../../store/index";
import Vue from 'vue';
// import minorStore from 'store-js';
// import store from 'store';
// import { mapState } from 'vuex';
import lockr from 'lockr';

// window.addEventListener("storage", function () {
//     // do your checks to detect
//     // changes in "e1", "e2" & "e3" here
// }, false);

export default {
  components: {
    SvgIcon,
    IconArrow,
  },
  data() {
    return {
      isPageOk: false,
      /// -> Model
      // currentMeetingId: Number,
      ///
      tietoToimivuudesta: String, //*
      jsonTestString: String,
      timer: '',
      test: String,
      shouldBeSeenOnTemplate: String
    };
  },
  computed: {
    ...mapAuthenticatedUserGetters({
      isAuthenticated: authenticatedUserGetters.GET_IS_AUTHENTICATED,
      role: authenticatedUserGetters.GET_USER_ROLE
    }),
    /// -> Model
    ...mapMeetingGetters({
      meeting: meetingGetters.GET_MEETING,
    }),
    ///
    ...mapMeetingGetters({ currentMeetingId: meetingGetters.getMeetingIdForCurrentMeeting }),
    getLockStoreItems(){
      this.jsonTestString = lockr.get('meetings_testingOfJsonData');
    }

    
  },
  // beforeMount(){
  //   this.getSomeDataFromLocalStorage();
  

  // },
  mounted(){
    // ///
    // // setInterval(this.getSomeDataFromLocalStorage(), 1000);
    ///Minor

        /// Minor
    },

  async created() {
    await this.getMeeting(localStorage.getItem("currentMeetingId"));
    // this.jsonTestString = lockr.get('meetings_testingOfJsonData');
    // this.jsonTestString = await this.getSomeDataFromLocalStorage();
    // console.log(lockr.get('meetings_testingOfJsonData'));
    ///
    
    ///
    // this.timer = setInterval(this.getSomeDataFromLocalStorage)
    ///
  },
  updated(){
    this.shouldBeSeenOnTemplate = localStorage.getItem("updatedHookTest")
  },
  // watch: {
  //   jsonTestString(newJsonTestString) {
  //     localStorage.setItem('testingOfJsonData', JSON.stringify(newJsonTestString));
  //     // localStorage.name = newJsonTestString;
  //   }
  // },

// watch: {
//   input: function () {
//     if (isLocalStorage() /* function to detect if localstorage is supported*/) {
//       localStorage.setItem('storedData', this.input)
//     }
//   }
// }

  // watch: {
  //   async code() {
  //     await this.callAuthenticate();
  //   },
  //   isAuthenticated() {
  //     router.push('/');
  //   }
  // }



  methods: {
    /// -> Model
    ...mapMeetingActions({
      getMeeting: meetingActions.GET_MEETING,
    }),
    getStoreStateItem(){
        // return store.state.idUsedtoGetCurrentMeeting
        return this.$store.state
        console.log("Tulostuuko seuraava?");
        // console.log(store.state.idUsedtoGetCurrentMeeting);
    }, //** 
    ///
    goToMeetingsPage() {
      this.$router.push({
        name: 'meetingsaspithy',
      });
    },
    setPageOk() {
      if(!this.isPageOk) {
      this.isPageOk = true; 
    } else {
      this.isPageOk = false;
      }
    },
    getSomeDataFromLocalStorage(){
      // this.test = lockr.get('someValue');
      // console.log(this.test);
      return lockr.get('meetings_testingOfJsonData');
      // console.log(this.jsonTestString);
    // const test = lockr.get('someValue');
    // console.log(test);
    // this.jsonTestString = lockr.get('meetings_testingOfJsonData');
    // console.log(this.jsonTestString);


    // this.jsonTestString = lockr.get('meetings_testingOfJsonData');
      // console.log(this.jsonTestString);
    }
    // getSomeDataFromLocalStorage(){  
    // // const self = this;          
    // this.intervalid1 = setInterval(function(){
    //     this.jsonTestString = JSON.parse(localStorage.getItem('testingOfJsonData'));
    //     // console.log (this.changes);
    // }, 1000);
    // }




          // setTimeout(() => {
          //   this.hasFailed = false;
          //   this.goToFrontPage();
          // }, 2000);


  },
  // mounted(){
  //   this.getSomeDataFromLocalStorage();
  // }

};
</script>

<style scoped>
.meetings {
  width: 20vw;
  margin-top: 20px;
  margin-bottom: 100px;
  margin-right: 0px;
  margin-left: 60px;
  position: absolute;
  left: 1px;
  width: 600px;
  text-align: left;
  /* height: 120px; */
  /* border: 1px solid green; */
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

.meetings-header {
  text-align: left;
  background-color: #ffffff;
  border: 2px solid #f5f5f5;
  padding-left: 0; /* reset inital padding for ul tags */
}

.new-meeting-button {
  cursor: pointer;
  cursor: hand;
  font-size: 14px;
}

.header-content {
  padding: 15px 40px;
}

.header-content p {
  font-weight: 500;
}

@media (max-width: 700px) {
  .meetings {
    width: 80%;
    margin: 40px 10vw 20px;
  }
}
</style>
