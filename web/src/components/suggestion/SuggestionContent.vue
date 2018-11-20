<template>
  <div class="suggestion-content">

    <div v-if="suggestion && suggestion.tags && suggestion.tags.length > 0">
      <p><strong>Käsitteen tyyppi</strong></p>
      <p>Maantieteellinen</p>
    </div>

    <div v-if="suggestion.preferred_label.fi">
      <p v-if="suggestion.suggestion_type == suggestionTypes.NEW"><strong>Ehdotettu termi suomeksi</strong></p>
      <p v-if="suggestion.suggestion_type == suggestionTypes.MODIFY"><strong>Päätermi/asiasana</strong></p>
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

    <div v-if="suggestion.alternative_label">
      <p><strong>Vaihtoehtoiset termit ja ilmaisut</strong></p>
      <p v-if="suggestion.alternative_label.fi">{{ suggestion.alternative_label.fi }} [fin]</p>
      <p v-if="suggestion.alternative_label.sv">{{ suggestion.alternative_label.sv }} [swe]</p>
      <p v-if="suggestion.alternative_label.en">{{ suggestion.alternative_label.en }} [eng]</p>
    </div>

    <div v-if="suggestion.broader && suggestion.broader.length > 0">
      <p><strong>Yläkäsite YSOssa (LT)</strong></p>
      <p v-for="term in suggestion.broader" :key="term.id">
        <a :href="term">{{ term }}</a>
      </p>
    </div>

    <div v-if="suggestion.narrower && suggestion.narrower.length > 0">
      <p><strong>Alakäsitteet (ST)</strong></p>
      <p v-for="term in suggestion.narrower" :key="term.id">
        <a :href="term">{{ term }}</a>
      </p>
    </div>

    <div v-if="suggestion.related && suggestion.related.length > 0">
      <p><strong>Assosiatiiviset (RT)</strong></p>
      <p v-for="term in suggestion.related" :key="term.id">
        <a :href="term">{{ term }}</a>
      </p>
    </div>

    <div v-if="suggestion.group && suggestion.group.length > 0">
      <p><strong>YSA/YSO temaattinen ryhmä</strong></p>
      <p v-for="group in suggestion.group" :key="group.id">
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
      <p v-if="suggestion.suggestion_type == suggestionTypes.MODIFY"><strong>Ehdotettu muutos</strong></p>
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

  </div>
</template>

<script>
import { suggestionType } from '../../utils/suggestionMappings.js';

export default {
  props: {
    suggestion: {
      type: Object,
      required: true
    }
  },
  data: () => ({
    suggestionTypes:
    {
      NEW: suggestionType.NEW,
      MODIFY: suggestionType.MODIFY
    }
  })
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
