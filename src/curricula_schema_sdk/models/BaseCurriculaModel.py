import importlib

from pydantic import BaseModel, Field, model_validator


class BaseCurriculaModel(BaseModel):
    title: str
    clazz: str = Field(default=None)

    # Populate clazz automatically
    @model_validator(mode="after")
    def _set_clazz(self):
        if not self.clazz:
            self.clazz = f"{self.__class__.__module__}.{self.__class__.__name__}"
        return self

    @classmethod
    def from_json(cls, json_str: str):
        """Deserialize JSON into the correct subclass."""
        import json
        data = json.loads(json_str)
        clazz_path = data.get("clazz")
        if not clazz_path:
            # No clazz → assume current class
            return cls.model_validate(data)

        module_name, _, class_name = clazz_path.rpartition(".")
        mod = importlib.import_module(module_name)
        subclass = getattr(mod, class_name)
        return subclass.model_validate(data)

    def to_json(self, **kwargs) -> str:
        """Dump as JSON with clazz included."""
        return self.model_dump_json(by_alias=True, **kwargs)
