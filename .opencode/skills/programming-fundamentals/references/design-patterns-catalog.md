# Design Patterns Catalog

Complete catalog of the 23 Gang of Four (GoF) design patterns with language-agnostic pseudocode examples.

---

## Pattern Categories

- **Creational**: Object creation mechanisms
- **Structural**: Object composition
- **Behavioral**: Communication between objects

---

## Creational Patterns

### 1. Singleton

**Intent:** Ensure a class has only one instance and provide global access to it.

```pseudocode
class Singleton:
  private static instance: Singleton = null
  private data: any
  
  private constructor():
    this.data = initialize_data()
  
  public static get_instance():
    if Singleton.instance == null:
      Singleton.instance = new Singleton()
    return Singleton.instance
  
  public get_data():
    return this.data

// Thread-safe version
class ThreadSafeSingleton:
  private static instance: ThreadSafeSingleton = null
  private static lock: Lock = new Lock()
  
  private constructor():
    // Initialize
  
  public static get_instance():
    if instance == null:
      lock.acquire()
      if instance == null:  // Double-check
        instance = new ThreadSafeSingleton()
      lock.release()
    return instance

// Usage
db1 = Singleton.get_instance()
db2 = Singleton.get_instance()
// db1 === db2 (same instance)
```

**When to Use:**
- Need exactly one instance
- Global access point required
- Resource management (connection pools, loggers)

**Drawbacks:**
- Tight coupling
- Difficult to test
- Can hide dependencies

---

### 2. Factory Method

**Intent:** Define an interface for creating objects, but let subclasses decide which class to instantiate.

```pseudocode
// Product interface
interface Transport:
  deliver(): void

// Concrete products
class Truck implements Transport:
  deliver():
    print("Deliver by land in a truck")

class Ship implements Transport:
  deliver():
    print("Deliver by sea in a ship")

// Creator
abstract class Logistics:
  abstract create_transport(): Transport
  
  plan_delivery():
    transport = this.create_transport()
    transport.deliver()

// Concrete creators
class RoadLogistics extends Logistics:
  create_transport():
    return new Truck()

class SeaLogistics extends Logistics:
  create_transport():
    return new Ship()

// Usage
logistics = new RoadLogistics()
logistics.plan_delivery()  // Uses Truck

logistics = new SeaLogistics()
logistics.plan_delivery()  // Uses Ship
```

**When to Use:**
- Class can't anticipate type of objects to create
- Subclasses specify objects to create
- Delegate responsibility to helper subclasses

---

### 3. Abstract Factory

**Intent:** Provide interface for creating families of related objects without specifying concrete classes.

```pseudocode
// Abstract products
interface Button:
  render(): void

interface Checkbox:
  render(): void

// Concrete products - Windows
class WindowsButton implements Button:
  render():
    print("Render Windows button")

class WindowsCheckbox implements Checkbox:
  render():
    print("Render Windows checkbox")

// Concrete products - Mac
class MacButton implements Button:
  render():
    print("Render Mac button")

class MacCheckbox implements Checkbox:
  render():
    print("Render Mac checkbox")

// Abstract factory
interface GUIFactory:
  create_button(): Button
  create_checkbox(): Checkbox

// Concrete factories
class WindowsFactory implements GUIFactory:
  create_button():
    return new WindowsButton()
  
  create_checkbox():
    return new WindowsCheckbox()

class MacFactory implements GUIFactory:
  create_button():
    return new MacButton()
  
  create_checkbox():
    return new MacCheckbox()

// Client
class Application:
  factory: GUIFactory
  button: Button
  checkbox: Checkbox
  
  constructor(factory):
    this.factory = factory
  
  create_ui():
    this.button = this.factory.create_button()
    this.checkbox = this.factory.create_checkbox()
  
  render():
    this.button.render()
    this.checkbox.render()

// Usage
factory = detect_os() == "Windows" ? new WindowsFactory() : new MacFactory()
app = new Application(factory)
app.create_ui()
app.render()
```

**When to Use:**
- System should be independent of product creation
- System configured with multiple product families
- Family of related products designed to be used together

---

### 4. Builder

**Intent:** Separate construction of complex object from its representation.

```pseudocode
class House:
  walls: integer
  doors: integer
  windows: integer
  roof: string
  garage: boolean
  pool: boolean
  
  describe():
    print("House with " + this.walls + " walls, " + 
          this.doors + " doors, " + this.windows + " windows")

// Builder interface
interface HouseBuilder:
  reset(): void
  build_walls(count): HouseBuilder
  build_doors(count): HouseBuilder
  build_windows(count): HouseBuilder
  build_roof(type): HouseBuilder
  build_garage(): HouseBuilder
  build_pool(): HouseBuilder
  get_result(): House

// Concrete builder
class ConcreteHouseBuilder implements HouseBuilder:
  house: House
  
  constructor():
    this.reset()
  
  reset():
    this.house = new House()
  
  build_walls(count):
    this.house.walls = count
    return this
  
  build_doors(count):
    this.house.doors = count
    return this
  
  build_windows(count):
    this.house.windows = count
    return this
  
  build_roof(type):
    this.house.roof = type
    return this
  
  build_garage():
    this.house.garage = true
    return this
  
  build_pool():
    this.house.pool = true
    return this
  
  get_result():
    result = this.house
    this.reset()
    return result

// Director (optional)
class HouseDirector:
  builder: HouseBuilder
  
  constructor(builder):
    this.builder = builder
  
  build_minimal_house():
    return this.builder
      .build_walls(4)
      .build_doors(1)
      .build_windows(2)
      .build_roof("flat")
      .get_result()
  
  build_luxury_house():
    return this.builder
      .build_walls(8)
      .build_doors(3)
      .build_windows(10)
      .build_roof("gabled")
      .build_garage()
      .build_pool()
      .get_result()

// Usage
builder = new ConcreteHouseBuilder()
director = new HouseDirector(builder)

minimal = director.build_minimal_house()
luxury = director.build_luxury_house()

// Or build custom house
custom = builder
  .build_walls(6)
  .build_doors(2)
  .build_windows(4)
  .build_roof("flat")
  .build_pool()
  .get_result()
```

**When to Use:**
- Construction process must allow different representations
- Construction is complex with many steps
- Want immutable objects with many optional parameters

---

### 5. Prototype

**Intent:** Create new objects by copying existing objects (prototypes).

```pseudocode
// Prototype interface
interface Cloneable:
  clone(): Cloneable

// Concrete prototype
class Shape implements Cloneable:
  x: integer
  y: integer
  color: string
  
  constructor(x, y, color):
    this.x = x
    this.y = y
    this.color = color
  
  clone():
    return new Shape(this.x, this.y, this.color)

class Rectangle extends Shape:
  width: integer
  height: integer
  
  constructor(x, y, color, width, height):
    super(x, y, color)
    this.width = width
    this.height = height
  
  clone():
    return new Rectangle(this.x, this.y, this.color, this.width, this.height)

class Circle extends Shape:
  radius: integer
  
  constructor(x, y, color, radius):
    super(x, y, color)
    this.radius = radius
  
  clone():
    return new Circle(this.x, this.y, this.color, this.radius)

// Prototype registry
class ShapeRegistry:
  shapes: Map<string, Shape>
  
  constructor():
    this.shapes = new Map()
  
  register(name, shape):
    this.shapes.set(name, shape)
  
  get(name):
    return this.shapes.get(name).clone()

// Usage
registry = new ShapeRegistry()

registry.register("red_circle", new Circle(0, 0, "red", 10))
registry.register("blue_rect", new Rectangle(0, 0, "blue", 20, 30))

circle1 = registry.get("red_circle")
circle2 = registry.get("red_circle")
// circle1 and circle2 are separate instances with same properties
```

**When to Use:**
- Object creation is expensive
- Avoid subclasses of object creator
- Runtime specification of objects to create

---

## Structural Patterns

### 6. Adapter

**Intent:** Convert interface of a class into another interface clients expect.

```pseudocode
// Target interface
interface MediaPlayer:
  play(filename): void

// Adaptee (incompatible interface)
class AdvancedMediaPlayer:
  play_vlc(filename):
    print("Playing VLC file: " + filename)
  
  play_mp4(filename):
    print("Playing MP4 file: " + filename)

// Adapter
class MediaAdapter implements MediaPlayer:
  advanced_player: AdvancedMediaPlayer
  
  constructor():
    this.advanced_player = new AdvancedMediaPlayer()
  
  play(filename):
    if filename.ends_with(".vlc"):
      this.advanced_player.play_vlc(filename)
    elif filename.ends_with(".mp4"):
      this.advanced_player.play_mp4(filename)

// Client
class AudioPlayer implements MediaPlayer:
  adapter: MediaAdapter
  
  play(filename):
    if filename.ends_with(".mp3"):
      print("Playing MP3 file: " + filename)
    elif filename.ends_with(".vlc") or filename.ends_with(".mp4"):
      this.adapter = new MediaAdapter()
      this.adapter.play(filename)
    else:
      print("Invalid format")

// Usage
player = new AudioPlayer()
player.play("song.mp3")
player.play("movie.mp4")
player.play("video.vlc")
```

**When to Use:**
- Use existing class with incompatible interface
- Create reusable class with unrelated classes
- Need to use several existing subclasses

---

### 7. Bridge

**Intent:** Decouple abstraction from implementation so they can vary independently.

```pseudocode
// Implementation interface
interface Device:
  is_enabled(): boolean
  enable(): void
  disable(): void
  get_volume(): integer
  set_volume(percent): void

// Concrete implementations
class TV implements Device:
  on: boolean
  volume: integer
  
  is_enabled():
    return this.on
  
  enable():
    this.on = true
  
  disable():
    this.on = false
  
  get_volume():
    return this.volume
  
  set_volume(percent):
    this.volume = percent

class Radio implements Device:
  // Similar implementation

// Abstraction
class RemoteControl:
  device: Device
  
  constructor(device):
    this.device = device
  
  toggle_power():
    if this.device.is_enabled():
      this.device.disable()
    else:
      this.device.enable()
  
  volume_up():
    this.device.set_volume(this.device.get_volume() + 10)
  
  volume_down():
    this.device.set_volume(this.device.get_volume() - 10)

// Refined abstraction
class AdvancedRemoteControl extends RemoteControl:
  mute():
    this.device.set_volume(0)

// Usage
tv = new TV()
remote = new RemoteControl(tv)
remote.toggle_power()
remote.volume_up()

radio = new Radio()
advanced_remote = new AdvancedRemoteControl(radio)
advanced_remote.mute()
```

**When to Use:**
- Avoid permanent binding between abstraction and implementation
- Both abstraction and implementation should be extensible
- Changes in implementation shouldn't affect clients

---

### 8. Composite

**Intent:** Compose objects into tree structures to represent part-whole hierarchies.

```pseudocode
// Component interface
interface Graphic:
  draw(): void
  move(x, y): void

// Leaf
class Dot implements Graphic:
  x: integer
  y: integer
  
  constructor(x, y):
    this.x = x
    this.y = y
  
  draw():
    print("Draw dot at (" + this.x + ", " + this.y + ")")
  
  move(x, y):
    this.x += x
    this.y += y

// Composite
class CompoundGraphic implements Graphic:
  children: List<Graphic>
  
  constructor():
    this.children = []
  
  add(child):
    this.children.append(child)
  
  remove(child):
    this.children.remove(child)
  
  draw():
    for child in this.children:
      child.draw()
  
  move(x, y):
    for child in this.children:
      child.move(x, y)

// Usage
dot1 = new Dot(1, 2)
dot2 = new Dot(3, 4)

group1 = new CompoundGraphic()
group1.add(dot1)
group1.add(dot2)

dot3 = new Dot(5, 6)
group2 = new CompoundGraphic()
group2.add(dot3)
group2.add(group1)

group2.draw()  // Draws all dots
group2.move(10, 10)  // Moves all dots
```

**When to Use:**
- Represent part-whole hierarchies
- Treat individual objects and compositions uniformly
- Structure can have any level of complexity

---

### 9. Decorator

**Intent:** Attach additional responsibilities to object dynamically.

```pseudocode
// Component interface
interface DataSource:
  write_data(data): void
  read_data(): string

// Concrete component
class FileDataSource implements DataSource:
  filename: string
  
  constructor(filename):
    this.filename = filename
  
  write_data(data):
    write_to_file(this.filename, data)
  
  read_data():
    return read_from_file(this.filename)

// Base decorator
abstract class DataSourceDecorator implements DataSource:
  wrappee: DataSource
  
  constructor(source):
    this.wrappee = source
  
  write_data(data):
    this.wrappee.write_data(data)
  
  read_data():
    return this.wrappee.read_data()

// Concrete decorators
class EncryptionDecorator extends DataSourceDecorator:
  write_data(data):
    encrypted = encrypt(data)
    super.write_data(encrypted)
  
  read_data():
    data = super.read_data()
    return decrypt(data)

class CompressionDecorator extends DataSourceDecorator:
  write_data(data):
    compressed = compress(data)
    super.write_data(compressed)
  
  read_data():
    data = super.read_data()
    return decompress(data)

// Usage
source = new FileDataSource("data.txt")
source.write_data("Hello World")

// With encryption
encrypted_source = new EncryptionDecorator(source)
encrypted_source.write_data("Secret message")

// With encryption and compression
secure_source = new CompressionDecorator(new EncryptionDecorator(source))
secure_source.write_data("Compressed and encrypted")
```

**When to Use:**
- Add responsibilities to objects dynamically
- Responsibilities can be withdrawn
- Extension by subclassing is impractical

---

### 10. Facade

**Intent:** Provide unified interface to set of interfaces in subsystem.

```pseudocode
// Complex subsystem classes
class CPU:
  freeze():
    print("CPU: Freeze")
  
  jump(position):
    print("CPU: Jump to " + position)
  
  execute():
    print("CPU: Execute")

class Memory:
  load(position, data):
    print("Memory: Load data at " + position)

class HardDrive:
  read(sector, size):
    print("HardDrive: Read sector " + sector)
    return "data"

// Facade
class ComputerFacade:
  cpu: CPU
  memory: Memory
  hard_drive: HardDrive
  
  constructor():
    this.cpu = new CPU()
    this.memory = new Memory()
    this.hard_drive = new HardDrive()
  
  start():
    this.cpu.freeze()
    this.memory.load(BOOT_ADDRESS, this.hard_drive.read(BOOT_SECTOR, SECTOR_SIZE))
    this.cpu.jump(BOOT_ADDRESS)
    this.cpu.execute()

// Usage
computer = new ComputerFacade()
computer.start()  // Simple interface to complex system
```

**When to Use:**
- Provide simple interface to complex subsystem
- Decouple subsystem from clients
- Layer your subsystems

---

### 11. Flyweight

**Intent:** Use sharing to support large numbers of fine-grained objects efficiently.

```pseudocode
// Flyweight (intrinsic state)
class TreeType:
  name: string
  color: string
  texture: string
  
  constructor(name, color, texture):
    this.name = name
    this.color = color
    this.texture = texture
  
  draw(x, y):
    print("Draw " + this.name + " tree at (" + x + ", " + y + ")")

// Flyweight factory
class TreeFactory:
  tree_types: Map<string, TreeType>
  
  constructor():
    this.tree_types = new Map()
  
  get_tree_type(name, color, texture):
    key = name + "_" + color + "_" + texture
    
    if not this.tree_types.has(key):
      this.tree_types.set(key, new TreeType(name, color, texture))
    
    return this.tree_types.get(key)

// Context (extrinsic state)
class Tree:
  x: integer
  y: integer
  type: TreeType
  
  constructor(x, y, type):
    this.x = x
    this.y = y
    this.type = type
  
  draw():
    this.type.draw(this.x, this.y)

// Forest (client)
class Forest:
  trees: List<Tree>
  factory: TreeFactory
  
  constructor():
    this.trees = []
    this.factory = new TreeFactory()
  
  plant_tree(x, y, name, color, texture):
    type = this.factory.get_tree_type(name, color, texture)
    tree = new Tree(x, y, type)
    this.trees.append(tree)
  
  draw():
    for tree in this.trees:
      tree.draw()

// Usage
forest = new Forest()
forest.plant_tree(1, 2, "Oak", "Green", "Oak texture")
forest.plant_tree(3, 4, "Oak", "Green", "Oak texture")  // Reuses TreeType
forest.plant_tree(5, 6, "Pine", "Dark Green", "Pine texture")
forest.draw()
```

**When to Use:**
- Application uses large number of objects
- Storage costs are high due to quantity
- Most object state can be made extrinsic
- Many groups of objects can be replaced by few shared objects

---

### 12. Proxy

**Intent:** Provide surrogate or placeholder for another object to control access.

```pseudocode
// Subject interface
interface ThirdPartyYouTubeLib:
  list_videos(): List
  get_video_info(id): Video
  download_video(id): Video

// Real subject
class ThirdPartyYouTubeClass implements ThirdPartyYouTubeLib:
  list_videos():
    print("Connecting to YouTube...")
    return download_video_list()
  
  get_video_info(id):
    print("Getting video info...")
    return get_info_from_youtube(id)
  
  download_video(id):
    print("Downloading video...")
    return download_from_youtube(id)

// Proxy
class CachedYouTubeClass implements ThirdPartyYouTubeLib:
  service: ThirdPartyYouTubeLib
  list_cache: List
  video_cache: Map
  
  constructor(service):
    this.service = service
    this.video_cache = new Map()
  
  list_videos():
    if this.list_cache == null:
      this.list_cache = this.service.list_videos()
    return this.list_cache
  
  get_video_info(id):
    if not this.video_cache.has(id):
      this.video_cache.set(id, this.service.get_video_info(id))
    return this.video_cache.get(id)
  
  download_video(id):
    if not this.video_cache.has(id):
      this.video_cache.set(id, this.service.download_video(id))
    return this.video_cache.get(id)

// Usage
service = new ThirdPartyYouTubeClass()
proxy = new CachedYouTubeClass(service)

proxy.list_videos()  // Downloads
proxy.list_videos()  // Returns from cache
```

**When to Use:**
- Virtual proxy: lazy initialization of expensive object
- Protection proxy: access control
- Remote proxy: local representation of remote object
- Logging proxy: log requests to object

---

## Behavioral Patterns

### 13-23. (Continued in next section due to length)

For the remaining behavioral patterns (Chain of Responsibility, Command, Iterator, Mediator, Memento, Observer, State, Strategy, Template Method, Visitor), see advanced-techniques.md or dedicated behavioral patterns documentation.

---

## Quick Reference

| Pattern | Category | Purpose |
|---------|----------|---------|
| Singleton | Creational | One instance |
| Factory Method | Creational | Subclass decides creation |
| Abstract Factory | Creational | Family of related objects |
| Builder | Creational | Complex construction |
| Prototype | Creational | Clone objects |
| Adapter | Structural | Interface conversion |
| Bridge | Structural | Decouple abstraction/implementation |
| Composite | Structural | Tree structures |
| Decorator | Structural | Add responsibilities |
| Facade | Structural | Simplified interface |
| Flyweight | Structural | Share objects |
| Proxy | Structural | Control access |
