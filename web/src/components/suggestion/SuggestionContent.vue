<template>
  <div class="suggestion-content">
    <div v-if="suggestion.status && suggestion.status.length > 0">
      <p class="content-title">
        <strong>Tila</strong>
      </p>
      <p>{{ suggestionStateStatusToString[suggestion.status] }}</p>
    </div>

    <div v-if="suggestion.preferred_label.fi && suggestion.preferred_label.fi.value">
      <p v-if="suggestion.suggestion_type == suggestionType.NEW" class="content-title">
        <strong>Ehdotettu termi suomeksi</strong>
      </p>
      <p v-if="suggestion.suggestion_type == suggestionType.MODIFY" class="content-title">
        <strong>Päätermi/asiasana</strong>
      </p>
      <p v-if="!suggestion.preferred_label.fi.value">{{ suggestion.preferred_label.fi }}</p>
      <p v-if="suggestion.preferred_label.fi.value && !suggestion.preferred_label.fi.uri">
        {{ suggestion.preferred_label.fi.value }}
      </p>
      <a :href="suggestion.preferred_label.fi.uri" v-if="suggestion.preferred_label.fi.uri">
        {{ suggestion.preferred_label.fi.value }}
      </a>
    </div>

    <div v-if="suggestion.preferred_label.sv && suggestion.preferred_label.sv.value">
      <p class="content-title"><strong>Ehdotettu termi ruotsiksi</strong></p>
      <p v-if="!suggestion.preferred_label.sv.value">{{ suggestion.preferred_label.sv }}</p>
      <p v-if="suggestion.preferred_label.sv.value && !suggestion.preferred_label.sv.uri">
        {{ suggestion.preferred_label.sv.value }}
      </p>
      <a :href="suggestion.preferred_label.sv.uri" v-if="suggestion.preferred_label.sv.uri">
        {{ suggestion.preferred_label.sv.value }}
      </a>
    </div>

    <div
      v-if="
        suggestion.preferred_label.en &&
          suggestion.preferred_label.en.value &&
          suggestion.preferred_label.en.value.length > 0
      "
    >
      <p class="content-title"><strong>Ehdotettu termi englanniksi</strong></p>
      <p>{{ suggestion.preferred_label.en.value }}</p>
    </div>

    <div
      v-if="suggestion.alternative_labels[0] && suggestion.alternative_labels[0].value.length > 0"
    >
      <p class="content-title"><strong>Vaihtoehtoiset termit ja ilmaisut</strong></p>
      <p v-for="label in suggestion.alternative_labels" :key="label.id">
        {{ label.value }}
      </p>
    </div>

    <div v-if="suggestion.broader_labels[0] && suggestion.broader_labels[0].value.length > 0">
      <p class="content-title"><strong>Yläkäsite YSOssa (LT)</strong></p>
      <p v-for="term in suggestion.broader_labels" :key="term.id">
        <a :href="term.uri">{{ term.value }}</a>
      </p>
    </div>

    <div v-if="suggestion.narrower_labels[0] && suggestion.narrower_labels[0].value.length > 0">
      <p class="content-title"><strong>Alakäsitteet (ST)</strong></p>
      <p v-for="term in suggestion.narrower_labels" :key="term.id">
        <a :href="term.uri">{{ term.value }}</a>
      </p>
    </div>

    <div v-if="suggestion.related_labels[0] && suggestion.related_labels[0].value.length > 0">
      <p class="content-title"><strong>Assosiatiiviset (RT)</strong></p>
      <p v-for="term in suggestion.related_labels" :key="term.id">
        <a :href="term.uri">{{ term.value }}</a>
      </p>
    </div>

    <div v-if="suggestion.groups && suggestion.groups[0]">
      <p class="content-title"><strong>YSA/YSO temaattinen ryhmä</strong></p>
      <p v-for="group in suggestion.groups" :key="group.id">
        <a :href="group.uri">{{ group.value }}</a>
      </p>
    </div>

    <div v-if="suggestion.exactMatches[0] && suggestion.exactMatches[0].value.length > 0">
      <p class="content-title"><strong>Vastaava käsite muussa sanastossa</strong></p>
      <p v-for="match in suggestion.exactMatches" :key="match.id">
        <span v-if="match.vocab.length > 0">{{ match.vocab }}, </span>
        <span v-if="match.value.length > 0 && !match.value.includes('http')">
          {{ match.value }}
        </span>
        <span v-if="match.value.length > 0 && match.value.includes('http')">
          <a :href="match.value">{{ match.value }}</a>
        </span>
      </p>
    </div>

    <div v-if="suggestion.scopeNote">
      <p class="content-title"><strong>Tarkoitusta täsmentävä selite:</strong></p>
      <p>{{ suggestion.scopeNote }}</p>
    </div>

    <div v-if="suggestion.description">
      <p v-if="suggestion.suggestion_type == suggestionType.NEW" class="content-title">
        <strong>Perustelut ehdotukselle</strong>
      </p>
      <p v-if="suggestion.suggestion_type == suggestionType.MODIFY" class="content-title">
        <strong>Ehdotettu muutos</strong>
      </p>
      <p>{{ suggestion.description }}</p>
    </div>

    <div v-if="suggestion.reason">
      <p v-if="suggestion.suggestion_type == suggestionType.NEW" class="content-title">
        <strong>Aineisto jonka kuvailussa käsitettä tarvitaan (esim. nimeke tai URL)</strong>
      </p>
      <p v-if="suggestion.suggestion_type == suggestionType.MODIFY" class="content-title">
        <strong>Perustelut ehdotukselle</strong>
      </p>
      <p>{{ suggestion.reason }}</p>
    </div>

    <div v-if="suggestion.neededFor">
      <p class="content-title">
        <strong>Aineisto jonka kuvailussa käsitettä tarvitaan (esim. nimeke tai URL)</strong>
      </p>
      <p>{{ suggestion.neededFor }}</p>
    </div>

    <div v-if="suggestion.organization">
      <p class="content-title"><strong>Ehdottajan organisaatio</strong></p>
      <p>{{ suggestion.organization }}</p>
    </div>

    <div v-if="suggestion.yse_term && suggestion.yse_term.value">
      <p class="content-title"><strong>Termi Fintossa</strong></p>
      <a :href="suggestion.yse_term.url">{{ suggestion.yse_term.value }}</a>
    </div>

    <transition name="fade">
      <div v-if="!suggestion.user_id && isAdmin">
        <assign-user :suggestion="suggestion" class="icon-button" />
      </div>
      <div v-if="userName && suggestion.user_id">
        <p class="content-title"><strong>Käsittelijä</strong></p>
        <p>
          {{ userName }}
          <a
            v-if="isAuthenticated && isAdmin"
            @click="unassignUserFromSuggestion(suggestion.id, suggestion.user_id)"
            class="remove-button"
          >
            Poista käsittelijä ehdotuksesta
          </a>
        </p>
      </div>
    </transition>
  </div>
</template>

<script>
import AssignUser from './AssignUser';
import {
  suggestionType,
  suggestionStateStatus,
  suggestionStateStatusToString
} from '../../utils/suggestionHelpers.js';
import { suggestionActions } from '../../store/modules/suggestion/suggestionConsts';
import { mapSuggestionActions } from '../../store/modules/suggestion/suggestionModule';

export default {
  components: {
    AssignUser
  },
  props: {
    suggestion: {
      type: Object,
      required: true
    },
    userName: { type: String, default: '' },
    isAuthenticated: Boolean,
    isAdmin: Boolean
  },
  data() {
    return {
      suggestionType,
      suggestionStateStatus,
      suggestionStateStatusToString
    };
  },
  methods: {
    ...mapSuggestionActions({
      unassignUserFromSuggestion: suggestionActions.UNASSIGN_SUGGESTION_FROM_USER
    })
  }
};
</script>

<style scoped>
.suggestion-content {
  border-top: 1px solid #f5f5f5;
  padding: 20px 40px 10px;
  font-size: 16px;
  margin-bottom: 0;
  overflow-wrap: break-word;
}

div > div {
  margin-bottom: 20px;
}

div > div:last-of-type {
  margin-bottom: 6px;
}

p {
  margin: 0;
}

a.remove-button {
  font-size: 14px;
  display: inline-block;
  -webkit-user-select: none; /* Safari */
  -moz-user-select: none; /* Firefox */
  -ms-user-select: none; /* IE10+/Edge */
  user-select: none; /* Standard */
}

a.remove-button:hover {
  cursor: pointer;
  cursor: hand;
}

.content-title {
  font-size: 13px;
  margin-bottom: 3px;
}

@media (max-width: 700px) {
  div.suggestion-content {
    padding-top: 30px;
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>
