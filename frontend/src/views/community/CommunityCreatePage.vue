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
      <div class="form-group">
        <label for="url">URL</label>
        <input type="url" id="url" v-model="form.url">
      </div>
      <div class="form-group">
        <label for="image">이미지 파일</label>
        <input type="file" id="image" @change="handleFileUpload">
      </div>
      <button type="submit">글 작성</button>
    </form>
  </div>
</template>

<script>
import api from '../../api'; // src 폴더에서 불러오기

export default {
  data() {
    return {
      form: {
        title: '',
        category: '',
        content: '',
        url: '',
        image: null
      },
      categories: []
    };
  },
  methods: {
    fetchCategories() {
      api.get('community/categories/')
        .then((response) => {
          this.categories = response.data;
        })
        .catch(error => {
          console.error("카테고리를 불러오는 중 에러가 발생했습니다:", error);
        });
    },
    handleFileUpload(event) {
      this.form.image = event.target.files[0];
    },
    async submitForm() {
      const formData = new FormData();
      formData.append('title', this.form.title);
      formData.append('category', this.form.category);
      formData.append('content', this.form.content);
      formData.append('url', this.form.url);
      if (this.form.image) {
        formData.append('image', this.form.image);
      }

      try {
        const token = localStorage.getItem('access');
        await api.post('community/create/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
            'Authorization': `Bearer ${token}`
          }
        });
        alert('글이 등록되었습니다!');
        this.$router.push({ name: 'communityMain' });
      } catch (error) {
        console.error("폼을 제출하는 중 에러가 발생했습니다:", error);
        alert("글 작성 중 에러가 발생했습니다. 다시 시도해주세요.");
      }
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
  margin-bottom: 10px;
  color: #333;
}

input[type="text"],
input[type="url"],
textarea,
select {
  width: 100%;
  padding: 12px 10px;
  border: 2px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
  background-color: #f8f8f8;
}

input[type="file"] {
  padding: 10px;
  border: 2px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
  background-color: #f8f8f8;
}

button {
  padding: 12px 20px;
  background-color: #007BFF;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #0056b3;
}
</style>
