import time

class DifficultyManager:
    def __init__(self):
        # Difficulty levels
        self.difficulty_level = 1  # Start at level 1 (Easy)
        self.max_difficulty = 5
        
        # Performance tracking
        self.deaths_count = 0
        self.survival_time = 0
        self.last_death_time = 0
        self.enemies_killed = 0
        self.bullets_fired = 0
        self.bullets_hit = 0
        self.accuracy = 0
        
        # Difficulty parameters
        self.enemy_spawn_rate = 1500  # milliseconds
        self.platform_spawn_rate = 1700
        self.enemy_speed = 2
        self.platform_speed = 1
        
        # DDA thresholds
        self.death_threshold_increase = 3  # Deaths before making easier
        self.survival_threshold_increase = 10  # Seconds survival for harder
        self.accuracy_threshold = 0.7  # 70% accuracy for harder
        
    #Update player performance metrics
    def update_performance(self, current_time, is_death=False, bullet_fired=False, bullet_hit=False):
        self.survival_time = current_time

        if is_death:
            self.deaths_count += 1
            self.last_death_time = current_time

        if bullet_fired:
            self.bullets_fired += 1

        if bullet_hit:
            self.bullets_hit += 1
            self.enemies_killed += 1

        if self.bullets_fired > 0:
            self.accuracy = self.bullets_hit / self.bullets_fired
    
    #Main DDA algorithm - adjusts difficulty based on performance
    def adjust_difficulty(self):
        
        # MAKE IT EASIER - Player is struggling
        if self.deaths_count >= self.death_threshold_increase and self.difficulty_level > 1:
            self.difficulty_level -= 1
            self.deaths_count = 0  
            self._apply_difficulty_settings()
            return "EASIER"
        
        # MAKE IT HARDER - Player is doing well
        elif (self.survival_time >= self.survival_threshold_increase and 
              self.accuracy >= self.accuracy_threshold and 
              self.difficulty_level < self.max_difficulty):
            self.difficulty_level += 1
            self._apply_difficulty_settings()
            return "HARDER"
            
        return "SAME"
    
    #Apply difficulty settings based on current level
    def _apply_difficulty_settings(self):
        if self.difficulty_level == 1:  # Very Easy
            self.enemy_spawn_rate = 1500
            self.platform_spawn_rate = 1700
            self.enemy_speed = 2
            self.platform_speed = 1
            
        elif self.difficulty_level == 2:  # Easy
            self.enemy_spawn_rate = 1450
            self.platform_spawn_rate = 1700
            self.enemy_speed = 2.5
            self.platform_speed = 1.5
            
        elif self.difficulty_level == 3:  # Medium
            self.enemy_spawn_rate = 1400
            self.platform_spawn_rate = 1700
            self.enemy_speed = 3
            self.platform_speed = 2
            
        elif self.difficulty_level == 4:  # Hard
            self.enemy_spawn_rate = 1350
            self.platform_spawn_rate = 1700
            self.enemy_speed = 3.5
            self.platform_speed = 2.5
            
        elif self.difficulty_level == 5:  # Very Hard
            self.enemy_spawn_rate = 1300
            self.platform_spawn_rate = 1700
            self.enemy_speed = 3.5
            self.platform_speed = 3
    
    # Return difficulty name as string
    def get_difficulty_name(self):
        names = {1: "VERY EASY", 2: "EASY", 3: "MEDIUM", 4: "HARD", 5: "VERY HARD"}
        return names.get(self.difficulty_level, "MEDIUM")
    
    def reset(self):
        self.survival_time = 0
        self.enemies_killed = 0
        self.bullets_fired = 0
        self.bullets_hit = 0
        self.accuracy = 0
    
    # Get current performance stats
    def get_stats(self):
        return {
            'difficulty_level': self.difficulty_level,
            'difficulty_name': self.get_difficulty_name(),
            'deaths': self.deaths_count,
            'survival_time': self.survival_time,
            'enemies_killed': self.enemies_killed,
            'accuracy': f"{self.accuracy * 100:.1f}%" if self.bullets_fired > 0 else "0%"
        }