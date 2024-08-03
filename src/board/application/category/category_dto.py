from pydantic import BaseModel, model_validator


class CategoryCreateDTO(BaseModel):
    name: str


class CategoryUpdateDTO(BaseModel):
    name: str | None

    @model_validator(mode="after")
    def check_at_least_one_field(self):
        if all(value is None for value in self.model_dump().values()):
            raise ValueError("At least one field must be provided for update")
        return self


class CategoryResponseDTO(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
