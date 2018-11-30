<template>
  <div class="suggestion">
    <div class="back-button">
      <a @click="goToSuggestion" unselectable="on">
        <svg-icon icon-name="arrow"><icon-arrow /></svg-icon>
        Takaisin käsite-ehdotuksiin
      </a>
    </div>

    <div v-if="suggestions && suggestions.length > 0" class="suggestion-container">
      <div class="suggestion-header">
        <div class="suggestion-header-headline">
          <h1 class="suggestion-title">{{ suggestions[0].preferred_label.fi }}</h1>
          <div class="suggestion-header-details">
            <span><strong>#{{ suggestions[0].id }} </strong></span>
            <span>Lähetetty 3 päivää sitten</span>
            <span class="suggestion-type">{{ suggestionTypeToString[suggestions[0].suggestion_type] }}</span>
            <span class="tag"
              v-if="suggestions[0].tags && suggestions[0].tags.length > 0"
              v-for="tag in suggestions[0].tags"
              :key="tag.label">{{ tag.label }}</span>
          </div>
        </div>
        <div class="suggestion-header-buttons">
          <svg-icon icon-name="more"><icon-more /></svg-icon>
        </div>
      </div>

      <suggestion-content
        v-if="suggestions && suggestions.length > 0"
        :suggestion="suggestions[0]" />

      <div v-if="suggestions && suggestions[0].reactions.length > 0" class="suggestion-reactions">
        <div v-for="reaction in suggestions[0].reactions" :key="reaction.id">
          <div class="reaction">
            <div class="emoji">{{ reaction.code }}</div>
            <div class="counter">2</div>
            <a @click="displayEmoji(reaction.code)">
              button
            </a>
          </div>
        </div>
      </div>
    </div>

    <div v-if="events && events.length > 0">
      <div v-for="event in events" :key="event.id">
        <suggestion-event
          :event="event"
          :type="event.event_type">
        </suggestion-event>
      </div>
    </div>

    <div>
      <add-comment :userId="userId" :suggestionId="suggestionId" />
    </div>
  </div>
</template>

<script>
import SuggestionContent from './SuggestionContent';
import SuggestionEvent from './SuggestionEvent';
import IconArrow from '../icons/IconArrow';
import IconMore from '../icons/IconMore';
import SvgIcon from '../icons/SvgIcon';
import AddComment from './AddComment';

import {
  suggestionGetters,
  suggestionActions
} from '../../store/modules/suggestion/suggestionConsts.js';

import {
  mapSuggestionGetters,
  mapSuggestionActions
} from '../../store/modules/suggestion/suggestionModule.js';

import { eventGetters, eventActions } from '../../store/modules/event/eventConsts.js';
import { mapEventGetters, mapEventActions } from '../../store/modules/event/eventModule.js';

import { suggestionTypeToString } from '../../utils/suggestionMappings.js';

export default {
  components: {
    SuggestionContent,
    SuggestionEvent,
    IconArrow,
    IconMore,
    SvgIcon,
    AddComment
  },
  props: {
    suggestionId: {
      type: [String, Number],
      require: true
    }
  },
  data: () => ({
    // eslint-disable-next-line
    userId: $cookies.get('logged_user_id'),
    suggestionTypeToString
  }),
  computed: {
    ...mapSuggestionGetters({
      suggestions: suggestionGetters.GET_SUGGESTIONS
    }),
    ...mapEventGetters({
      events: eventGetters.GET_EVENTS
    })
  },
  async created() {
    await this.getSuggestions(parseInt(this.suggestionId));
    await this.getEventsBySuggestionId(parseInt(this.suggestionId));
  },
  methods: {
    ...mapSuggestionActions({
      getSuggestions: suggestionActions.GET_SUGGESTION_BY_ID
    }),
    ...mapEventActions({
      getEventsBySuggestionId: eventActions.GET_EVENTS_BY_SUGGESTION_ID
    }),
    goToSuggestion() {
      this.$router.push('/');
    }
  }
};
</script>

<style scoped>
div.suggestion {
  width: 60vw;
  padding: 40px 20%;
  overflow: hidden;
}

div.back-button {
  color: #1ea195;
  font-weight: 800;
  font-size: 16px;
  text-align: left;
  margin-left: 6px;
  -webkit-user-select: none; /* Safari */
  -moz-user-select: none; /* Firefox */
  -ms-user-select: none; /* IE10+/Edge */
  user-select: none; /* Standard */
}

div.back-button a:hover {
  cursor: pointer;
  cursor: hand;
}

div.back-button svg {
  margin: 0 -15px -27px 0;
  width: 37px;
  height: 37px;
}

div.suggestion-container {
  background-color: #ffffff;
  border: 2px solid #f5f5f5;
  text-align: left;
}

div.suggestion-header {
  margin: 35px 40px 20px;
  position: relative;
}

div.suggestion-header-headline {
  line-height: 45px;
  display: inline-block;
  width: 80%;
  height: 100px;
}

h1.suggestion-title {
  display: inline;
  font-weight: 900;
  vertical-align: middle;
  text-transform: lowercase;
  text-transform: capitalize;
}

div.suggestion-header-buttons {
  position: absolute;
  top: 0px;
  right: 0px;
  bottom: 0px;
  display: inline-block;
  width: 20%;
  height: 100px;
  text-align: right;
}

@media (max-width: 700px) {
  div.suggestion {
    width: 80vw;
    padding: 10px 10% 20px;
  }

  div.suggestion-header-headline,
  div.suggestion-header-buttons {
    width: 100%;
    height: initial;
    position: initial;
    text-align: left;
  }

  div.suggestion-header-details {
    line-height: 24px;
  }
}

.suggestion-type {
  font-size: 14px;
  font-weight: 600;
  background-color: #f2994a;
  color: #ffffff;
  padding: 3px 10px;
  margin-left: 10px;
  border-radius: 2px;
  text-transform: lowercase;
}

.tag {
  font-size: 14px;
  font-weight: 600;
  background-color: #ffffff;
  color: #ac63ef;
  border: 1px solid #ac63ef;
  padding: 3px 10px;
  margin-left: 10px;
  border-radius: 2px;
  text-transform: lowercase;
}
</style>
