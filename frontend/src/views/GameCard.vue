<template>
    <v-col cols="12" md="3" class="game-card-col">
        <v-card class="game-card">
            <v-img :src="game.image_url" class="game-card-img"></v-img>
            <v-card-title class="game-card-title">{{ game.name }}</v-card-title>
            <v-card-subtitle class="game-card-subtitle">{{ game.review_summary }}</v-card-subtitle>
            <v-card-subtitle class="game-card-subtitle">{{ game.price }}</v-card-subtitle>
            <v-card-actions>
                <v-btn :href="game.store_url" target="_blank">스팀 상점 페이지로 이동</v-btn>
            </v-card-actions>
        </v-card>
    </v-col>
</template>

<script>
export default {
    props: {
        game: {
            type: Object,
            required: true
        }
    }
}
</script>

<style scoped>
.game-card-col {
    width: 300px;
    /* 카드의 고정 너비 */
}

.game-card {
    overflow: hidden;
    height: 350px;
    /* 카드의 고정 높이 */
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    width: 100%;
}

.game-card-img {
    object-fit: cover;
    height: 150px;
    /* 이미지의 고정 높이 */
    width: 100%;
    /* 이미지의 너비를 카드 너비에 맞춤 */
}

.game-card-title {
    height: 50px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.game-card-subtitle {
    height: 20px;
    /* 부제목의 고정 높이 */
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}</style>
