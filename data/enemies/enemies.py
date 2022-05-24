from rpg.combat import Enemy

enemies = [
    Enemy(name="Small Slime", location="plains", hp=26, damage=10, block=0, healing=5, loot={'slime': 3, 'gold': 140}),
    Enemy(name="Giant Beetle", location="plains", hp=40, damage=6, block=25, healing=0, loot={'Chitin': 1}),
    Enemy(name="Wolf", location="forest", hp=60, damage=16, block=0, healing=8, loot={'fur': 4, 'gold': 460}),
    Enemy(name="Giant Spider", location="forest", hp=52, damage=19, block=6, healing=6, loot={'silk': 2, 'gold': 275}),
    Enemy(name="Hyena", location="plains", hp=18, damage=14, block=0, healing=0, loot={'fur': 1, 'gold': 190}),
    Enemy(name="Skeleton", location="crypt", hp=80, damage=26, block=22, healing=0, loot={'bone': 2, 'gold': 686}),
    Enemy(name="Zombie", location="plains", hp=98, damage=28, block=20, healing=10, loot={'bone': 1, 'gold': 840}),
    Enemy(name="Ghoul", location="crypt", hp=60, damage=14, block=0, healing=36, loot={'ectoplasm': 1, 'gold': 360}),
    Enemy(name="Sprite", location="forest", hp=38, damage=14, block=19, healing=19, loot={'magicdust': 3, 'gold': 263}),

]