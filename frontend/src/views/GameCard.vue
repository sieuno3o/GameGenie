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
        };
    },
    methods: {
        async toggleFavorite() {
            const baseUrl = 'http://localhost:8000/api/recommendations';
            const url = this.isFavorite ? `${baseUrl}/favorites/${this.favoriteId}/` : `${baseUrl}/favorites/add/`;
            const method = this.isFavorite ? 'DELETE' : 'POST';
            const body = this.isFavorite ? null : JSON.stringify({
                game_name: this.game.name,
                game_image: this.game.image_url,
                game_review: this.game.review_summary,
                game_price: this.game.price,
                game_url: this.game.store_url
            });

            console.log(`Sending ${method} request to ${url} with body:`, body);

            try {
                const response = await fetch(url, {
                    method,
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('token')}`,
                    },
                    body,
                });
                if (response.ok) {
                    if (method === 'POST') {
                        const data = await response.json();
                        this.favoriteId = data.id;
                    }
                    this.isFavorite = !this.isFavorite;
                    console.log('Favorite toggled successfully');
                } else {
                    console.error('Failed to toggle favorite');
                }
            } catch (error) {
                console.error('Error toggling favorite', error);
            }
        },
    },
    async mounted() {
        try {
            const response = await fetch('http://localhost:8000/api/recommendations/favorites/', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`,
                },
            });
            const favorites = await response.json();
            const favorite = favorites.find(fav => fav.game_name === this.game.name);
            if (favorite) {
                this.isFavorite = true;
                this.favoriteId = favorite.id;
            }
        } catch (error) {
            console.error('Error fetching favorites', error);
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
