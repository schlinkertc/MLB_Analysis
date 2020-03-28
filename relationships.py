from tables import *

from sqlalchemy.orm import relationship

# one-to-many between game and plays

Play.game = relationship("Game",back_populates="plays")
Game.plays = relationship(
    "Play",order_by=Play.about_endTime,back_populates='game')

# one-to-many relationship between play and pitches
Play.pitches = relationship('Pitch',order_by=Pitch.index,back_populates='play')
Pitch.play = relationship('Play',back_populates='pitches')

# one-to-one relationship between a pitch and it's hit data

Pitch.hitData = relationship(
    'HitData',back_populates='pitch',uselist=False
)

HitData.pitch = relationship(
    'Pitch',back_populates='hitData'
)

# one-to-one relationship between a pitch and it's pitch data 

Pitch.pitchData = relationship(
    'PitchData',back_populates='pitch',uselist=False
)

PitchData.pitch = relationship(
    'Pitch',back_populates='pitchData'
)

# one-to-many: Play --> Hit Data // Play --> Pitch Data

Play.hitData = relationship(
    'HitData',order_by=HitData.index,back_populates='play'
)
HitData.play = relationship('Play',back_populates='hitData',viewonly=True)

Play.pitchData = relationship(
    'PitchData',order_by=PitchData.index,back_populates='play'
)
PitchData.play = relationship('Play',back_populates='pitchData',viewonly=True)