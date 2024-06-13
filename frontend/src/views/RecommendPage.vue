<template>
  <v-container class="mainBox">
    <v-row class="chat-content" ref="chatContent">
      <v-col cols="12" class="chatBox">
        <div v-for="(message, index) in messages" :key="index" class="chat-message" :class="messageClass(message)">
          <div :class="messageClass(message, true)">
            {{ message.text }}
          </div>
          <v-row v-if="message.games && message.games.length" class="game-cards" align="start">
            <game-card v-for="game in message.games" :key="game.appid || game.name" :game="game" />
          </v-row>
        </div>
      </v-col>
    </v-row>
    <div class="search-bar">
      <v-row>
        <v-col cols="12">
          <v-text-field v-model="userInput" label="검색어를 입력하세요" @keyup.enter="sendQuery" append-outer-icon="mdi-magnify"
            @click:append-outer="sendQuery" hide-details dense outlined></v-text-field>
        </v-col>
      </v-row>
    </div>
  </v-container>
</template>

<script>
import GameCard from './GameCard.vue';
import api from '../api';

export default {
  components: {
    GameCard
  },
  data() {
    return {
      userInput: '',
      messages: [],
      error: null,
      previousInput: '',
      loading: false,
    };
  },
  mounted() {
    if (this.$route.query.user_input) {
      this.userInput = this.$route.query.user_input;
      this.sendQuery();
    }
    this.scrollToBottom();
  },
  updated() {
    this.scrollToBottom();
  },
  methods: {
    messageClass(message, inner = false) {
      if (message.isUser) {
        return inner ? 'user-message' : 'user-message-container';
      } else {
        return inner ? 'bot-message' : 'bot-message-container';
      }
    },
    isValidSearchQuery(query) {
      // 의미 없는 검색어 필터링 (특수 문자만 포함된 경우 등)
      if (/^[^a-zA-Z0-9가-힣]+$/.test(query)) return false;

      // 공백만 포함된 경우 필터링
      if (!query.trim()) return false;

      return true;
    },
    async sendQuery() {
      if (this.userInput.trim() === '') return;

      this.messages.push({ text: this.userInput, isUser: true });

      // 검색어 유효성 검사
      if (!this.isValidSearchQuery(this.userInput)) {
        this.messages.push({ text: '유효한 검색어를 입력해주세요.', isUser: false });
        this.userInput = '';
        this.$nextTick(() => {
          this.scrollToBottom();
        });
        return;
      }

      this.loading = true;
      this.messages.push({ text: '게임 추천 중입니다...', isUser: false });
      this.$nextTick(() => {
        this.scrollToBottom();
      });

      try {
        const response = await api.get(`recommendations/games/`, {
          params: {
            user_input: this.userInput
          }
        });
        if (!response.status === 200) throw new Error(`Error: ${response.statusText}`);

        const data = response.data;

        this.messages = this.messages.filter(message => message.text !== '게임 추천 중입니다...');

        if (data.similar_games) {
          const botMessage = { text: '다음은 추천 게임입니다:', isUser: false, games: data.similar_games.slice(0, 4) };
          this.messages.push(botMessage);
          this.$nextTick(() => {
            setTimeout(() => {
              this.scrollToBottom();
            }, 500);
          });
        } else {
          this.messages.push({ text: data.error || '추천 게임을 찾을 수 없습니다.', isUser: false });
        }

        this.previousInput = this.userInput;
      } catch (error) {
        this.messages = this.messages.filter(message => message.text !== '게임 추천 중입니다...');
        this.messages.push({ text: '추천 게임을 가져오는 중 오류가 발생했습니다. 검색어를 확인해주세요.', isUser: false });
        this.error = error.toString();
      } finally {
        this.loading = false;
      }

      this.userInput = '';
      this.$nextTick(() => {
        this.scrollToBottom();
      });
    },
    async getMoreRecommendations() {
      if (this.previousInput.trim() === '') return;

      this.messages.push({ text: '다른 게임은 없어?', isUser: true });
      this.loading = true;
      this.messages.push({ text: '게임 추천 중입니다...', isUser: false });
      this.$nextTick(() => {
        this.scrollToBottom();
      });

      try {
        const response = await api.get(`recommendations/games/`, {
          params: {
            user_input: this.previousInput
          }
        });
        if (!response.status === 200) throw new Error(`Error: ${response.statusText}`);

        const data = response.data;

        this.messages = this.messages.filter(message => message.text !== '게임 추천 중입니다...');

        if (data.similar_games) {
          const botMessage = { text: '다음은 추가 추천 게임입니다:', isUser: false, games: data.similar_games.slice(0, 4) };
          this.messages.push(botMessage);
          this.$nextTick(() => {
            setTimeout(() => {
              this.scrollToBottom();
            }, 500);
          });
        } else {
          this.messages.push({ text: data.error || '추가 추천 게임을 찾을 수 없습니다.', isUser: false });
        }
      } catch (error) {
        this.messages = this.messages.filter(message => message.text !== '게임 추천 중입니다...');
        this.messages.push({ text: '추가 추천 게임을 가져오는 중 오류가 발생했습니다.', isUser: false });
        this.error = error.toString();
      } finally {
        this.loading = false;
      }

      this.$nextTick(() => {
        this.scrollToBottom();
      });
    },
    scrollToBottom() {
      this.$nextTick(() => {
        const chatContent = this.$refs.chatContent;
        if (chatContent && chatContent.$el) {
          const messages = chatContent.$el.querySelectorAll('.chat-message');
          if (messages.length > 0) {
            const lastMessage = messages[messages.length - 1];
            lastMessage.scrollIntoView({ behavior: 'smooth', block: 'end' });
          }
        }
      });
    }
  },
  watch: {
    messages() {
      this.$nextTick(() => {
        setTimeout(() => {
          this.scrollToBottom();
        }, 500);
      });
    },
  }
};
</script>

<style lang="scss" scoped>
html,
body {
  height: 100%;
  margin: 0;
  overflow: hidden;
}

.mainBox {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 55px);
  max-width: 1000px;
  margin: 0 auto;
}

.chat-content {
  flex: 1;
  overflow-y: auto;
  margin-bottom: 100px;
  overflow-x: hidden;
}

.chat-content::-webkit-scrollbar {
  display: none;
}

.user-message-container,
.bot-message-container {
  display: flex;
  margin-bottom: 10px;
}

.user-message-container {
  justify-content: flex-end;
}

.bot-message-container {
  flex-direction: column;
  align-items: flex-start;
}

.user-message,
.bot-message {
  margin-top: 15px;
  position: relative;
  padding: 20px;
  max-width: 60%;
  min-width: 100px;
  border-radius: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-message {
  background-color: #ffffff;
  color: #000000;
  margin-right: 10px;
}

.user-message:after {
  content: '';
  position: absolute;
  top: 13px;
  right: -23px;
  border-left: 30px solid #ffffff;
  border-top: 10px solid transparent;
  border-bottom: 10px solid transparent;
}

.bot-message {
  background-color: $MAIN-COLOR-NAVY;
  color: white;
  margin-left: 10px;
}

.bot-message:before {
  content: '';
  position: absolute;
  top: 13px;
  left: -23px;
  border-right: 30px solid $MAIN-COLOR-NAVY;
  border-top: 10px solid transparent;
  border-bottom: 10px solid transparent;
}

.search-bar {
  position: fixed;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  max-width: 1000px;
  box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
  background-color: #ffffff;
}

.game-cards {
  margin-top: 10px;
  display: flex;
  flex-wrap: wrap;
}
</style>
