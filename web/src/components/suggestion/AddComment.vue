<template>
<div class="comment">
  <div class="comment-divider"></div>

  <div class="comment-container">
    <div class="comment-header">
      <div class="comment-info">
        <p>Kommentoi ehdotusta</p>
      </div>
    </div>

    <div class="comment-box">
        <markdown-editor v-model="content" ref="markdownEditor"></markdown-editor>
    </div>
    <div class="comment-submit">
      <span>
        <button class="submitButton" @click="saveNewComment">Lähetä</button>
      </span>
    </div>
  </div>
</div>

</template>

<script>
import markdownEditor from 'vue-simplemde/src/markdown-editor';

import { mapEventActions } from '../../store/modules/event/eventModule.js';
import { eventActions } from '../../store/modules/event/eventConsts.js';
import { eventTypes } from '../../utils/eventMappings.js';

import { mapUserGetters, mapUserActions } from '../../store/modules/user/userModule.js';
import { userGetters, userActions } from '../../store/modules/user/userConsts.js';

export default {
  props: {
    suggestionId: {
      type: [String, Number],
      required: true
    }
  },
  components: {
    markdownEditor
  },
  data: () => ({
    content: ''
  }),
  computed: {
    ...mapUserGetters({ userId: userGetters.GET_USER_ID })
  },
  methods: {
    ...mapEventActions({
      addNewEvent: eventActions.ADD_NEW_EVENT
    }),
    constructEventJsonObject() {
      if (this.userId > 0 && this.suggestionId > 0) {
        return {
          event_type: eventTypes.COMMENT,
          text: this.content,
          user_id: parseInt(this.userId),
          suggestion_id: parseInt(this.suggestionId)
        };
      }
      return null;
    },
    saveNewComment() {
      this.addNewEvent({
        // TODO: needs to give user some error message because if not logged in cannot add comments
        event: this.constructEventJsonObject(),
        suggestionId: parseInt(this.suggestionId)
      });
      this.content = '';
    }
  }
};
</script>

<style scoped>
@import '~simplemde/dist/simplemde.min.css';

div.comment-divider {
  display: inline-block;
  text-align: center;
  width: 2px;
  height: 40px;
  margin-top: 20px;
  background-color: #dddddd;
}

div.comment-container {
  width: 100%;
  background-color: #ffffff;
  border: 2px solid #f5f5f5;
  text-align: left;
  margin-top: 10px;
}

div.comment-header {
  padding: 20px 40px;
}

div.comment-header .comment-info {
  display: inline-block;
  vertical-align: middle;
  margin-left: 20px;
}
div.comment-header .comment-info p {
  vertical-align: middle;
  margin: 0;
  font-weight: bold;
}

div.comment-box {
  width: 100%;
  border-top: 1px solid #f5f5f5;
  padding: 10px 40px;
  margin: 0;
}

div.markdown-editor {
  padding-left: 10px;
  padding-right: 10px;
  width: 90%;
}

div.comment-submit {
  width: 100%;
  padding: 10px 40px;
  margin: 0;
  text-align: right;
}

.submitButton {
  background-color: #06a798;
  border: none;
  color: white;
  padding: 15px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 62px;
  cursor: pointer;
}

@media (max-width: 750px) {
  div.comment-header {
    padding: 20px;
  }

  div.comment-box {
    padding-left: 20px;
    padding-right: 20px;
  }
}
</style>
