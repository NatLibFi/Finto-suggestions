<template>
  <div class="search-container">
    <div class="content">
      <h3>YSE - YSAn ja YSOn käsite-ehdotukset</h3>
      <div class="welcome-text">
        <p>
          {{ welcomeSummary }}
          <a @click="toggleWelcomeText" v-if="!isShown" class="button">Lue lisää</a>
          <a @click="toggleWelcomeText" v-if="isShown" class="button">Piilota</a>
        </p>
        <p v-if="isShown">{{ welcomeExplanation }}</p>
        <p class="meetings-link">
          <strong>
            Voit tarkastella tulevia YSO-kokouksia <a @click="goToMeetings()">täällä</a>.
          </strong>
        </p>
      </div>
      <div>
        <suggestion-search-form :filters="filters" :searchWord="searchWord" :sort="sort" />
      </div>
      <div>
        <filter-suggestions :isMeeting="false" :filters="filters" :searchWord="searchWord" :sort="sort" />
      </div>
    </div>
  </div>
</template>

<script>
import SuggestionSearchForm from './SuggestionSearchForm';
import FilterSuggestions from './FilterSuggestions';

export default {
  components: {
    SuggestionSearchForm,
    FilterSuggestions
  },
  props: {
    filters: {
      type: String,
      default: ''
    },
    searchWord: {
      type: String,
      default: ''
    },
    sort: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      isShown: false,
      welcomeSummary: `Tämä palvelu on YSA/YSO -käsite-ehdotuksille ja niiden etenemisen
        seuraamiselle.`,
      welcomeExplanation: `Voit selata ja kommentoida ehdotuksia tässä palvelussa. Ehdotusten
        selaaminen onnistuu ilman käyttäjätunnuksia, mutta kommentointi edellyttää tunnuksen
        luomista. Voit osoittaa tukesi ehdotukselle kommentoimalla sitä ja voit halutessasi
        nopeuttaa ehdotuksen käsittelyä jättämällä ehdotuksen kommenttikenttään täsmennyksiä
        ja lisätietoja. Uusien käsite-ehdotuksien tekeminen onnistuu Finto-palvelussa.`
    };
  },
  methods: {
    goToMeetings() {
      this.$router.push('/meetings');
    },
    toggleWelcomeText() {
      this.isShown = !this.isShown;
    }
  }
};
</script>

<style scoped>
h3 {
  text-align: left;
  padding-bottom: 6px;
}
.search-container {
  width: 60vw;
  margin: 20px 20vw 0;
  border: 2px solid #f5f5f5;
  background-color: #ffffff;
}
.search-container .content {
  padding: 20px 30px 10px;
}
.welcome-text {
  text-align: left;
  font-size: 14.5px;
}
.button {
  white-space: nowrap;
}
.button:hover {
  cursor: pointer;
  cursor: hand;
}
.meetings-link a:hover {
  cursor: pointer;
  cursor: hand;
}
@media (max-width: 700px) {
  .search-container {
    width: 80vw;
    margin: 20px 10vw 0;
  }
  .search-container .content {
    padding: 20px 20px 10px;
  }
  .welcome-text {
    font-size: 15px;
    line-height: 1.3;
  }
}
</style>
