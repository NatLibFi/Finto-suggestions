<template>
<div class="list-container">
  <meeting-list-header
    :futureMeetingCount="futureMeetingCount"
    :pastMeetingCount="pastMeetingCount"
    class="header" />
  <ul :class="['list', pageCount > 1 ? 'with-pagionation' : '']">
    <meeting-list-item
      class="item"
      v-for="item in paginated_items"
      :key="item.id"
      :meeting="item"
      />
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

export default {
  components: {
    MeetingListHeader,
    MeetingListItem,
    MeetingListPagination
  },
  data: function() {
    return {
      pageCount: 1,
      // TODO: use store to get real meetings
      paginated_items: [
        {
          id: 1,
          name: 'YSA-kokous 2018/4 – Ongelmakokous',
          created: '2018-11-20T17:19:31.114000Z',
          modified: '2018-11-20T17:19:31.114000Z',
          meeting_date: '2018-12-24T10:00:31.114000Z'
        },
        {
          id: 2,
          name: 'YSA-kokous 2019/1',
          created: '2018-11-20T17:19:31.114000Z',
          modified: '2018-11-20T17:19:31.114000Z',
          meeting_date: '2019-02-13T10:00:31.114000Z'
        },
      ]
    }
  },
  created() {
    this.getFutureAndPastMeetingCounts();
  },
  computed: {
    ...mapMeetingGetters({
      futureMeetingCount: meetingGetters.GET_FUTURE_MEETINGS_COUNT,
      pastMeetingCount: meetingGetters.GET_PAST_MEETINGS_COUNT
    })
  },
  methods: {
    ...mapMeetingActions({
      getFutureAndPastMeetingCounts: meetingActions.GET_FUTURE_AND_PAST_MEETINGS_COUNT
    }),
    calculatePageCountForPagination: function() {
      return 10;
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
