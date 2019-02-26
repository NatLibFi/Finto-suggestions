<template>
<div class="event">
  <div class="event-divider"></div>

  <div class="event-container">
    <div class="event-header">
      <div class="event-user-initials">{{ userNameInitials }}</div>
      <div class="event-info">
        <p class="event-user">
          <span class="user-name">{{ user.name }} </span>
          <span v-if="type === eventTypes.ACTION">
            {{ event.text }}
            <span class="tag">{{ event.value }}</span>
          </span>
        </p>
        <p class="date-sent">{{ dateTimeFormatLabel(this.event.created) }}</p>
      </div>
      <div
        v-if="isAuthenticated && (role === userRoles.ADMIN || authenticatedUserId === event.user_id )"
        class="menu-wrapper">
        <menu-button
          v-if="type === eventTypes.COMMENT"
          :options="commentOptions"
          ref="menu"
          class="menu" />
        <menu-button
          v-if="type === eventTypes.ACTION"
          :options="actionOptions"
          ref="menu"
          class="menu" />
      </div>
    </div>
    <div v-if="type === eventTypes.COMMENT">
      <div v-if="!isEditable" class="event-comment">
        <p>{{ event.text }}</p>
      </div>
      <div v-if="isEditable" class="edit-comment">
        <markdown-editor
          v-model="event.text"
          ref="markdownEditor"
          :configs="mdeConfigs">
        </markdown-editor>
        <div class="comment-submit">
          <span @click="saveComment" class="submit-button">
            Tallenna
          </span>
        </div>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import MenuButton from '../common/MenuButton';
import { dateTimeFormatLabel } from '../../utils/dateHelper';
import { userRoles } from '../../utils/userHelpers';
import markdownEditor from 'vue-simplemde/src/markdown-editor';

// eslint-disable-next-line
import { mapAuthenticatedUserGetters } from '../../store/modules/authenticatedUser/authenticatedUserModule.js';
// eslint-disable-next-line
import { authenticatedUserGetters } from '../../store/modules/authenticatedUser/authenticatedUserConsts.js';

import { eventTypes } from '../../utils/eventHelper.js';
import { eventActions } from '../../store/modules/event/eventConsts.js';
import { mapEventActions } from '../../store/modules/event/eventModule.js';
import { mapUserGetters, mapUserActions } from '../../store/modules/user/userModule';
import { userGetters, userActions } from '../../store/modules/user/userConsts';
import { userNameInitials } from '../../utils/userHelpers';
import { compineEventTextContent } from '../../utils/eventHelper';

export default {
  components: {
    MenuButton,
    markdownEditor
  },
  props: {
    event: {
      type: Object,
      required: true
    },
    type: {
      type: String,
      required: true
    },
    suggestionId: [String, Number],
    isAuthenticated: Boolean
  },
  data() {
    return {
      content: '',
      mdeConfigs: {
        autofocus: false,
        hideIcons: ['preview', 'fullscreen', 'side-by-side', 'guide'],
        indentWithTabs: false,
        spellChecker: false,
        status: false,
        toolbarTips: true
      },
      isEditable: false,
      dateTimeFormatLabel,
      compineEventTextContent,
      eventTypes,
      userNameInitials: '',
      userRoles,
      commentOptions: [
        {
          title: 'Muokkaa kommenttia',
          method: this.editComment
        },
        {
          title: 'Poista kommentti',
          method: this.removeEvent
        }
      ],
      actionOptions: [
        {
          title: 'Poista tapahtuma',
          method: this.removeEvent
        }
      ]
    };
  },
  async created() {
    await this.getUser(this.event.user_id);
    this.fetchUserNameAndInitials();
  },
  computed: {
    ...mapUserGetters({
      user: userGetters.GET_USER
    }),
    ...mapAuthenticatedUserGetters({
      authenticatedUserId: authenticatedUserGetters.GET_USER_ID,
      role: authenticatedUserGetters.GET_USER_ROLE
    })
  },
  methods: {
    ...mapUserActions({
      getUser: userActions.GET_USER
    }),
    ...mapEventActions({
      patchEvent: eventActions.PATCH_EVENT,
      deleteEvent: eventActions.DELETE_EVENT
    }),
    fetchUserNameAndInitials() {
      if (this.user) {
        this.userNameInitials = userNameInitials(this.user.name);
      }
    },
    closeMenuDropdown() {
      this.$refs.menu.closeDropdown()
    },
    async editComment() {
      this.isEditable = true;
      this.closeMenuDropdown()
    },
    saveComment() {
      this.patchEvent({
        eventId: this.event.id,
        data: { text: this.event.text },
        suggestionId: this.suggestionId
      });
      this.isEditable = false;
    },
    async removeEvent() {
      await this.deleteEvent({ eventId: this.event.id, suggestionId: this.suggestionId });
    }
  }
};
</script>

<style scoped>
.event-divider {
  display: inline-block;
  text-align: center;
  width: 2px;
  height: 40px;
  margin-top: 20px;
  background-color: #dddddd;
}

.event-container {
  background-color: #ffffff;
  border: 2px solid #f5f5f5;
  text-align: left;
  margin-top: 10px;
}

.event-header {
  padding: 20px 40px;
  position: relative;
}

.event-header .event-user-initials {
  display: inline-block;
  height: 40px;
  width: 40px;
  font-size: 15px;
  line-height: 41px;
  background-color: #eeeeee;
  vertical-align: middle;
}

.event-header .event-info {
  display: inline-block;
  vertical-align: middle;
  margin-left: 20px;
  max-width: calc(100% - 60px);
}

.event-header .event-info p {
  vertical-align: middle;
  margin: 0;
}

.event-header .event-info .user-name {
  font-weight: 600;
  font-size: 16px;
}

.event-header .event-info .date-sent {
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

.tag {
  color: #ffffff;
  font-size: 12px;
  line-height: 20px;
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

.menu-wrapper {
  display: inline;
}

.menu {
  position: absolute;
  right: 20px;
}

.event-comment {
  width: 100%;
  border-top: 1px solid #f5f5f5;
  padding: 10px 40px;
  margin: 0;
}

.edit-comment {
  width: calc(100% - 80px);
  border-top: 1px solid #f5f5f5;
  padding: 40px 40px 25px;
  margin: 0;
}

.comment-submit {
  margin: 20px 0 0;
  text-align: right;
}

.submit-button {
  background-color: #06a798;
  border: none;
  border-radius: 2px;
  color: white;
  padding: 8px 16px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  cursor: hand;
  transition: background-color 0.1s;
  margin: 0;
}

.submit-button:hover {
  background-color: #44bdb2;
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
