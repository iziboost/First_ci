from pydantic import BaseModel


class RecipeBase(BaseModel):
    id: int
    title: str
    time_min: int

    class Config:
        orm_mode = True


class RecipeListResponse(RecipeBase):
    amount_views: int


class RecipeDetailResponse(RecipeBase):
    ingredients: str
    description: str
    amount_views: int


class RecipeCreate(BaseModel):
    title: str
    time_min: int
    ingredients: str
    description: str
