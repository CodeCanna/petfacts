class Animal:
    def __init__(self, id: int, name: str, type: str, image: str):
        self._id = id
        self._name = name
        self._type = type
        self._image = image


    def to_dict(self):
        return {
            self._id,
            self._name,
            self._type,
            self._image
        }

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, id: int) -> None:
        self._id = id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, type: str):
        self._type = type

    @property
    def image(self) -> str:
        return self._image

    @image.setter
    def image(self, path: str):
        self._image = path

    

