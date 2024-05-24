<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1>게임 추천</h1>
        <v-text-field
          v-model="userInput"
          label="검색어를 입력하세요"
          @keyup.enter="sendQuery"
        ></v-text-field>
        <v-btn @click="sendQuery">검색</v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <div v-for="(message, index) in messages" :key="index" class="chat-message">
          <div :class="{'user-message': message.isUser, 'bot-message': !message.isUser}">
            {{ message.text }}
          </div>
        </div>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" v-if="recommendedGames.length > 0">
        <h2>추천 게임</h2>
        <v-row>
          <v-col v-for="game in recommendedGames" :key="game.appid" cols="12" md="4">
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
          this.recommendedGames = data.similar_games;
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
          this.recommendedGames = data.similar_games;
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

<style scoped>
.chat-message {
  margin: 10px 0;
}
.user-message {
  text-align: right;
  color: blue;
}
.bot-message {
  text-align: left;
  color: green;
}
</style>
