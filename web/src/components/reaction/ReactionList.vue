<template>
  <div class="emoji-list">
    <div v-for="(emoji, index) in emojiList" :key="index" class="single-emoji">
      <span class="count">{{ emoji.count }}</span>
      <span class="emoji">
        {{ emojiMapping[emoji.code] }}
      </span>
    </div>
  </div>
</template>

<script>
import { emojiMapping } from '../../utils/reactionHelpers';
export default {
  props: {
    reactions: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      emojiMapping,
      emojiList: []
    };
  },
  async created() {
    this.emojiList = this.listCountedEmojis(this.reactions);
  },
  watch: {
    reactions(newVal) {
      this.emojiList = this.listCountedEmojis(newVal);
    }
  },
  methods: {
    listCountedEmojis(reactions) {
      let listedEmojis = [];
      let arr = [];
      for (let i = 0; i < reactions.length; i++) {
        if (reactions[i].code in this.emojiMapping) {
          if (listedEmojis.includes(reactions[i].code)) {
            let index = arr.findIndex(emoji => emoji.code === reactions[i].code);
            arr[index].count += 1;
          } else {
            arr.push({
              code: reactions[i].code,
              count: 1
            });
            listedEmojis.push(reactions[i].code);
          }
        }
      }
      return arr.sort((a, b) => b.count - a.count || a.code < b.code);
    }
  }
};
</script>

<style scoped>
.emoji-list {
  font-size: 16px;
  min-height: 45px;
  position: relative;
}

.single-emoji {
  display: inline-block;
  width: 50px;
  height: 40px;
  margin-right: 12px;
  position: relative;
}

.count {
  position: absolute;
  top: 50%;
  left: 0;
  transform: translateY(-50%);
}

.emoji {
  font-size: 24px;
  position: absolute;
  top: 50%;
  left: 20px;
  transform: translateY(-50%);
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
