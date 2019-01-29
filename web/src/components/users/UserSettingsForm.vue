<template>
  <div class="form-container">
    <h5>Muokkaa asetuksiasi</h5>
    <div class="setting-inputs">
      <div>
        <p>Nimi:</p>
        <input v-model="userName" type="text">
      </div>
      <div>
        <p>Nimike/titteli:</p>
        <input v-model="userTitle" type="text">
      </div>
      <div>
        <p>Organisaatio:</p>
        <input v-model="userOrg" type="text">
      </div>
      <div>
        <p>Profiilikuvan url-osoite:</p>
        <input v-model="userImageUrl" type="url">
      </div>
    </div>

    <div @click="submitForm" :class="[isTouched ? '' : 'disabled', 'button']">
      <span class="save">
        Tallenna muutokset
      </span>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isTouched: false,
      userName: '',
      userTitle: '',
      userOrg: '',
      userImageUrl: ''
    };
  },
  methods: {
    submitForm() {
      if (this.isTouched) {
        this.isTouched = false;
      }
    }
  }
};
</script>

<style scoped>
.form-container {
  padding: 10px 0 20px;
}

.setting-inputs h5 {
  margin: 14px 0 0;
}

.setting-inputs div {
  margin: 6px 0 14px;
  width: 50%;
  display: inline-block;
}

.setting-inputs div p {
  height: 100%;
  margin: 0 0 2px 0;
  font-size: 13.5px;
  font-weight: 500;
}

.setting-inputs div input {
  padding: 7px 6px;
  width: 20vw;
}

.button {
  display: inline-block;
  margin: 10px 0 0;
  padding: 6px 12px;
  font-weight: 600;
  font-size: 13px;
  background-color: #06a798;
  border: 3px solid #06a798;
  border-radius: 2px;
}

.button:hover {
  background-color: #44bdb2;
  border: 3px solid #44bdb2;
  cursor: pointer;
  cursor: hand;
}

.button .save {
  color: #ffffff;
  transition: background-color, 0.1s;
  transition: border, 0.1s;
}

.disabled,
.disabled:hover {
  background-color: #dddddd;
  border: none;
  -webkit-user-select: none; /* Safari */
  -moz-user-select: none; /* Firefox */
  -ms-user-select: none; /* IE10+/Edge */
  user-select: none; /* Standard */
  cursor: default;
}

@media (max-width: 700px) {
  .setting-inputs div {
    margin: 6px 0 14px;
    width: 100%;
    display: block;
  }

  .setting-inputs div input {
    padding: 7px 6px;
    width: 42vw;
  }
}

@media (max-width: 500px) {
  .setting-inputs div input {
    width: 50vw;
  }
}
</style>
