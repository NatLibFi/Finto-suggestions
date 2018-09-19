<template>
  <div :class="container">
    <h3>YSE - YSAn ja YSOn käsite-ehdotukset</h3>
    <div :class="welcomeText">
      <p>
        Tämä palvelu on YSA/YSO -käsite-ehdotuksille ja niiden etenemisen seuraamiselle.
        Voit selata ja kommentoida ehdotuksia täällä. Ehdotusten selaaminen onnistuu ilman käyttäjätunnuksia,
        mutta kommentointi edellyttää tunnuksen luomista. Voit osoittaa tukesi ehdotukselle kommentoimalla sitä.
        Halutessasi voit nopeuttaa ehdotuksen käsittelyä jättämällä ehdotuksen kommenttikenttään täsmennyksiä ja lisätietoja.
        Uusien käsite-ehdotuksien tekeminen onnistuu Fintossa.
      </p>
    </div>
    <!-- <div :class="searchSuggestions">
      <h4>Hae ehdotusta</h4>
      <span>
        <form>
          <input type="text" value="Hae jotain" />
          <input type="button" value="Hae" />
        </form>
      </span>
    </div> -->
    <div>
      <suggestion-search-form />
    </div>
    <!-- <div :class="filterSuggestions">
      <h4>Suodata hakutuloksia</h4>
      <span>
        <select>
          <option>Käsittelyn tila</option>
        </select>
        <select>
          <option>Ehdotustyyppi</option>
        </select>
        <select>
          <option>Tyyppi</option>
        </select>
        <select>
          <option>Kokous</option>
        </select>
      </span>
    </div> -->
    <div>
      <filter-suggestions />
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
  }
}
</script>

<style scoped>

</style>
