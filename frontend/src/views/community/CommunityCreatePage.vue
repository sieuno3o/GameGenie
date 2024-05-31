<template>
  <div class="community-create-container">
    <h1>게임 커뮤니티 게시글 작성</h1>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="title">제목</label>
        <input type="text" id="title" v-model="form.title" required>
      </div>
      <div class="form-group">
        <label for="category">카테고리</label>
        <select id="category" v-model="form.category" required>
          <option disabled value="">Please select one</option>
          <option v-for="option in categories" :key="option.key" :value="option.key">
            {{ option.value }}
          </option>
        </select>
      </div>
      <div class="form-group">
        <label for="content">내용</label>
        <textarea id="content" v-model="form.content" rows="10" required></textarea>
      </div>
      <button type="submit">글 작성</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios'; 

export default {
  data() {
    return {
      form: {
        title: '',
        category: '',
        content: ''
      },
      categories: []
    };
  },
  methods: {
    fetchCategories() {
      axios.get('http://localhost:8000/api/community/categories')
        .then((response) => { // response 사용
          this.categories = response.data;
        })
        .catch(error => {
          console.error("카테고리를 불러오는 중 에러가 발생했습니다:", error);
        });
    },
    submitForm() {
      axios.post('http://localhost:8000/api/community/create/', this.form)
        .then(() => { // response 제거
          alert('글이 등록되었습니다!');
          this.$router.push({ name: 'CommunityMain' });
        })
        .catch(error => {
          console.error("폼을 제출하는 중 에러가 발생했습니다:", error);
        });
    }
  },
  created() {
    this.fetchCategories();
  }
}
</script>

<style scoped>
.community-create-container {
  max-width: 600px;
  margin: auto;
  padding: 20px;
}
.form-group {
  margin-bottom: 20px;
}
label {
  display: block;
  margin-bottom: 10px; /* 조금 더 여유 있는 간격 */
  color: #333; /* 라벨 텍스트 색상 */
}
input[type="text"], textarea, select {
  width: 100%;
  padding: 12px 10px; /* 패딩 수정 */
  border: 2px solid #ccc; /* 테두리 스타일 */
  border-radius: 4px; /* 둥근 모서리 */
  box-sizing: border-box;
  background-color: #f8f8f8; /* 배경색 변경 */
}
button {
  padding: 12px 20px;
  background-color: #007BFF;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s; /* 부드러운 색상 전환 효과 */
}
button:hover {
  background-color: #0056b3;
}
</style>