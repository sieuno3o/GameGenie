<template>
    <v-col cols="12" md="3" class="game-card-col">
        <v-card class="game-card">
            <v-img :src="game.image_url" class="game-card-img"></v-img>
            <v-card-title class="game-card-title">{{ game.name }}</v-card-title>
            <v-card-subtitle class="game-card-subtitle">{{ game.review_summary }}</v-card-subtitle>
            <v-card-subtitle class="game-card-subtitle">{{ game.price }}</v-card-subtitle>
            <v-card-actions>
                <v-btn :href="game.store_url" target="_blank">스팀 상점 페이지로 이동</v-btn>
                <v-btn @click="toggleFavorite">{{ isFavorite ? '즐겨찾기 제거' : '즐겨찾기 추가' }}</v-btn>
            </v-card-actions>
        </v-card>
    </v-col>
</template>

<script>
import api from '../api';

export default {
    props: {
        game: {
            type: Object,
            required: true
        }
    },
    data() {
        return {
            isFavorite: false,
            favoriteId: null,
            isLoggedIn: !!localStorage.getItem('access') // 로그인 상태 확인
        };
    },
    methods: {
        async toggleFavorite() {
            if (!this.isLoggedIn) {
                // 로그인되지 않은 경우 알림 메시지 표시 또는 로그인 페이지로 리다이렉트
                alert('로그인이 필요합니다. 로그인 페이지로 이동합니다.');
                this.$router.push({ name: 'login' });
                return;
            }

            const url = this.isFavorite ? `/recommendations/favorites/${this.favoriteId}/` : `/recommendations/favorites/add/`;
            const method = this.isFavorite ? 'delete' : 'post';
            const body = this.isFavorite ? null : {
                game_name: this.game.name,
                game_image: this.game.image_url,
                game_review: this.game.review_summary,
                game_price: this.game.price,
                game_url: this.game.store_url
            };

            console.log(`Sending ${method} request to ${url} with body:`, body);

            try {
                const response = await api({
                    method,
                    url,
                    data: body,
                });
                if (response.status === 200 || response.status === 201 || response.status === 204) {
                    if (method === 'post') {
                        const data = await response.data;
                        this.favoriteId = data.id;
                        this.isFavorite = true;
                    } else if (method === 'delete') {
                        this.favoriteId = null;
                        this.isFavorite = false;
                    }
                    console.log('Favorite toggled successfully');
                } else {
                    console.error('Failed to toggle favorite', response.statusText);
                }
            } catch (error) {
                console.error('Error toggling favorite', error);
            }
        },
    },
    async mounted() {
        if (this.isLoggedIn) {
            try {
                const response = await api.get('/recommendations/favorites/');
                const favorites = response.data;
                const favorite = favorites.find(fav => fav.game_name === this.game.name);
                if (favorite) {
                    this.isFavorite = true;
                    this.favoriteId = favorite.id;
                }
            } catch (error) {
                console.error('Error fetching favorites', error);
            }
        }
    },
}
</script>

<style scoped>
.game-card-col {
    width: 300px;
}

.game-card {
    overflow: hidden;
    height: 350px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    width: 100%;
}

.game-card-img {
    object-fit: cover;
    height: 150px;
    width: 100%;
}

.game-card-title {
    height: 50px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.game-card-subtitle {
    height: 20px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
</style>
