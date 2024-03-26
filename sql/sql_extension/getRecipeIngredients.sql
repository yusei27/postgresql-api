SELECT
	fk_id_recipe,
	fk_id_ingredient,
	amount,
	name_ingredient,
	fk_id_unit,
	fk_id_genre
FROM
	{0[schema]}.recipe_ingredient_table
LEFT JOIN
	{0[schema]}.ingredient_table
	ON
	 ingredient_table.id_ingredient	= recipe_ingredient_table.fk_id_ingredient
WHERE
	fk_id_recipe = {0[id_recipe]}