<template>
<div class="list-container">
  <meeting-list-header
    :futureMeetingCount="futureMeetingCount"
    :pastMeetingCount="pastMeetingCount"
    class="header"
    @sortListBy="sortMeetingList"
  />
  <ul :class="['list', pageCount > 1 ? 'with-pagionation' : '']">
    <transition-group name="fade">
      <meeting-list-item
        class="item"
        v-for="item in paginated_items"
        :key="item.id"
        :meeting="item"
        />
    </transition-group>
  </ul>
  <meeting-list-pagination
    v-if="pageCount > 1"
    :pageCount="pageCount"
    @paginationPageChanged="console.log('pagination changed')"
  />
</div>
</template>

<script>
import MeetingListHeader from './MeetingListHeader';
import MeetingListItem from './MeetingListItem';
import MeetingListPagination from './MeetingListPagination';

import { mapMeetingGetters, mapMeetingActions } from '../../store/modules/meeting/meetingModule.js';
import { meetingGetters, meetingActions } from '../../store/modules/meeting/meetingConst.js';

import { sortingKeys, comparerDesc, comparerAsc } from '../../utils/sortingHelper.js';
import { compareDesc, compareAsc, parse } from 'date-fns';

export default {
  components: {
    MeetingListHeader,
    MeetingListItem,
    MeetingListPagination
  },
  data: function() {
    return {
      pageCount: 1,
      // TODO: fix pagination
      paginated_items: []
    }
  },
  created() {
    this.getFutureAndPastMeetingCounts();
    this.getMeetings();
  },
  computed: {
    ...mapMeetingGetters({
      futureMeetingCount: meetingGetters.GET_FUTURE_MEETINGS_COUNT,
      pastMeetingCount: meetingGetters.GET_PAST_MEETINGS_COUNT,
      meetings: meetingGetters.GET_MEETINGS
    })
  },
  methods: {
    ...mapMeetingActions({
      getFutureAndPastMeetingCounts: meetingActions.GET_FUTURE_AND_PAST_MEETINGS_COUNT,
      getMeetings: meetingActions.GET_MEETINGS
    }),
    calculatePageCountForPagination: function() {
      return 10;
    },
    sortMeetingList(sort) {
      let meetings = this.meetings;
      if(sort === sortingKeys.NEWEST_FIRST) {
        meetings.sort(comparerDesc('meeting_date'));
      }
      if(sort === sortingKeys.OLDEST_FIRST) {
        meetings.sort(comparerAsc('meeting_date'));
      }
      this.paginated_items = meetings;
    }
  },
  watch: {
    meetings() {
      this.paginated_items = this.meetings;
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.list-container {
  margin-bottom: 40px;
}

ul {
  list-style: none;
}

.list {
  text-align: left;
  background-color: #ffffff;
  border: 2px solid #f5f5f5;
  border-top: none;
  width: 60vw;
  margin: 0 20vw;
  padding-left: 0; /* reset inital padding for ul tags */
}

.with-pagionation {
  border-bottom: none;
}

.item {
  margin: 10px 0 10px 0;
  border-bottom: 2px solid #f5f5f5;
}

@media (max-width: 700px) {
  .list {
    width: 80vw;
    margin: 0 10vw 20px;
  }
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 3s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0.75;
}
</style>
