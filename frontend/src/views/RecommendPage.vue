<template>
  <v-container class="mainBox flex-conter">
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
            @click:append-outer="sendQuery"></v-text-field>
        </v-col>
      </v-row>
    </div>
  </v-container>
</template>

<script>
import GameCard from './GameCard.vue';

export default {
  components: {
    GameCard,
  },
  data() {
    return {
      userInput: '',
      messages: [],
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
  methods: {
    async sendQuery() {
      if (!this.userInput.trim()) return;

      this.addMessage(this.userInput, true);
      this.setLoading(true);

      try {
        const data = await this.fetchRecommendations(this.userInput);
        this.handleResponse(data, '다음은 추천 게임입니다:');
        this.previousInput = this.userInput;
      } catch {
        this.addMessage('추천 게임을 가져오는 중 오류가 발생했습니다.', false);
      } finally {
        this.setLoading(false);
        this.userInput = '';
        this.scrollToBottom();
      }
    },
    async getMoreRecommendations() {
      if (!this.previousInput.trim()) return;

      this.addMessage('다른 게임은 없어?', true);
      this.setLoading(true);

      try {
        const data = await this.fetchRecommendations(this.previousInput);
        this.handleResponse(data, '다음은 추가 추천 게임입니다:');
      } catch {
        this.addMessage('추가 추천 게임을 가져오는 중 오류가 발생했습니다.', false);
      } finally {
        this.setLoading(false);
        this.scrollToBottom();
      }
    },
    async fetchRecommendations(input) {
      const response = await fetch(`http://localhost:8000/api/recommendations/games/?user_input=${encodeURIComponent(input)}`);
      if (!response.ok) throw new Error(`Error: ${response.statusText}`);
      return response.json();
    },
    handleResponse(data, botText) {
      this.removeLoadingMessage();
      if (data.similar_games) {
        this.addMessage(botText, false, data.similar_games.slice(0, 4));
      } else {
        this.addMessage(data.error || '추천 게임을 찾을 수 없습니다.', false);
      }
    },
    addMessage(text, isUser, games = []) {
      this.messages.push({ text, isUser, games });
    },
    setLoading(isLoading) {
      this.loading = isLoading;
      if (isLoading) {
        this.addMessage('게임 추천 중입니다...', false);
      } else {
        this.removeLoadingMessage();
      }
    },
    removeLoadingMessage() {
      this.messages = this.messages.filter(message => message.text !== '게임 추천 중입니다...');
    },
    scrollToBottom() {
      this.$nextTick(() => {
        const chatContent = this.$refs.chatContent;
        if (chatContent && chatContent.$el) {
          const messages = this.$refs.message;
          if (messages && messages.length > 0) {
            const lastMessage = messages[messages.length - 1];
            lastMessage.scrollIntoView({ behavior: 'smooth', block: 'end' });
          }
        }
      });
    },
    messageClass(message, isInner = false) {
      const baseClass = message.isUser ? 'user-message' : 'bot-message';
      return isInner ? baseClass : `${baseClass}-container`;
    },
  },
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
  left: 0;
  width: 100%;
  max-width: 800px;
  background: #fff;
  padding: 10px;
  box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.1);
  margin: 0 auto;
}

.game-cards {
  margin-top: 10px;
  display: flex;
  flex-wrap: wrap;
}
</style>
