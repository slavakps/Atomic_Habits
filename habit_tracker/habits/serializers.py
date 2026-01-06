from rest_framework import serializers

from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = [
            'id',
            'user',
            'action',
            'place',
            'time',
            'is_reward',
            'related_habit',
            'reward',
            'periodicity',
            'duration',
            'is_public',
        ]
        read_only_fields = ['id', 'user']

    def validate(self, data):

        reward = data.get("reward")
        related_habit = data.get("related_habit")
        duration = data.get("duration")
        periodicity = data.get("periodicity")
        is_reward = data.get("is_reward")

        # 1️⃣ Нельзя одновременно выбрать награду и связанную привычку
        if reward and related_habit:
            raise serializers.ValidationError(
                {"reward": "Нельзя одновременно указывать вознаграждение и связанную привычку"}
            )

        # 2️⃣ Длительность ≤ 120 сек
        if duration and duration > 120:
            raise serializers.ValidationError({"duration": "Время выполнения привычки не может превышать 120 секунд"})

        # 3️⃣ Периодичность 1–7
        if periodicity is not None and not (1 <= periodicity <= 7):
            raise serializers.ValidationError({"periodicity": "Периодичность привычки должна быть от 1 до 7 дней"})

        # 4️⃣ Привычка-вознаграждение не может иметь связанную привычку
        if is_reward and related_habit:
            raise serializers.ValidationError(
                {"related_habit": "Привычка-вознаграждение не может иметь связанную привычку"}
            )

        return data
