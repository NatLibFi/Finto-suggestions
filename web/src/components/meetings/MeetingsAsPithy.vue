<template>
  <div class="meetings">
    <a @click="setPageOk()" unselectable="on">
      Swap the value:
    </a>
    {{ isPageOk }}
    <div>
      <ul>
        <span v-for="meeting in meetings" :key="meeting.id" >
                <h4>*** {{ meeting.name }} / #{{ meeting.id }} ***</h4>
                <!-- <li>#{{ meeting.id }}</li> -->
                <li>Luontipäivä: {{ meeting.created }}</li>
                <li>Kokouspäivä: {{ meeting.meeting_date }}</li>
        </span>
          <!-- <meeting-list-item class="item" v-for="item in meetings" :key="item.id" :meeting="item" /> -->
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
import { mapMeetingGetters, mapMeetingActions } from '../../store/modules/meeting/meetingModule.js';
import { meetingGetters, meetingActions } from '../../store/modules/meeting/meetingConsts.js';

export default {
  components: {
    SvgIcon,
    IconArrow,
  },
  data() {
    return {
      isPageOk: false,
    };
  },
  computed: {
    ...mapAuthenticatedUserGetters({
      isAuthenticated: authenticatedUserGetters.GET_IS_AUTHENTICATED,
      role: authenticatedUserGetters.GET_USER_ROLE
    }),
    ...mapMeetingGetters({
      meetings: meetingGetters.GET_MEETINGS_AS_PITHY,
    }),
  },
  async created() {
    await this.getMeetings();
  },
  methods: {
    ...mapMeetingActions({
      getMeetings: meetingActions.GET_MEETINGS_AS_PITHY,
    }),
    setPageOk() {
      if(!this.isPageOk) {
      this.isPageOk = true; 
    } else {
      this.isPageOk = false;
      }
    },
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
