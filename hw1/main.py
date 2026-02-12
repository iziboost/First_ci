from contextlib import asynccontextmanager
from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException
from sqlalchemy.future import select

from hw1 import models, schemas
from hw1.database import engine, session


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield
    await session.close()
    await engine.dispose()


app = FastAPI(lifespan=lifespan)


@app.get("/recipes", response_model=List[schemas.RecipeListResponse])
async def recipes() -> List[models.Recipe]:
    res = await session.execute(select(models.Recipe))
    return res.scalars().all()


@app.get("/recipes/{recipe_id}", response_model=schemas.RecipeDetailResponse)
async def recipe(recipe_id: int) -> models.Recipe:

    recipe = await session.get(models.Recipe, recipe_id)

    # Если рецепт не найден - возвращаем 404
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    # Увеличиваем счетчик просмотров
    recipe.increment_view()
    await session.commit()

    return recipe


@app.post("/recipe/", response_model=schemas.RecipeDetailResponse)
async def create_recipe(recipe: schemas.RecipeCreate) -> models.Recipe:
    new_recipe = models.Recipe(**recipe.model_dump())
    async with session.begin():
        session.add(new_recipe)
    return new_recipe


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
