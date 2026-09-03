"""
FormaCore - Core Data Models

Tämä tiedosto määrittelee FormaCoren digitaalisen kaksosen
perusrakenteen.

Periaate:

INPUT
  ↓
PERCEPTION
  ↓
RECONSTRUCTION
  ↓
SCENE GRAPH
  ↓
DIGITAL TWIN

GLB on vain yksi mahdollinen esitysmuoto.
Scene-malli on FormaCoren varsinainen tietolähde.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, Tuple


# ============================================================
# PERUSMATEMATIIKKA
# ============================================================

@dataclass
class Vector3:
    """3D-koordinaatti tai mitta."""

    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def to_list(self) -> List[float]:
        return [self.x, self.y, self.z]


@dataclass
class Transform:
    """Objektin sijainti, rotaatio ja skaala."""

    position: Vector3 = field(default_factory=Vector3)

    rotation: Vector3 = field(default_factory=Vector3)

    scale: Vector3 = field(
        default_factory=lambda: Vector3(1.0, 1.0, 1.0)
    )


# ============================================================
# MATERIAALI
# ============================================================

@dataclass
class Material:
    """
    Digitaalisen pinnan materiaali.

    Esimerkiksi:
    - maalattu seinä
    - parketti
    - laatta
    - marmori
    """

    id: str

    name: str

    type: str

    color: Optional[str] = None

    texture: Optional[str] = None

    metadata: Dict[str, Any] = field(default_factory=dict)


# ============================================================
# PINTA
# ============================================================

@dataclass
class Surface:
    """
    Fyysinen pinta rakennuksessa.

    Esimerkiksi:
    - keittiön lattia
    - olohuoneen seinä
    - keittiötaso
    """

    id: str

    type: str

    area: float = 0.0

    material_id: Optional[str] = None

    room_id: Optional[str] = None

    metadata: Dict[str, Any] = field(default_factory=dict)


# ============================================================
# OVI
# ============================================================

@dataclass
class Door:
    """Huoneen tai rakennuksen ovi."""

    id: str

    width: float = 0.9

    height: float = 2.1

    transform: Transform = field(default_factory=Transform)

    room_a: Optional[str] = None

    room_b: Optional[str] = None

    metadata: Dict[str, Any] = field(default_factory=dict)


# ============================================================
# IKKUNA
# ============================================================

@dataclass
class Window:
    """Rakennuksen ikkuna."""

    id: str

    width: float = 1.2

    height: float = 1.2

    sill_height: float = 0.9

    transform: Transform = field(default_factory=Transform)

    room_id: Optional[str] = None

    metadata: Dict[str, Any] = field(default_factory=dict)


# ============================================================
# SEINÄ
# ============================================================

@dataclass
class Wall:
    """Rakennuksen seinä."""

    id: str

    start: Vector3

    end: Vector3

    height: float = 2.7

    thickness: float = 0.15

    room_id: Optional[str] = None

    material_id: Optional[str] = None

    metadata: Dict[str, Any] = field(default_factory=dict)


# ============================================================
# OBJEKTI / KALUSTE
# ============================================================

@dataclass
class SceneObject:
    """
    Digitaalisen kaksosen objekti.

    Esimerkiksi:
    - sohva
    - keittiökaappi
    - jääkaappi
    - ruokapöytä
    - sänky
    - valaisin
    """

    id: str

    type: str

    name: str

    transform: Transform = field(default_factory=Transform)

    room_id: Optional[str] = None

    material_id: Optional[str] = None

    dimensions: Vector3 = field(default_factory=Vector3)

    confidence: float = 1.0

    source: Optional[str] = None

    metadata: Dict[str, Any] = field(default_factory=dict)


# ============================================================
# HUONE
# ============================================================

@dataclass
class Room:
    """
    Digitaalisen kaksosen semanttinen huone.

    Forma ei käsittele vain geometriaa.

    Se tietää esimerkiksi:
        room.type = "kitchen"
        room.area = 14.2

    Tämä mahdollistaa myöhemmin:
        "Vaihda keittiön lattia."
        "Paljonko keittiön remontti maksaa?"
        "Lisää saareke."
    """

    id: str

    type: str

    name: str

    area: float = 0.0

    floor_level: int = 0

    walls: List[str] = field(default_factory=list)

    doors: List[str] = field(default_factory=list)

    windows: List[str] = field(default_factory=list)

    surfaces: List[str] = field(default_factory=list)

    objects: List[str] = field(default_factory=list)

    metadata: Dict[str, Any] = field(default_factory=dict)


# ============================================================
# KERROS
# ============================================================

@dataclass
class Floor:
    """Rakennuksen kerros."""

    id: str

    level: int

    elevation: float = 0.0

    rooms: List[str] = field(default_factory=list)

    metadata: Dict[str, Any] = field(default_factory=dict)


# ============================================================
# LÄHDEAINEISTO
# ============================================================

@dataclass
class SourceAsset:
    """
    Alkuperäinen aineisto, josta digitaalinen kaksonen
    on muodostettu.

    Esimerkiksi:
        floorplan.pdf
        kitchen.jpg
        apartment_video.mp4
    """

    id: str

    filename: str

    asset_type: str

    path: Optional[str] = None

    url: Optional[str] = None

    metadata: Dict[str, Any] = field(default_factory=dict)


# ============================================================
# DIGITAL TWIN / SCENE
# ============================================================

@dataclass
class Scene:
    """
    FORMACOREN TÄRKEIN OBJEKTI.

    Tämä on digitaalisen kaksosen lähde.

    Kaikki muu voidaan rakentaa tämän ympärille:
        - 3D
        - GLB
        - viewer
        - materiaalivaihdot
        - kustannuslaskenta
        - AI
        - lead generation
        - analytiikka
    """

    id: str

    property_id: Optional[str] = None

    name: str = "Forma Scene"

    units: str = "metric"

    floors: Dict[str, Floor] = field(default_factory=dict)

    rooms: Dict[str, Room] = field(default_factory=dict)

    walls: Dict[str, Wall] = field(default_factory=dict)

    doors: Dict[str, Door] = field(default_factory=dict)

    windows: Dict[str, Window] = field(default_factory=dict)

    surfaces: Dict[str, Surface] = field(default_factory=dict)

    objects: Dict[str, SceneObject] = field(default_factory=dict)

    materials: Dict[str, Material] = field(default_factory=dict)

    sources: Dict[str, SourceAsset] = field(default_factory=dict)

    metadata: Dict[str, Any] = field(default_factory=dict)

    version: int = 1

    # --------------------------------------------------------
    # HUONE
    # --------------------------------------------------------

    def add_room(self, room: Room) -> None:
        self.rooms[room.id] = room

    # --------------------------------------------------------
    # SEINÄ
    # --------------------------------------------------------

    def add_wall(self, wall: Wall) -> None:
        self.walls[wall.id] = wall

        if wall.room_id and wall.room_id in self.rooms:
            room = self.rooms[wall.room_id]

            if wall.id not in room.walls:
                room.walls.append(wall.id)

    # --------------------------------------------------------
    # OVI
    # --------------------------------------------------------

    def add_door(self, door: Door) -> None:
        self.doors[door.id] = door

        if door.room_a and door.room_a in self.rooms:
            if door.id not in self.rooms[door.room_a].doors:
                self.rooms[door.room_a].doors.append(door.id)

        if door.room_b and door.room_b in self.rooms:
            if door.id not in self.rooms[door.room_b].doors:
                self.rooms[door.room_b].doors.append(door.id)

    # --------------------------------------------------------
    # IKKUNA
    # --------------------------------------------------------

    def add_window(self, window: Window) -> None:
        self.windows[window.id] = window

        if window.room_id and window.room_id in self.rooms:
            if window.id not in self.rooms[window.room_id].windows:
                self.rooms[window.room_id].windows.append(window.id)

    # --------------------------------------------------------
    # PINTA
    # --------------------------------------------------------

    def add_surface(self, surface: Surface) -> None:
        self.surfaces[surface.id] = surface

        if surface.room_id and surface.room_id in self.rooms:
            if surface.id not in self.rooms[surface.room_id].surfaces:
                self.rooms[surface.room_id].surfaces.append(surface.id)

    # --------------------------------------------------------
    # OBJEKTI
    # --------------------------------------------------------

    def add_object(self, obj: SceneObject) -> None:
        self.objects[obj.id] = obj

        if obj.room_id and obj.room_id in self.rooms:
            if obj.id not in self.rooms[obj.room_id].objects:
                self.rooms[obj.room_id].objects.append(obj.id)

    # --------------------------------------------------------
    # MATERIAALI
    # --------------------------------------------------------

    def add_material(self, material: Material) -> None:
        self.materials[material.id] = material

    # --------------------------------------------------------
    # KERROS
    # --------------------------------------------------------

    def add_floor(self, floor: Floor) -> None:
        self.floors[floor.id] = floor

    # --------------------------------------------------------
    # MATERIAALIN VAIHTO
    # --------------------------------------------------------

    def change_material(
        self,
        surface_id: str,
        material_id: str
    ) -> bool:
        """
        Vaihtaa olemassa olevan pinnan materiaalin.

        Tärkeää:
        Geometriaa ei tarvitse rakentaa uudelleen.
        """

        if surface_id not in self.surfaces:
            return False

        if material_id not in self.materials:
            return False

        self.surfaces[surface_id].material_id = material_id

        self.version += 1

        return True

    # --------------------------------------------------------
    # OBJEKTIN MATERIAALIN VAIHTO
    # --------------------------------------------------------

    def change_object_material(
        self,
        object_id: str,
        material_id: str
    ) -> bool:

        if object_id not in self.objects:
            return False

        if material_id not in self.materials:
            return False

        self.objects[object_id].material_id = material_id

        self.version += 1

        return True

    # --------------------------------------------------------
    # SERIALISOINTI
    # --------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        """
        Muuttaa koko Scene-rakenteen JSON-yhteensopivaksi
        Python-sanakirjaksi.
        """

        return asdict(self)

    # --------------------------------------------------------
    # YHTEENVETO
    # --------------------------------------------------------

    def summary(self) -> Dict[str, Any]:

        return {
            "scene_id": self.id,
            "property_id": self.property_id,
            "version": self.version,
            "floors": len(self.floors),
            "rooms": len(self.rooms),
            "walls": len(self.walls),
            "doors": len(self.doors),
            "windows": len(self.windows),
            "surfaces": len(self.surfaces),
            "objects": len(self.objects),
            "materials": len(self.materials),
            "sources": len(self.sources)
        }


# ============================================================
# FACTORY
# ============================================================

def create_empty_scene(
    scene_id: str,
    property_id: Optional[str] = None,
    name: str = "Forma Scene"
) -> Scene:
    """
    Luo tyhjän FormaCore-scenen.
    """

    return Scene(
        id=str(scene_id),
        property_id=str(property_id) if property_id else None,
        name=name
    )
