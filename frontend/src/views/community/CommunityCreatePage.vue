<template>
  <div class="community-create-container">
    <span class="createHeading heading1">게시글 작성</span>
    <form @submit.prevent="submitForm" class="formBox">
      <!-- 필수 입력 항목 안내 -->
      <p class="requiredNotice">* 필수 입력 항목</p>
      <!-- 카테고리 -->
      <div class="form-group">
        <label for="category">카테고리 <span class="required">*</span></label>
        <select id="category" v-model="form.category" required>
          <option disabled value="">카테고리를 선택해 주세요</option>
          <option v-for="option in categories" :key="option.key" :value="option.key">
            {{ option.value }}
          </option>
        </select>
      </div>
      <!-- 제목 -->
      <div class="form-group">
        <label for="title">제목 <span class="required">*</span></label>
        <input type="text" id="title" v-model="form.title" required>
      </div>
      <!-- 내용 -->
      <div class="form-group">
        <label for="content">내용 <span class="required">*</span></label>
        <textarea id="content" v-model="form.content" rows="10" required></textarea>
      </div>
      <!-- 이미지 파일 -->
      <div class="form-group">
        <label for="image">이미지 파일</label>
        <div class="flex-between">
          <input type="file" id="image" @change="handleFileUpload">
          <button type="submit" class="createButton">글 작성</button>
        </div>
      </div>
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

<style lang="scss" scoped>
.formBox {
  margin-top: 20px;
}

.community-create-container {
  max-width: 1000px;
  min-width: 600px;
  padding: 30px;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 10px;
  color: #333;
}

.required {
  color: red;
}

.requiredNotice {
  color: red;
  font-size: 14px;
}

input[type="text"],
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
  width: 100%;
  padding: 10px;
  border: 2px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
  background-color: #f8f8f8;
}

.createButton {
  border: 2px solid #ccc;
  border-radius: 5px;
  cursor: pointer;
  width: 120px;
  height: 53px;
  background-color: $MAIN-COLOR-SKYBLUE;
  color: #000;
  margin-left: 20px;
}

button:hover {
  background-color: $HOVER-COLOR;
}
</style>
