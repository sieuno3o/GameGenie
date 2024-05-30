<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <div v-for="(message, index) in messages" :key="index" class="chat-message">
          <div :class="{ 'user-message': message.isUser, 'bot-message': !message.isUser }">
            {{ message.text }}
          </div>
        </div>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" v-if="recommendedGames.length > 0">
        <h2>추천 게임</h2>
        <v-row>
          <v-col v-for="game in recommendedGames" :key="game.appid" cols="12" md="3">
            <v-card>
              <v-img :src="game.image_url" height="200px"></v-img>
              <v-card-title>{{ game.name }}</v-card-title>
              <v-card-subtitle>{{ game.review_summary }}</v-card-subtitle>
              <v-card-subtitle>{{ game.price }}</v-card-subtitle>
              <v-card-actions>
                <v-btn :href="game.store_url" target="_blank">스팀 상점 페이지로 이동</v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
    <!-- 검색어 입력 부분을 화면 하단에 고정 -->
    <div class="search-bar">
      <v-row>
        <v-col cols="12">
          <v-text-field v-model="userInput" label="검색어를 입력하세요" @keyup.enter="sendQuery" append-outer-icon="mdi-magnify"
            @click:append-outer="sendQuery">
          </v-text-field>
        </v-col>
      </v-row>
    </div>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      userInput: '',
      messages: [],
      recommendedGames: [],
      error: null,
      previousInput: '',
    };
  },
  mounted() {
    if (this.$route.query.user_input) {
      this.userInput = this.$route.query.user_input;
      this.sendQuery();
    }
  },
  methods: {
    async sendQuery() {
      if (this.userInput.trim() === '') return;

      this.messages.push({ text: this.userInput, isUser: true });

      try {
        const response = await fetch(`http://localhost:8000/api/recommendations/?user_input=${encodeURIComponent(this.userInput)}`);
        if (!response.ok) {
          throw new Error(`Error: ${response.statusText}`);
        }
        const data = await response.json();

        if (data.similar_games) {
          this.messages.push({ text: '다음은 추천 게임입니다:', isUser: false });
          this.recommendedGames = data.similar_games.slice(0, 4);
        } else {
          this.messages.push({ text: data.error || '추천 게임을 찾을 수 없습니다.', isUser: false });
        }

        this.previousInput = this.userInput;
      } catch (error) {
        this.messages.push({ text: '추천 게임을 가져오는 중 오류가 발생했습니다.', isUser: false });
        this.error = error.toString();
      }

      this.userInput = '';
    },
    async getMoreRecommendations() {
      if (this.previousInput.trim() === '') return;

      this.messages.push({ text: '다른 게임은 없어?', isUser: true });

      try {
        const response = await fetch(`http://localhost:8000/api/recommendations/?user_input=${encodeURIComponent(this.previousInput)}`);
        if (!response.ok) {
          throw new Error(`Error: ${response.statusText}`);
        }
        const data = await response.json();

        if (data.similar_games) {
          this.messages.push({ text: '다음은 추가 추천 게임입니다:', isUser: false });
          this.recommendedGames = data.similar_games.slice(0, 4);
        } else {
          this.messages.push({ text: data.error || '추가 추천 게임을 찾을 수 없습니다.', isUser: false });
        }
      } catch (error) {
        this.messages.push({ text: '추가 추천 게임을 가져오는 중 오류가 발생했습니다.', isUser: false });
        this.error = error.toString();
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.user-message {
  position: relative;
  padding: 20px;
  min-width: 200px;
  min-height: 60px;
  color: #FFF;
  border-radius: 10px;
  background-color: white;
  border: 1px solid rgb(147, 147, 147);
  color: black;
}

.user-message:before,
.user-message:after {
  content: "";
  position: absolute;
  border-top: 10px solid transparent;
  border-bottom: 10px solid transparent;
}

.user-message:before {
  border-left: 31px solid rgb(147, 147, 147);
  top: 21px;
  right: -33px;
  z-index: 1;
}

.user-message:after {
  border-left: 30px solid white;
  top: 21px;
  right: -30px;
  z-index: 2;
}

.bot-message {
  text-align: left;
  color: green;
}

.search-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  background: #fff;
  padding: 10px;
  box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.1);
}
</style>
