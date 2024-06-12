# Generated by Django 4.2 on 2024-06-11 13:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comments', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('comments_likes', models.ManyToManyField(blank=True, related_name='liked_comments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('community_comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reply_comments', to='community.comment')),
                ('reply_likes', models.ManyToManyField(blank=True, related_name='liked_replies', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('action', '액션'), ('first_person_shooter', '1인칭 슈팅'), ('third_person_shooter', '3인칭 슈팅'), ('fighting', '격투 및 무술'), ('shoot_em_up', '슛뎀업'), ('arcade_rhythm', '아케이드 및 리듬'), ('platform_runner', '플랫폼 게임 및 러너'), ('hack_slash', '핵 앤 슬래시'), ('adventure', '어드벤처'), ('metroidvania', '메트로베니아'), ('visual_novel', '비주얼 노벨'), ('adventure_rpg', '어드벤처 RPG'), ('casual', '캐주얼'), ('puzzle', '퍼즐'), ('story_rich', '풍부한 스토리'), ('hidden_object', '히든 오브젝트'), ('rpg', '롤플레잉'), ('jrpg', 'JRPG'), ('roguelike', '로그라이크'), ('action_rpg', '액션 RPG'), ('strategy_rpg', '전략 RPG'), ('turn_based_rpg', '턴제 RPG'), ('party_based', '파티 기반'), ('simulation', '시뮬레이션'), ('building_automation', '건설 및 자동화'), ('dating', '연애'), ('farming_crafting', '농업 및 제작'), ('sandbox_physics', '샌드박스 및 물리'), ('life_sim', '생활 및 몰입형'), ('space_flight', '우주 및 비행'), ('hobby_job', '취미 및 직업'), ('strategy', '전략'), ('card_board', '카드 및 보드'), ('city_settlement', '도시 및 정착'), ('grand_4x', '대전략 및 4X'), ('real_time_strategy', '실시간 전략'), ('tower_defense', '타워 디펜스'), ('turn_based_strategy', '턴제 전략'), ('sports_racing', '스포츠 및 레이싱'), ('all_sports', '개별 스포츠'), ('fishing_hunting', '낚시 및 사냥'), ('racing', '레이싱'), ('racing_sim', '레이싱 시뮬레이션'), ('sports_sim', '스포츠 시뮬레이션'), ('team_sports', '팀 스포츠'), ('sci_fi_cyberpunk', '공상과학 및 사이버펑크'), ('horror', '공포'), ('mystery_detective', '미스터리 및 수사관'), ('survival', '생존'), ('anime', '애니메이션'), ('open_world', '오픈 월드'), ('space', '우주'), ('lan', 'LAN'), ('mmo', 'MMO'), ('local_party', '로컬 및 파티'), ('multiplayer', '멀티플레이어'), ('singleplayer', '싱글 플레이어'), ('online_competitive', '온라인 경쟁'), ('co_op', '협동'), ('other', '기타')], max_length=50)),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('link', models.URLField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='community_images/')),
                ('video', models.FileField(blank=True, null=True, upload_to='community_videos/')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('community_like', models.ManyToManyField(blank=True, related_name='liked_communities', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='community',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='community.community'),
        ),
        migrations.AddField(
            model_name='comment',
            name='parent_comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='community.comment'),
        ),
    ]
