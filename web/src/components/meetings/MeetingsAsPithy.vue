<template>
  <div class="meetings">
    <div>
      <a @click="setPageOk()" unselectable="on">
        Swap the value:
      </a>
      {{ isPageOk }}
      <div v-if='isPageOk'>
        <div v-for='suggestion in suggestions2' :key='suggestion.id' >
          {{ suggestion }}
        </div>
      </div>
    </div>
    <div>
      <a @click="runTheSpeedTest()" unselectable="on">
        Run the store state test:
      </a>
      {{ testSwitcher }}
      <div v-if='testSwitcher'>
        {{ getEntireStoreState }}
      </div>

    </div>
    <div>
      <div>
      <a @click="getTestData(true)" unselectable="on">
        Get Test Data >>
      </a>
      </div>
      <div>
      <a @click="getTestData(false)" unselectable="on">
        Empty >>
      </a>
      </div>
      {{ responseAsString }}
    <div>
    </div>
      <ul>
        <span v-for="meeting in meetings" :key="meeting.id" >
                <h4>*** {{ meeting.name }} / #{{ meeting.id }} ***</h4>
                <li>Luontipäivä: {{ meeting.created }}</li>
                <li>Kokouspäivä: {{ meeting.meeting_date }}</li>
                <a @click="setCurrentMeetingIdForLinkToMeeting(meeting.id), goToSingleMeetingPage()" unselectable="on">Tästä pääset tapaamiseen</a>
                <div>...</div>
        </span>
      </ul>
    </div>
  </div>
</template>

<script>
import SvgIcon from '../icons/SvgIcon';
import IconArrow from '../icons/IconArrow';
import { userRoles } from '../../utils/userHelpers.js';
// eslint-disable-next-line
import { authenticatedUserGetters } from '../../store/modules/authenticatedUser/authenticatedUserConsts.js';
// eslint-disable-next-line
import { mapAuthenticatedUserGetters } from '../../store/modules/authenticatedUser/authenticatedUserModule.js';
import meetingModule, { mapMeetingGetters, mapMeetingActions, mapMeetingMutations } from '../../store/modules/meeting/meetingModule.js';
import { meetingGetters, meetingActions, meetingMutations } from '../../store/modules/meeting/meetingConsts.js';
import store from "../../store/index";
import Vue from 'vue';
import lockr from 'lockr';
import { mapGetters, mapActions, mapMutations, mapState} from 'vuex';

// For speedTesting
import axios from 'axios';

// This component is a playground for code testings

export default {
  components: {
    SvgIcon,
    IconArrow,
  },
  data() {
    return {
      isPageOk: false,
      testSwitcher: false,
      responseAsString: String,
      currentMeetingId: Number,
      tietoToimivuudesta: String, //*
      updateTest: String,
      somethingToManipulate: String,
      somethingToJsonify: String,
      something: String 
    };
  },
  computed: {
    ...mapState('bundledItems', ['suggestions2', 'directives2', 'user2']),
    ...mapAuthenticatedUserGetters({
      isAuthenticated: authenticatedUserGetters.GET_IS_AUTHENTICATED,
      role: authenticatedUserGetters.GET_USER_ROLE
    }),
    ...mapMeetingGetters({
      meetings: meetingGetters.GET_MEETINGS_AS_PITHY,
    }),
    setValueToStoreState: function(value) {
      Vue.set('updateMessage', value);
    },
    getEntireStoreState() {
      this.somethingToManipulate = this.$store.state.bundledItems;
      return this.somethingToManipulate;
    },
  },
  async created() {
    this.$store.dispatch('bundledItems/getSuggestionsFromDBAndCommitState',{
      offset: 0,
      sort: 'CREATED_DESC',
      filters: '',
      searchWord: ''      
    });
    // this.$store.dispatch('bundledItems/setTestValues',{
    //   data: "kattiz",
    // });

    /// Minor
    this.testingOfUpdateHook();
    lockr.prefix = 'meetings_';
    lockr.set('someValue', { name:'Mika' })
    ///
    this.helper();
    await this.getMeetings();
  },
  methods: {
    helper(){
      // console.log(localStorage)
      // localStorage.setItem("currentMeetingId", 0);
    },
    ...mapMeetingActions({
      getMeetings: meetingActions.GET_MEETINGS_AS_PITHY,
    }),
    getStoreStateItem(){
      this.tietoToimivuudesta = store.state.idUsedtoGetCurrentMeeting
    }, //** 
    keyValuePairIsAddedToState(key, value) {
        Vue.set(store.state, key, value);
    }, //** 
    testingOfUpdateHook() {
      localStorage.setItem("updatedHookTest", "globalText4");
    }, //** 
    setCurrentMeetingIdForLinkToMeeting(meetingId) {
      localStorage.setItem("currentMeetingId", meetingId);
    },

    goToSingleMeetingPage() {
      this.$router.push({
        name: 'meetingaspithy',
      });
    },
    setPageOk() {
      if(!this.isPageOk) {
        this.isPageOk = true; 
    } else {
        this.isPageOk = false;
      }
    },
    runTheSpeedTest() {
      if(!this.testSwitcher) {
        this.testSwitcher = true; 
      } else {
        this.testSwitcher = false;
      }
    },
    async getTestData(trueOrFalse) {
      // axios.interceptors.response.use( x => {
      //   x.responseTime = new Date().getTime() - x.config.meta.beginTimer;
      //   return x;
      //   })
      if (true === trueOrFalse) {
        try {
          this.responseAsString = await axios.get('http://localhost:8080/api/suggestions?limit=25&sort=COMMENTS_DESC')
          // .then( x => console.log(x.responseTime));
          // console.log(response);
        } catch (error) {
          console.error(error);
        }        
      } else {
        this.responseAsString = '';
      }

    },
  
  },
  // mounted(){
  //   window.addEventListener("storage", this.getValueFromStoreState);
  // },
  watch: {
    name(newName) {
      localStorage.name = newName;
    }
  }

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
