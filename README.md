# 🎮 GameGenie 🎮

<img src="https://github.com/sieuno3o/GameGenie/assets/160442750/2eef9f38-9665-4518-b797-e23d010c741b">

SPARTA와 고용노동부에서 진행하는 내일배움캠프의 AI 6기 최종 프로젝트 팀 GG이 제작한 웹 페이지입니다. 선호하는 게임이나 게임 장르를 입력하면 AI를 이용하여 비슷한 게임을 추천해주는 사이트를 제작 했습니다.

<br>
<br>

## 목차

- [개발 기간](#개발-기간)
- [주요 기능](#주요-기능)
- [문서](#문서)
- [기술 스택](#기술-스택)

<br>

## 개발 기간

🕓 2024. 05. 13. (월) ~

<br>

## 주요 기능

### 계정 관련 기능

#### 1. 회원가입

<img src="https://github.com/sieuno3o/GameGenie/assets/160442750/8216b8b3-13e9-43f3-8be0-bf77819870cb">

- 아이디, 비밀번호, 이메일, 닉네임 (필수) / 프로필 사진 (선택)
- 비밀번호를 제외한 모든 사항 중복체크
- 비밀번호 암호화 (SHA-256)

#### 2. 로그인

<img src="https://github.com/sieuno3o/GameGenie/assets/160442750/f7503157-bc72-49ff-90c1-7b0d480698ef">

- 아이디, 비밀번호 입력
- DB 값 검증

#### 3. 로그아웃

#### 4. 회원정보 수정

#### 5. 회원 탈퇴

<br> 

### 게임 검색 관련 기능

#### 1. 메인 페이지의 입력창에 게임 추천 텍스트 입력 가능

<img src="https://github.com/sieuno3o/GameGenie/assets/160442750/2d86d461-22f4-4605-a0f4-efc7f3c6726e">

#### 2. openai의 GPT를 이용해 게임 추천 받기 가능

<img src="https://github.com/sieuno3o/GameGenie/assets/160442750/110f0e30-2e0b-4de4-9cd1-94a0bbe8d470">

- 추천 받은 게임들의 정보를 BeautifulSoup를 이용해 가져온 후 사용자에게 카드형태로 표시


#### 3. 검색어 추천 기능

- 검색창에 게임 장르 입력시 비슷한 장르를 유도 추천

<img src="https://github.com/sieuno3o/GameGenie/assets/160442750/683b4487-89d9-42ec-9978-ed367735d6e3"> 

<br>

### 커뮤니티 관련 기능

<br>

## 문서

- [📖 GG S.A.](https://www.notion.so/teamsparta/S-A-GG-f171c28b31bd4d85b210cf13c19da9b3)
- [📌 기능정의서 및 정책서](https://docs.google.com/spreadsheets/d/1hobOW0uL0eCD4xPE-cuJ8muZjCl3EkYzNvOXJbEfCd0/edit#gid=0)
- [📂 ERD](https://dbdiagram.io/d/6655adcdb65d933879dcd4bb)
- [🖌️ 와이어프레임](https://www.figma.com/file/qV9SY9bMTZ8krWhaOsa84h?embed_host=notion&kind=file&node-id=0%3A1&t=oAZOhWUeoI0PgmFp-1&viewer=1)

<br>

## 기술 스택

<div align="center">
<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">
<img src="https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=flask&logoColor=white">
<img src="https://img.shields.io/badge/diagrams-F08705?style=for-the-badge&logo=diagrams.net&logoColor=white">
<br>
<img src="https://img.shields.io/badge/html5-E34F26?style=for-the-badge&logo=html5&logoColor=white">
<img src="https://img.shields.io/badge/css-1572B6?style=for-the-badge&logo=css3&logoColor=white">
<img src="https://img.shields.io/badge/javascript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black">
<img src="https://img.shields.io/badge/bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white">
<br>
<img src="https://img.shields.io/badge/git-F05032?style=for-the-badge&logo=git&logoColor=white">
<img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white">
<img src="https://img.shields.io/badge/Slack-4A154B?style=for-the-badge&logo=Slack&logoColor=white">
<img src="https://img.shields.io/badge/discord-5865F2?style=for-the-badge&logo=discord&logoColor=white">
<br>
<img src="https://img.shields.io/badge/notion-000000?style=for-the-badge&logo=notion&logoColor=white">
<img src="https://img.shields.io/badge/google-sheets-34A853?style=for-the-badge&logo=google-sheets&logoColor=white">
<img src="https://img.shields.io/badge/figma-F24E1E?style=for-the-badge&logo=figma&logoColor=white">
</div>