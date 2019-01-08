<template>
<div class="list-container">
  <meeting-list-header
    :futureMeetingCount="futureMeetingCount"
    :pastMeetingCount="pastMeetingCount"
    class="header"
  />
  <ul :class="['list', pageCount > 1 ? 'with-pagionation' : '']">
    <meeting-list-item
      class="item"
      v-for="item in meetings"
      :key="item.id"
      :meeting="item"
      />
  </ul>
  <meeting-list-pagination
    v-if="pageCount > 1"
    :pageCount="pageCount"
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
import { compareDesc, compareAsc, parse, isAfter, isEqual } from 'date-fns';
import meeting from '../../api/meeting/meeting';

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
      paginated_meetings: [],
      futureMeetingCount: 0,
      pastMeetingCount: 0
    }
  },
  async created() {
    await this.getMeetings();
    this.calcultePastAndFutureMeetingCounts();
    this.getSelectedSortKey();
    this.sortMeetingList();
  },
  computed: {
    ...mapMeetingGetters({
      meetings: meetingGetters.GET_MEETINGS,
      selectedSort: meetingGetters.GET_MEETINGS_SELECTED_SORT
    })
  },
  methods: {
    ...mapMeetingActions({
      getMeetings: meetingActions.GET_MEETINGS,
      getSelectedSortKey: meetingActions.GET_MEETINGS_SELECTED_SORT
    }),
    calculatePageCountForPagination: function() {
      return 10;
    },
    sortMeetingList() {
      if(this.selectedSort) {
        if(this.selectedSort === sortingKeys.NEWEST_FIRST) {
          this.meetings.sort(comparerDesc('meeting_date'));
        }
        if(this.selectedSort === sortingKeys.OLDEST_FIRST) {
          this.meetings.sort(comparerAsc('meeting_date'));
        }
      }
    },
    calcultePastAndFutureMeetingCounts() {
      let futureMeetings = [];
      let pastMeetings = [];
      const today = Date();
      this.meetings.forEach(meeting => {
        if (meeting.meeting_date) {
          if (
            isAfter(parse(meeting.meeting_date), today) ||
            isEqual(parse(meeting.meeting_date), today)
          ) {
            futureMeetings.push(meeting);
          } else {
            pastMeetings.push(meeting);
          }
        }
      });
      this.futureMeetingCount = futureMeetings.length;
      this.pastMeetingCount = pastMeetings.length;
    }
  },
  watch: {
    selectedSort() {
      if(this.selectedSort) {
        this.sortMeetingList()
      }
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
</style>
