# 🎮 GameGenie 🎮

<img src="https://media.discordapp.net/attachments/1245260060024635464/1245260081365385216/image.png?ex=66581a53&is=6656c8d3&hm=0f74ae0ede53688516ea4641ebf8d574b79cdaf41f1cbb79361eb072383c9f50&=&format=webp&quality=lossless&width=2160&height=980">

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

<img src="https://media.discordapp.net/attachments/1245260060024635464/1245265002135420948/image.png?ex=66581ee8&is=6656cd68&hm=24345489a5c5afdebb967dacbd7372d730de7922aefa29966124894ccd83567c&=&format=webp&quality=lossless&width=2160&height=958">

- 아이디, 비밀번호, 이메일, 닉네임 (필수) / 프로필 사진 (선택)
- 비밀번호를 제외한 모든 사항 중복체크
- 비밀번호 암호화 (SHA-256)

#### 2. 로그인

<img src="https://media.discordapp.net/attachments/1245260060024635464/1245264222288482305/image.png?ex=66581e2e&is=6656ccae&hm=e316da53d8d01b8a632bc9bc76a48172d7dd5014773834ff77f33df2e5bd6efe&=&format=webp&quality=lossless&width=2160&height=964">

- 아이디, 비밀번호 입력
- DB 값 검증

#### 3. 로그아웃

#### 4. 회원정보 수정

#### 5. 회원 탈퇴

<br> 

### 게임 검색 관련 기능

#### 1. 메인 페이지의 입력창에 게임 추천 텍스트 입력 가능

<img src="https://cdn.discordapp.com/attachments/1245260060024635464/1245268855765467167/2024-05-29_155208.png?ex=6658227f&is=6656d0ff&hm=79683030f3a64fdb1786fea369572b40128ae49bea717dfc23841051635c72f3&">

#### 2. openai의 GPT를 이용해 게임 추천 받기 가능

<img src="https://cdn.discordapp.com/attachments/1245260060024635464/1245271631174176768/2024-05-29_160419.png?ex=66582514&is=6656d394&hm=488a6a06250e3382f4a48f55a2353de325d195553e9957fbc2d541baa42be67d&">

- 추천 받은 게임들의 정보를 BeautifulSoup를 이용해 가져온 후 사용자에게 카드형태로 표시

<img src="https://cdn.discordapp.com/attachments/1245260060024635464/1245271630721056798/2024-05-29_160357.png?ex=66582514&is=6656d394&hm=b4fa96040128d2b92dd264a1f671f0466f16e9488cc2ff60878d527384b2b7be&">


#### 3. 검색어 추천 기능

- 검색창에 게임 장르 입력시 비슷한 장르를 유도 추천

<img src="https://cdn.discordapp.com/attachments/1245260060024635464/1245277391115386910/image.png?ex=66582a72&is=6656d8f2&hm=e916dce22c17cab62bdbf786611aac82869c4d098e882ea8617ad73a30ee2963&"> 

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