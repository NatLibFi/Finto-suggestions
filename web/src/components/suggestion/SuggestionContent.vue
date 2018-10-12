<template>
  <div class="suggestion-content">

    <div v-if="s.tags && s.tags.length > 0">
      <p><strong>Käsitteen tyyppi</strong></p>
      <p>Maantieteellinen</p>
    </div>

    <div v-if="s.preferred_label.fi">
      <p v-if="s.suggestion_type == 'NEW'"><strong>Ehdotettu termi suomeksi</strong></p>
      <p v-if="s.suggestion_type == 'MODIFY'"><strong>Päätermi/asiasana</strong></p>
      <p>{{ s.preferred_label.fi }}</p>
    </div>

    <div v-if="s.preferred_label.sv">
      <p><strong>Ehdotettu termi ruotsiksi</strong></p>
      <p>{{ s.preferred_label.sv }}</p>
    </div>

    <div v-if="s.preferred_label.en">
      <p><strong>Ehdotettu termi englanniksi</strong></p>
      <p>{{ s.preferred_label.en }}</p>
    </div>

    <div v-if="s.alternative_label">
      <p><strong>Vaihtoehtoiset termit ja ilmaisut</strong></p>
      <p v-if="s.alternative_label.fi">{{ s.alternative_label.fi }} [fin]</p>
      <p v-if="s.alternative_label.sv">{{ s.alternative_label.sv }} [swe]</p>
      <p v-if="s.alternative_label.en">{{ s.alternative_label.en }} [eng]</p>
    </div>

    <div v-if="s.broader && s.broader.length > 0">
      <p><strong>Yläkäsite YSOssa (LT)</strong></p>
      <p v-for="term in s.broader" :key="term.id">
        <a :href="term">{{ term }}</a>
      </p>
    </div>

    <div v-if="s.narrower && s.narrower.length > 0">
      <p><strong>Alakäsitteet (ST)</strong></p>
      <p v-for="term in s.narrower" :key="term.id">
        <a :href="term">{{ term }}</a>
      </p>
    </div>

    <div v-if="s.related && s.related.length > 0">
      <p><strong>Assosiatiiviset (RT)</strong></p>
      <p v-for="term in s.related" :key="term.id">
        <a :href="term">{{ term }}</a>
      </p>
    </div>

    <div v-if="s.group && s.group.length > 0">
      <p><strong>YSA/YSO temaattinen ryhmä</strong></p>
      <p v-for="group in s.group" :key="group.id">
        <a :href="group">{{ group }}</a>
      </p>
    </div>

    <div v-if="s.exactMatches && s.exactMatches.length > 0">
      <p><strong>Vastaava käsite muussa sanastossa</strong></p>
      <p v-for="match in s.exactMatches" :key="match.id">
        <span>{{ match.vocab }}, </span>
        <span>{{ match.value }}</span>
      </p>
    </div>

    <div v-if="s.description">
      <p v-if="s.suggestion_type == 'NEW'"><strong>Tarkoitusta täsmentävä selite</strong></p>
      <p v-if="s.suggestion_type == 'MODIFY'"><strong>Ehdotettu muutos</strong></p>
      <p>{{ s.description }}</p>
    </div>

    <div v-if="s.reason">
      <p><strong>Perustelut ehdotukselle</strong></p>
      <p>{{ s.reason }}</p>
    </div>

    <div v-if="s.neededFor">
      <p><strong>Aineisto jonka kuvailussa käsitettä tarvitaan (esim. nimeke tai URL)</strong></p>
      <p>{{ s.neededFor }}</p>
    </div>

    <div v-if="s.organization">
      <p><strong>Ehdottajan organisaatio</strong></p>
      <p>{{ s.organization }}</p>
    </div>

  </div>
</template>

<script>
export default {
  props: {
    s: Object // suggestion
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
