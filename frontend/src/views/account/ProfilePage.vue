<template>
    <div class="profile-page">
        <h1>프로필</h1>
        <div v-if="user">
            <p>사용자 이름: {{ user.username }}</p>
            <p>닉네임: {{ user.nickname }}</p> <!-- 닉네임 추가 -->
            <v-btn color="primary" @click="showEditModal = true">정보 수정</v-btn>
        </div>
        <div v-if="favorites && favorites.length">
            <h2>즐겨찾기한 게임</h2>
            <v-row class="game-cards">
                <game-card v-for="game in formattedFavorites" :key="game.id" :game="game" />
            </v-row>
        </div>
        <div v-else>
            <p>즐겨찾기한 게임이 없습니다.</p>
        </div>

        <v-dialog v-model="showEditModal" persistent max-width="600px">
            <v-card>
                <v-card-title>
                    <span class="headline">계정 정보 수정</span>
                </v-card-title>
                <v-card-text>
                    <v-container>
                        <v-row>
                            <v-col cols="12">
                                <v-text-field v-model="editData.nickname" label="닉네임" /> <!-- 닉네임 필드 추가 -->
                            </v-col>
                            <v-col cols="12">
                                <v-text-field v-model="editData.currentPassword" label="현재 비밀번호" type="password" />
                            </v-col>
                            <v-col cols="12">
                                <v-text-field v-model="editData.newPassword" label="새 비밀번호" type="password" />
                            </v-col>
                            <v-col cols="12">
                                <v-text-field v-model="editData.confirmPassword" label="새 비밀번호 확인" type="password" />
                            </v-col>
                        </v-row>
                    </v-container>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1" text @click="showEditModal = false">취소</v-btn>
                    <v-btn color="blue darken-1" text @click="updateProfile">저장</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </div>
</template>

<script>
import axios from 'axios';
import GameCard from '@/views/GameCard.vue';

export default {
    components: {
        GameCard
    },
    data() {
        return {
            user: null,
            favorites: [],
            showEditModal: false,
            editData: {
                nickname: '',
                currentPassword: '',
                newPassword: '',
                confirmPassword: ''
            },
            errorMessage: ''
        };
    },
    computed: {
        formattedFavorites() {
            return this.favorites.map(favorite => ({
                image_url: favorite.game_image,
                name: favorite.game_name,
                review_summary: favorite.game_review,
                price: favorite.game_price,
                store_url: favorite.game_url,
                id: favorite.id
            }));
        }
    },
    async mounted() {
        try {
            const accessToken = localStorage.getItem('access');
            if (accessToken) {
                const userId = localStorage.getItem('userId');
                console.log('Fetching user data...');
                const userResponse = await axios.get(`http://localhost:8000/api/accounts/profile/${userId}/`, {
                    headers: { 'Authorization': `Bearer ${accessToken}` }
                });
                this.user = userResponse.data;
                this.editData.nickname = this.user.nickname; // 닉네임 설정
                console.log('User data:', this.user);

                console.log('Fetching favorite games...');
                const favoritesResponse = await axios.get('http://localhost:8000/api/recommendations/favorites/', {
                    headers: { 'Authorization': `Bearer ${accessToken}` }
                });
                this.favorites = favoritesResponse.data;
                console.log('Favorite games:', this.favorites);
            } else {
                this.errorMessage = '로그인이 필요합니다.';
            }
        } catch (error) {
            console.error('Error fetching user or favorites:', error);
            this.errorMessage = '정보를 가져오는 중 오류가 발생했습니다.';
        }
    },
    methods: {
        async updateProfile() {
            const { nickname, currentPassword, newPassword, confirmPassword } = this.editData;
            if (newPassword !== confirmPassword) {
                alert('새 비밀번호가 일치하지 않습니다.');
                return;
            }

            try {
                const accessToken = localStorage.getItem('access');
                const userId = localStorage.getItem('userId');
                const response = await axios.patch(`http://localhost:8000/api/accounts/profile/${userId}/`, {
                    nickname, // 닉네임 추가
                    old_password: currentPassword,
                    new_password: newPassword
                }, {
                    headers: { 'Authorization': `Bearer ${accessToken}` }
                });

                if (response.status === 200) {
                    this.user.nickname = nickname;
                    this.showEditModal = false;
                    alert('프로필이 성공적으로 업데이트되었습니다.');
                } else {
                    alert('프로필 업데이트에 실패했습니다.');
                }
            } catch (error) {
                console.error('Error updating profile:', error);
                alert('프로필 업데이트 중 오류가 발생했습니다.');
            }
        }
    }
};
</script>

<style scoped>
.profile-page {
    padding: 20px;
}

.game-cards {
    display: flex;
    flex-wrap: wrap;
}

.game-card-col {
    flex: 0 0 300px;
    max-width: 300px;
    margin-bottom: 20px;
}
</style>