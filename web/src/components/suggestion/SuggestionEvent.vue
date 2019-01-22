<template>
<div class="event">
  <div class="event-divider"></div>

  <div class="event-container">
    <div class="event-header">
      <div class="event-user-initials">{{ userNameInitials }}</div>
      <div class="event-info">
        <p class="event-user">
          <span class="user-name">{{ user.name }} </span>
          <span v-if="type == 'ACTION'">
            {{ event.text }}
            <span class="tag">{{ event.value }}</span>
          </span>
        </p>
        <p class="date-sent">{{ dateTimeFormatLabel(this.event.created) }}</p>
      </div>
    </div>
    <div v-if="type == 'COMMENT'" class="event-comment">
      <p>{{ event.text }}</p>
    </div>
  </div>
</div>
</template>

<script>
import { dateTimeFormatLabel } from '../../utils/dateHelper';

import { mapUserGetters, mapUserActions } from '../../store/modules/user/userModule';
import { userGetters, userActions } from '../../store/modules/user/userConsts';
import { userNameInitials } from '../../utils/userHelpers';
import { compineEventTextContent } from '../../utils/eventHelper';

export default {
  props: {
    event: {
      type: Object,
      required: true
    },
    type: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      dateTimeFormatLabel,
      compineEventTextContent,
      userNameInitials: ''
    }
  },
  async created() {
    await this.getUser(this.event.user_id);
    this.fetchUserNameAndInitials();
  },
  computed: {
    ...mapUserGetters({
      user: userGetters.GET_USER
    })
  },
  methods: {
    ...mapUserActions({
      getUser: userActions.GET_USER
    }),
    fetchUserNameAndInitials() {
      if (this.user) {
        this.userNameInitials = userNameInitials(this.user.name);
      }
    }
  }
};
</script>

<style scoped>
div.event-divider {
  display: inline-block;
  text-align: center;
  width: 2px;
  height: 40px;
  margin-top: 20px;
  background-color: #dddddd;
}

div.event-container {
  width: 100%;
  background-color: #ffffff;
  border: 2px solid #f5f5f5;
  text-align: left;
  margin-top: 10px;
}

div.event-header {
  padding: 20px 40px;
}

div.event-header .event-user-initials {
  display: inline-block;
  height: 50px;
  width: 50px;
  background-color: #eeeeee;
  vertical-align: middle;
}

div.event-header .event-info {
  display: inline-block;
  vertical-align: middle;
  margin-left: 20px;
}

div.event-header .event-info p {
  vertical-align: middle;
  margin: 0;
}

div.event-header .event-info .user-name {
  font-weight: 600;
  font-size: 16px;
}

div.event-header .event-info .date-sent {
  font-size: 14px;
}

.event-user-initials {
  display: inline-block;
  height: 35px;
  width: 35px;
  border-radius: 35px;
  line-height: 46px;
  text-align: center;
  background-color: #804af2;
  color: #727272;
  font-size: 20px;
  font-weight: 800;
}

div.event-comment {
  width: 100%;
  border-top: 1px solid #f5f5f5;
  padding: 10px 40px;
  margin: 0;
}

.tag {
  color: #ffffff;
  text-transform: lowercase;
  font-weight: bold;
  background-color: #4794a2;
  border: 2px solid #4794a2;
  padding: 0 6px;
  margin: 4px 4px 0 0;
  border-radius: 2px;
  display: inline-block;
}
.type-new {
  background-color: #1137ff;
  border: 2px solid #1137ff;
}
.type-modify {
  background-color: #ff8111;
  border: 2px solid #ff8111;
}

@media (max-width: 700px) {
  div.event-header {
    padding: 20px;
  }

  div.event-comment {
    padding-left: 20px;
    padding-right: 20px;
  }
}
</style>
