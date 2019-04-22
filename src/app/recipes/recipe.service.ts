import { Recipe } from './recipe.model';
import { EventEmitter, Injectable } from '@angular/core';
import { Ingredient } from '../shared/ingredient.model';
import { ShoppingListService } from '../shopping-list/shopping-list.service';

@Injectable()
export class RecipeService {
  recipeSelected = new EventEmitter<Recipe>();

  private recipes: Recipe[] = [
    // tslint:disable-next-line: max-line-length
    new Recipe(
      'Tasty Schnizel',
      'This is simply a test',
      'https://cdn.pixabay.com/photo/2017/06/21/22/42/recipe-2428926_1280.jpg',
      [new Ingredient('Meat', 1), new Ingredient('French frieis', 20)]
    ),
    new Recipe(
      'Big Fat Burger',
      'This is simply a test',
      'https://cdn.pixabay.com/photo/2017/06/21/22/42/recipe-2428926_1280.jpg',
      [new Ingredient('Buns', 2), new Ingredient('Meat', 1)]
    )
  ];

  constructor(private shoppingListService: ShoppingListService) {}

  getRecipes() {
    return this.recipes.slice();
  }

  getRecipe(index: number){
    return this.recipes[index];
  }

  addIngredientsToShopingList(ingredits: Ingredient[]) {
    this.shoppingListService.addIngredients(ingredits);
  }
}
