<template>
  <div class="flex-col-center signupPageBox">
    <span class="signupTitle heading3">회원가입</span>
    <div id="id" class="signupInputBox flex-row-left">
      <img src="../../assets/image/account/idIcon.png" class="signupIconImg">
      <input v-model="username" type="text" class="signupInput button2" id="inputId" placeholder="아이디">
    </div>
    <div id="password" class="signupInputBox flex-row-left">
      <img src="../../assets/image/account/passwordIcon.png" class="signupIconImg">
      <input v-model="password" type="password" class="signupInput button2" id="inputPassword" placeholder="비밀번호">
    </div>
    <div id="email" class="signupInputBox flex-row-left">
      <img src="../../assets/image/account/emailIcon.png" class="signupIconImg">
      <input v-model="email" type="text" class="signupInput button2" id="inputEmail" placeholder="이메일">
    </div>
    <div id="nickname" class="signupInputBox flex-row-left">
      <img src="../../assets/image/account/nicknameIcon.png" class="signupIconImg">
      <input v-model="nickname" type="text" class="signupInput button2" id="inputNickname" placeholder="닉네임">
    </div>
    <div class="profileImageBox flex-col-center">
      <img :src="profileImagePreview || defaultImage" class="profileImagePreview" />
      <button @click="triggerFileInput" class="profileImageButton button2">📸 사진 업로드</button>
      <input type="file" ref="fileInput" @change="onImageChange" accept="image/*" class="profileImageInput">
    </div>
    <div v-if="errorMessage" class="errorMessage">{{ errorMessage }}</div>
    <button @click="signup" type="submit" class="signupInputBox" id="signupButton">회원가입</button>
  </div>
</template>

<script>
import api from '../../api'; // api.js를 사용하여 요청을 처리합니다.

export default {
  data() {
    return {
      username: '',
      password: '',
      email: '',
      nickname: '',
      profileImage: null,
      profileImagePreview: null,
      defaultImage: require('../../assets/image/account/profileImgIcon.png'),
      errorMessage: '',
    };
  },
  methods: {
    triggerFileInput() {
      this.$refs.fileInput.click();
    },
    onImageChange(event) {
      const file = event.target.files[0];
      if (file) {
        this.profileImage = file; // 원본 파일 저장
        const reader = new FileReader();
        reader.onload = (e) => {
          this.profileImagePreview = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    },
    async signup() {
      if (!this.username) {
        this.errorMessage = '아이디를 입력해주세요.';
        return;
      }
      if (!this.password) {
        this.errorMessage = '비밀번호를 입력해주세요.';
        return;
      }
      if (!this.email) {
        this.errorMessage = '이메일을 입력해주세요.';
        return;
      }
      if (!this.nickname) {
        this.errorMessage = '닉네임을 입력해주세요.';
        return;
      }

      try {
        const formData = new FormData();
        formData.append('username', this.username);
        formData.append('password', this.password);
        formData.append('email', this.email);
        formData.append('nickname', this.nickname);
        if (this.profileImage) {
          formData.append('profile_image', this.profileImage); // 원본 파일 추가
        }

        const response = await api.post('accounts/create/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });

        if (response.status === 201) {
          alert('회원가입이 완료되었습니다.');
          this.$router.push({ name: 'login' });
        }
      } catch (error) {
        if (error.response && error.response.data) {
          if (error.response.data.username) {
            this.errorMessage = '아이디가 이미 사용 중입니다.';
          } else if (error.response.data.email) {
            this.errorMessage = '이메일 형식이 잘못되었거나 이미 사용 중입니다.';
          } else {
            this.errorMessage = '회원가입에 실패했습니다. 다시 시도해주세요.';
          }
        } else {
          console.error('Signup failed:', error);
          this.errorMessage = '회원가입에 실패했습니다. 다시 시도해주세요.';
        }
      }
    }
  }
};
</script>

<style lang="scss" scoped>
.signupPageBox {
  margin-top: 100px;
}

.signupTitle {
  margin-bottom: 50px;
}

.signupInput {
  width: 100%;
  height: 100%;
  border: 0px;
  outline: none;
  padding-left: 15px;
  border-radius: 5px;
}

.signupIconImg {
  width: 50px;
  padding: 15px;
  border-right: 1px solid rgb(178, 178, 178);
}

.signupInputBox {
  border-width: 1px;
  border-style: solid;
  border-color: rgb(178, 178, 178);
  border-radius: 5px;
  width: 380px;
  height: 50px;
  margin-bottom: 23px;
}

#signupButton {
  background-color: $MAIN-COLOR-SKYBLUE;
  height: 48px;
}

.profileImageBox {
  width: 120px;
}

.profileImageInput {
  display: none;
}

.profileImageButton {
  border: none;
  border-radius: 5px;
  cursor: pointer;
  width: 120px;
  height: 30px;
  margin-top: 10px;
  margin-bottom: 40px;
  background-color: $MAIN-COLOR-SKYBLUE;
}

.profileImagePreview {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 50%;
}

#signupButton {
  margin-bottom: 130px
}

.errorMessage {
  margin-bottom: 20px;
  font-size: 20px;
}
</style>
