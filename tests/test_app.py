import pytest


@pytest.mark.asyncio
async def test_create_recipe(client):
    """Тест 1: Создание рецепта"""
    recipe = {
        "title": "Яичница",
        "time_min": 5,
        "ingredients": "яйца, масло, соль",
        "description": "Разбить яйца и пожарить"
    }

    response = await client.post("/recipe/", json=recipe)

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Яичница"
    assert data["amount_views"] == 0
    print(f"✅ Рецепт создан: {data['title']}")


@pytest.mark.asyncio
async def test_get_recipe_and_views(client):
    """Тест 2: Получение рецепта и счетчик просмотров"""
    # Создаем рецепт
    create_resp = await client.post("/recipe/", json={
        "title": "Блины",
        "time_min": 30,
        "ingredients": "мука, молоко, яйца",
        "description": "Замесить и пожарить"
    })
    recipe_id = create_resp.json()["id"]

    # Получаем рецепт 2 раза
    resp1 = await client.get(f"/recipes/{recipe_id}")
    resp2 = await client.get(f"/recipes/{recipe_id}")

    assert resp1.json()["amount_views"] == 1
    assert resp2.json()["amount_views"] == 2
    print(f"✅ Просмотры: 0 → 1 → 2")


@pytest.mark.asyncio
async def test_recipe_not_found(client):
    """Тест 3: Рецепт не найден"""
    response = await client.get("/recipes/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Recipe not found"
    print(f"✅ 404 Not Found работает")