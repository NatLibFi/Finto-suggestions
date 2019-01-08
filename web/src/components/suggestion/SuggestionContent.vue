<template>
  <div class="suggestion-content">

    <div v-if="suggestion && suggestion.tags && suggestion.tags.length > 0">
      <p><strong>Käsitteen tyyppi</strong></p>
      <p>Maantieteellinen</p>
    </div>

    <div v-if="suggestion.preferred_label.fi">
      <p v-if="suggestion.suggestion_type == suggestionTypes.NEW">
        <strong>Ehdotettu termi suomeksi</strong>
      </p>
      <p v-if="suggestion.suggestion_type == suggestionTypes.MODIFY">
        <strong>Päätermi/asiasana</strong>
      </p>
      <p>{{ suggestion.preferred_label.fi }}</p>
    </div>

    <div v-if="suggestion.preferred_label.sv">
      <p><strong>Ehdotettu termi ruotsiksi</strong></p>
      <p>{{ suggestion.preferred_label.sv }}</p>
    </div>

    <div v-if="suggestion.preferred_label.en">
      <p><strong>Ehdotettu termi englanniksi</strong></p>
      <p>{{ suggestion.preferred_label.en }}</p>
    </div>

    <div v-if="suggestion.alternative_labels">
      <p><strong>Vaihtoehtoiset termit ja ilmaisut</strong></p>
      <p v-if="suggestion.alternative_labels.fi">{{ suggestion.alternative_labels.fi }} [fin]</p>
      <p v-if="suggestion.alternative_labels.sv">{{ suggestion.alternative_labels.sv }} [swe]</p>
      <p v-if="suggestion.alternative_labels.en">{{ suggestion.alternative_labels.en }} [eng]</p>
    </div>

    <div v-if="suggestion.broader_labels && suggestion.broader_labels.length > 0">
      <p><strong>Yläkäsite YSOssa (LT)</strong></p>
      <p v-for="term in suggestion.broader_labels" :key="term.id">
        <a :href="term">{{ term }}</a>
      </p>
    </div>

    <div v-if="suggestion.narrower_labels && suggestion.narrower_labels.length > 0">
      <p><strong>Alakäsitteet (ST)</strong></p>
      <p v-for="term in suggestion.narrower_labels" :key="term.id">
        <a :href="term">{{ term }}</a>
      </p>
    </div>

    <div v-if="suggestion.related_labelsrelated && suggestion.related_labels.length > 0">
      <p><strong>Assosiatiiviset (RT)</strong></p>
      <p v-for="term in suggestion.related_labels" :key="term.id">
        {{ term.vocab }}: <a :href="term.value">{{ term.value }}</a>
      </p>
    </div>

    <div v-if="suggestion.groups && suggestion.groups.length > 0">
      <p><strong>YSA/YSO temaattinen ryhmä</strong></p>
      <p v-for="group in suggestion.groups" :key="group.id">
        <a :href="group">{{ group }}</a>
      </p>
    </div>

    <div v-if="suggestion.exactMatches && suggestion.exactMatchesuggestion.length > 0">
      <p><strong>Vastaava käsite muussa sanastossa</strong></p>
      <p v-for="match in suggestion.exactMatches" :key="match.id">
        <span>{{ match.vocab }}, </span>
        <span>{{ match.value }}</span>
      </p>
    </div>

    <div v-if="suggestion.description">
      <p v-if="suggestion.suggestion_type == suggestionTypes.NEW">
        <strong>Tarkoitusta täsmentävä selite</strong>
      </p>
      <p v-if="suggestion.suggestion_type == suggestionTypes.MODIFY">
        <strong>Ehdotettu muutos</strong>
      </p>
      <p>{{ suggestion.description }}</p>
    </div>

    <div v-if="suggestion.reason">
      <p><strong>Perustelut ehdotukselle</strong></p>
      <p>{{ suggestion.reason }}</p>
    </div>

    <div v-if="suggestion.neededFor">
      <p><strong>Aineisto jonka kuvailussa käsitettä tarvitaan (esim. nimeke tai URL)</strong></p>
      <p>{{ suggestion.neededFor }}</p>
    </div>

    <div v-if="suggestion.organization">
      <p><strong>Ehdottajan organisaatio</strong></p>
      <p>{{ suggestion.organization }}</p>
    </div>

    <div v-if="userName">
      <p><strong>Käsittelijä</strong></p>
      <p>{{ userName }} <a href="#" v-on:click="unassignUserFromSuggestion(suggestion.id, suggestion.user_id)">Poista käsittelijä ehdotuksesta</a></p>
    </div>

  </div>
</template>

<script>
import { suggestionType } from '../../utils/suggestionMappings.js';
import { suggestionActions } from '../../store/modules/suggestion/suggestionConsts';
import { mapSuggestionActions } from '../../store/modules/suggestion/suggestionModule';

export default {
  props: {
    suggestion: {
      type: Object,
      required: true
    },
    userName: { type: String, default: '' }
  },
  data() {
    return {
      suggestionTypes: {
        NEW: suggestionType.NEW,
        MODIFY: suggestionType.MODIFY
      }
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
div.suggestion-content {
  border-top: 1px solid #f5f5f5;
  padding: 30px 40px 10px;
  font-size: 16px;
}

div > div {
  margin-bottom: 20px;
}

p {
  margin: 0;
}
</style>
