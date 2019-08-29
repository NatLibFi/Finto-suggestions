<template>
  <div class="container">
    <h4 v-if="isNewMeeting">Luo uusi kokous</h4>
    <h4 v-if="!isNewMeeting">Muokkaa kokousta {{ meetingId }}</h4>

    <div class="input-group">
      <p><strong>Kokouksen nimi</strong></p>
      <input @input="$v.$touch()" v-model="name" type="text" />
    </div>

    <div class="input-group">
      <p><strong>Kokouksen päivämäärä</strong></p>
      <datepicker
        @input="$v.$touch()"
        v-model="date"
        :inline="true"
        :monday-first="true"
        :full-month-name="true"
        :language="fi"
        :bootstrap-styling="true"
      />
    </div>

    <div
      v-if="isNewMeeting"
      @click.stop="createNewMeeting()"
      :class="[!$v.$invalid ? '' : 'disabled', 'button']"
    >
      <span v-if="isNewMeeting" class="save">
        Luo kokous
      </span>
    </div>
    <transition v-if="isNewMeeting" name="fade">
      <p v-if="hasSucceeded" class="success-message">Kokous luotu!</p>
      <p v-if="hasFailed" class="failure-message">Kokousta ei saatu luotua.</p>
    </transition>

    <div
      v-if="!isNewMeeting"
      @click.stop="editMeeting()"
      :class="[!$v.$invalid ? '' : 'disabled', 'button']"
    >
      <span v-if="!isNewMeeting" class="save">
        Tallenna muutokset
      </span>
    </div>
    <transition v-if="!isNewMeeting" name="fade">
      <p v-if="hasSucceeded" class="success-message">Muutokset tallennettu.</p>
      <p v-if="hasFailed" class="failure-message">Muutos ei onnistunut.</p>
    </transition>
  </div>
</template>

<script>
import Datepicker from 'vuejs-datepicker';
import { fi, sv } from 'vuejs-datepicker/dist/locale';
import { required, minLength } from 'vuelidate/lib/validators';

import { mapMeetingActions, mapMeetingGetters } from '../../store/modules/meeting/meetingModule.js';
import { meetingActions, meetingGetters } from '../../store/modules/meeting/meetingConsts.js';

export default {
  components: {
    Datepicker
  },
  props: {
    meetingId: [String, Number],
    isNewMeeting: {
      type: Boolean,
      required: true
    }
  },
  data() {
    return {
      name: '',
      date: '',
      hasSucceeded: false,
      hasFailed: false,
      fi: fi,
      sv: sv
    };
  },
  validations: {
    name: {
      required,
      minLength: minLength(1)
    },
    date: {
      required
    }
  },
  computed: {
    ...mapMeetingGetters({ meeting: meetingGetters.GET_MEETING })
  },
  created() {
    if (!this.isNewMeeting) {
      this.name = this.meeting.name;
      this.date = this.meeting.meeting_date;
    } else {
      this.date = new Date();
    }
  },
  methods: {
    ...mapMeetingActions({
      addNewMeeting: meetingActions.ADD_NEW_MEETING,
      updateMeeting: meetingActions.UPDATE_MEETING
    }),
    async editMeeting() {
      if (!this.$v.$invalid) {
        await this.updateMeeting({
          meetingId: this.meetingId,
          data: {
            name: this.$sanitize(this.name),
            meeting_date: this.date
          }
        })
          .then(() => {
            this.hasSucceeded = true;
            setTimeout(() => {
              this.hasSucceeded = false;
            }, 2000);
          })
          .catch(() => {
            this.hasFailed = true;
          });
      }
    },
    async createNewMeeting() {
      if (!this.$v.$invalid) {
        await this.addNewMeeting({
          name: this.$sanitize(this.name),
          meeting_date: this.date
        })
          .then(() => {
            this.hasSucceeded = true;
            this.name = '';
            setTimeout(() => {
              this.$emit('close');
              this.hasSucceeded = false;
            }, 2000);
          })
          .catch(() => {
            this.hasFailed = true;
            setTimeout(() => {
              this.hasFailed = false;
            }, 3000);
          });
      }
    }
  },
  mounted: function() {
    document.addEventListener('keydown', e => {
      if (e.keyCode == 13) {
        if (this.isNewMeeting) {
          this.createNewMeeting();
        } else {
          this.editMeeting();
        }
      }
    });
  }
};
</script>

<style>
.vdp-datepicker__calendar .cell:not(.blank):not(.disabled).day:hover,
.vdp-datepicker__calendar .cell:not(.blank):not(.disabled).month:hover,
.vdp-datepicker__calendar .cell:not(.blank):not(.disabled).year:hover {
  border: 1px solid #06a798;
}

.vdp-datepicker__calendar .cell.selected {
  background: #06a798;
  color: #ffffff;
  border: 1px solid #06a798;
}

.vdp-datepicker__calendar .cell.selected:hover {
  background: #44bdb2;
  border: 1px solid #44bdb2;
}
</style>

<style scoped>
.container {
  padding: 10px 40px;
  margin-bottom: 20px;
}

.container h4 {
  margin-bottom: 30px;
  text-align: left;
}

.input-group {
  position: relative;
  height: 100%;
  box-sizing: border-box;
}

.input-group p {
  margin: 20px 0 6px 0;
  font-size: 13.5px;
  font-weight: 500;
  text-align: left;
}

.input-group input {
  padding: 7px 6px !important;
  width: 100%;
  font-size: 12px;
  box-sizing: border-box;
  overflow: visible;
}

.button {
  display: block;
  margin: 20px 0 0;
  padding: 8px 12px;
  font-weight: 600;
  font-size: 13px;
  background-color: #06a798;
  border: 3px solid #06a798;
  border-radius: 2px;
  text-align: center;
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
  text-align: center;
}

.disabled,
.disabled:hover {
  background-color: #dddddd;
  border-color: #dddddd;
  -webkit-user-select: none; /* Safari */
  -moz-user-select: none; /* Firefox */
  -ms-user-select: none; /* IE10+/Edge */
  user-select: none; /* Standard */
  cursor: default;
}

.success-message,
.failure-message {
  color: #44bdb2;
  position: absolute;
  bottom: 0px;
  left: 50%;
  transform: perspective(1px) translateX(-50%);
}

.failure-message {
  color: red;
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
