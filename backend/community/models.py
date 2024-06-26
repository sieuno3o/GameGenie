from django.db import models
from accounts.models import User


class Community(models.Model):
    CATEGORY_CHOICES = [
        # 액션
        ('action', '액션'),
        ('first_person_shooter', '1인칭 슈팅'),
        ('third_person_shooter', '3인칭 슈팅'),
        ('fighting', '격투 및 무술'),
        ('shoot_em_up', '슛뎀업'),
        ('arcade_rhythm', '아케이드 및 리듬'),
        ('platform_runner', '플랫폼 게임 및 러너'),
        ('hack_slash', '핵 앤 슬래시'),

        # 어드벤처
        ('adventure', '어드벤처'),
        ('metroidvania', '메트로베니아'),
        ('visual_novel', '비주얼 노벨'),
        ('adventure_rpg', '어드벤처 RPG'),
        ('casual', '캐주얼'),
        ('puzzle', '퍼즐'),
        ('story_rich', '풍부한 스토리'),
        ('hidden_object', '히든 오브젝트'),

        # 롤플레잉
        ('rpg', '롤플레잉'),
        ('jrpg', 'JRPG'),
        ('roguelike', '로그라이크'),
        ('action_rpg', '액션 RPG'),
        ('strategy_rpg', '전략 RPG'),
        ('turn_based_rpg', '턴제 RPG'),
        ('party_based', '파티 기반'),

        # 시뮬레이션
        ('simulation', '시뮬레이션'),
        ('building_automation', '건설 및 자동화'),
        ('dating', '연애'),
        ('farming_crafting', '농업 및 제작'),
        ('sandbox_physics', '샌드박스 및 물리'),
        ('life_sim', '생활 및 몰입형'),
        ('space_flight', '우주 및 비행'),
        ('hobby_job', '취미 및 직업'),

        # 전략
        ('strategy', '전략'),
        ('card_board', '카드 및 보드'),
        ('city_settlement', '도시 및 정착'),
        ('grand_4x', '대전략 및 4X'),
        ('real_time_strategy', '실시간 전략'),
        ('tower_defense', '타워 디펜스'),
        ('turn_based_strategy', '턴제 전략'),

        # 스포츠 및 레이싱
        ('sports_racing', '스포츠 및 레이싱'),
        ('all_sports', '개별 스포츠'),
        ('fishing_hunting', '낚시 및 사냥'),
        ('racing', '레이싱'),
        ('racing_sim', '레이싱 시뮬레이션'),
        ('sports_sim', '스포츠 시뮬레이션'),
        ('team_sports', '팀 스포츠'),

        # 테마
        ('sci_fi_cyberpunk', '공상과학 및 사이버펑크'),
        ('horror', '공포'),
        ('mystery_detective', '미스터리 및 수사관'),
        ('survival', '생존'),
        ('anime', '애니메이션'),
        ('open_world', '오픈 월드'),
        ('space', '우주'),

        # 플레이어 지원
        ('lan', 'LAN'),
        ('mmo', 'MMO'),
        ('local_party', '로컬 및 파티'),
        ('multiplayer', '멀티플레이어'),
        ('singleplayer', '싱글 플레이어'),
        ('online_competitive', '온라인 경쟁'),
        ('co_op', '협동'),

        ('other', '기타')
    ]

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=255)
    content = models.TextField()
    link = models.URLField(blank=True, null=True)
    community_like = models.ManyToManyField(User, related_name='liked_communities', blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='community_images/', null=True, blank=True)
    video = models.FileField(upload_to='community_videos/', null=True, blank=True)
    view_count = models.IntegerField(default=0)  # 조회수 필드 추가

    def like(self, user):
        self.community_like.add(user)

    def unlike(self, user):
        self.community_like.remove(user)

    def is_liked_by_user(self, user):
        return self.community_like.filter(id=user.id).exists()

    def get_likes_count(self):
        return self.community_like.count()

    def communitylist_points(self):
        comments_count = self.comments.count()
        comments_count_point = 1 * comments_count

        likes_count = self.community_like.count()
        likes_count_point = 1 * likes_count

        return comments_count_point + likes_count_point


class Comment(models.Model):
    community = models.ForeignKey(
        Community, related_name='comments', on_delete=models.CASCADE)
    comments = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comments_likes = models.ManyToManyField(
        User, related_name='liked_comments', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    def like(self, user):
        self.comments_likes.add(user)

    def unlike(self, user):
        self.comments_likes.remove(user)

    def is_liked_by_user(self, user):
        return self.comments_likes.filter(id=user.id).exists()

    def get_likes_count(self):
        return self.comments_likes.count()


class Reply(models.Model):
    community_comment = models.ForeignKey(
        Comment, related_name='reply_comments', on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    reply_likes = models.ManyToManyField(
        User, related_name='liked_replies', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def like(self, user):
        self.reply_likes.add(user)

    def unlike(self, user):
        self.reply_likes.remove(user)

    def is_liked_by_user(self, user):
        return self.reply_likes.filter(id=user.id).exists()

    def get_likes_count(self):
        return self.reply_likes.count()
