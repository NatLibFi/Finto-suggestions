<template>
  <div :class="['search-container', !meetingId ? 'extra-margin' : '']">
    <div class="content">
      <div v-if="!meetingId">
        <h3>YSE - YSAn ja YSOn käsite-ehdotukset</h3>
        <div class="welcome-text">
          <p>
            {{ welcomeSummary }}
          </p>
          <p>  
            <a @click="toggleWelcomeText" v-if="!isShown" class="button">Lue lisää</a>
            <a @click="toggleWelcomeText" v-if="isShown" class="button">Piilota</a>
          </p>
          <p v-if="isShown">{{ welcomeExplanation }}</p>
          <p class="meetings-link">
            <strong>
              <div>
                Voit tarkastella tulevia YSO-kokouksia <a @click="goToMeetings()">täällä</a>.
              </div>
              <div>
                Voit seurata uuden kokoustoiminnon kehittämistä <a @click="goToMeetingsAsPithy()">täällä</a>.
              </div>
            </strong>
          </p>
        </div>
      </div>
      <div>
        <suggestion-search-form :filters="filters" :searchWord="searchWord" :sort="sort" />
      </div>
      <div>
        <suggestion-filtering
          :meetingId="meetingId"
          :filters="filters"
          :searchWord="searchWord"
          :sort="sort"
        />
      </div>
    </div>
  </div>
</template>

<script>
import SuggestionSearchForm from './SuggestionSearchForm';
import SuggestionFiltering from './SuggestionFiltering';

export default {
  components: {
    SuggestionSearchForm,
    SuggestionFiltering
  },
  props: {
    meetingId: {
      type: [String, Number],
      default: null
    },
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
    goToMeetingsAsPithy() {
      this.$router.push('/meetingsaspithy');
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
  margin: 0 20vw 0;
  border: 2px solid #f5f5f5;
  border-top: none;
  background-color: #ffffff;
}

.extra-margin {
  margin-top: 20px;
  border-top: 2px solid #f5f5f5;
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
    margin: 0 10vw;
  }

  .extra-margin {
    margin-top: 20px;
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
