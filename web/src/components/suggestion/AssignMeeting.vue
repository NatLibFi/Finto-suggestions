<template>
<div>
  <span v-if="meetingId && meetingId > 0">–
    <a v-if="!meeting" @click="goToMeeting(meetingId)"> Kokous {{ meetingId }}</a>
    <a v-if="meeting && meeting.name" @click="goToMeeting(meetingId)"> {{ meeting.name }}</a>
    <a v-if="isAuthenticated && isAdmin"
      @click="isOpenDropdown = true"> (muokkaa)</a>
  </span>
  <span v-if="!meetingId || meetingId === 0">
    <a v-if="isAuthenticated && isAdmin"
      @click="isOpenDropdown = true">Lisää käsite kokoukseen</a>
  </span>
  <div class="assign-meeting">
    <div class="dropdown-content" v-if="isOpenDropdown" v-on-clickaway="closeDropdown">
      <div class="dropdown-header">Valitse kokous</div>
      <div class="dropdown-filter">
        <input type="text" class="dropdown-filter-input" v-model="searchQuery" />
      </div>
      <div class="dropdown-options">
        <div
          v-for="meeting in filteredMeetings"
          :key="meeting.id"
          @click="assignToMeeting(meeting.id)"
          class="meeting-item">
          <div v-if="meeting.name && meeting.name.length > 0">
            <div class="meeting-title">{{ meeting.name }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import { suggestionActions } from '../../store/modules/suggestion/suggestionConsts';
import { mapSuggestionActions } from '../../store/modules/suggestion/suggestionModule';
import {
  mapMeetingActions,
  mapMeetingGetters,
  mapMeetingMutations
} from '../../store/modules/meeting/meetingModule';
import {
  meetingActions,
  meetingGetters,
  meetingMutations
} from '../../store/modules/meeting/meetingConsts';

import { directive as onClickaway } from 'vue-clickaway';

export default {
  directives: { onClickaway: onClickaway },
  props: {
    suggestion: {
      type: Object,
      required: true
    },
    meetingId: [String, Number],
    isAuthenticated: Boolean,
    isAdmin: Boolean,
    role: String
  },
  data() {
    return {
      isOpenDropdown: false,
      searchQuery: '',
      filteredMeetings: []
    };
  },
  computed: {
    ...mapMeetingGetters({
      meetings: meetingGetters.GET_MEETINGS,
      meeting: meetingGetters.GET_MEETING
    })
  },
  async created() {
    await this.getMeetings();
    if (this.meetingId) {
      await this.getMeeting(this.meetingId);
    }
    this.filteredMeetings = this.meetings;
  },
  mounted() {
    document.body.addEventListener('keyup', e => {
      if (e.keyCode === 27) {
        this.closeDropdown();
      }
    });
  },
  methods: {
    ...mapSuggestionActions({
      assignSuggestionToMeeting: suggestionActions.ASSIGN_SUGGESTION_TO_MEETING
    }),
    ...mapMeetingActions({
      getMeetings: meetingActions.GET_MEETINGS,
      getMeeting: meetingActions.GET_MEETING
    }),
    ...mapMeetingMutations({ setMeetings: meetingMutations.SET_MEETINGS }),
    filterResults() {
      this.getMeetings();
      if (this.searchQuery.length >= 0 && this.meetings) {
        this.filteredMeetings = this.meetings.filter(meeting =>
          meeting.name.toLowerCase().includes(this.searchQuery.toLowerCase())
        );
        this.setMeetings(this.filteredUsers);
      }
    },
    assignToMeeting(id) {
      this.assignSuggestionToMeeting({ suggestionId: this.suggestion.id, meetingId: id });
      this.closeDropdown();
      this.$router.go();
    },
    goToMeeting(id) {
      this.$emit('goToMeeting', id);
    },
    closeDropdown() {
      this.isOpenDropdown = false;
    }
  },
  watch: {
    searchQuery() {
      this.filterResults();
    }
  }
};
</script>

<style scoped>
.assign-meeting {
  position: relative;
  display: inline-block;
}
.assign-meeting a {
  font-size: 14px;
  -webkit-user-select: none; /* Safari */
  -moz-user-select: none; /* Firefox */
  -ms-user-select: none; /* IE10+/Edge */
  user-select: none; /* Standard */
}
.assign-meeting a:hover {
  cursor: pointer;
  cursor: hand;
}
.dropdown-content {
  text-align: center;
  position: absolute;
  top: 22px;
  left: -30%;
  width: 200px;
  height: auto;
  background: #ffffff;
  border: 1px solid #f5f5f5;
  box-sizing: border-box;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
  border-radius: 1px;
  z-index: 10;
}
.dropdown-header {
  font-style: normal;
  font-weight: bold;
  line-height: normal;
  padding: 9px 0 8px 0;
  border-bottom: 1px solid #f5f5f5;
  font-size: 12px;
  color: #444444;
}
.dropdown-filter {
  border-bottom: 1px solid #f5f5f5;
  padding: 10px;
}
input.dropdown-filter-input {
  width: 180px;
  height: 26px;
  left: 10px;
  top: 44px;
  border: 1px solid #e1e1e1;
  box-sizing: border-box;
  border-radius: 1px;
}
.dropdown-options {
  max-height: 180px;
  overflow-x: scroll;
}
.meeting-item {
  text-align: left;
  position: relative;
  height: 42px;
  padding: 0 10px;
}
.meeting-item:hover {
  cursor: pointer;
  background-color: #f3fbfa;
}
.meeting-title {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  margin-left: 2px;
  display: inline-block;
  font-style: normal;
  font-weight: bold;
  line-height: 20px;
  font-size: 13px;
  color: #333333;
}

@media (max-width: 700px) {
  .dropdown-content {
    left: -25%;
  }
}
</style>
